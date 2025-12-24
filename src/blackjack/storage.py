import json
import os
import shutil
import hashlib
from pathlib import Path
from datetime import datetime
from typing import Optional, Dict, List

# Store data in user's home directory
DATA_DIR = Path.home() / ".terminal_blackjack"
DATA_FILE = DATA_DIR / "players.json"
SESSION_FILE = DATA_DIR / "session.json"
BACKUP_ROOT = DATA_DIR / "saves"

# ... (Previous code remains, but need to check if BACKUP_ROOT usage is consistent)
# Actually, I am editing the file content. I should only specificy the chunk.

# Skipping lines 15-184...

def reset_data(keep_saves: bool = False) -> bool:
    """
    Deletes the current data directory.
    If keep_saves is True, preserves the saves directory.
    """
    global CURRENT_SAVE_SLOT
    CURRENT_SAVE_SLOT = None
    
    if not DATA_DIR.exists():
        return True
    
    try:
        if keep_saves:
            # Delete specific files/dirs but keep saves
            if DATA_FILE.exists():
                os.remove(DATA_FILE)
            if SESSION_FILE.exists():
                os.remove(SESSION_FILE)
            
            questions_dir = DATA_DIR / "questions"
            if questions_dir.exists():
                shutil.rmtree(questions_dir)
            
            # Note: We rely on BACKUP_ROOT being inside DATA_DIR.
            # If any other files exist, they might persist, but main data is gone.
            
        else:
            # Full wipe
            shutil.rmtree(DATA_DIR)
            
        return True
    except Exception:
        return False

def _get_data_path() -> Path:
    """Ensure data directory exists and return path to data file."""
    DATA_DIR.mkdir(exist_ok=True)
    return DATA_FILE

def get_data_dir() -> Path:
    """Return the main data directory path."""
    return DATA_DIR

def _hash_name(name: str) -> str:
    """Create a hash of the player name for storage key."""
    return hashlib.sha256(name.lower().strip().encode()).hexdigest()[:16]

def _load_all_data() -> Dict:
    """Load all player data from file."""
    path = _get_data_path()
    if not path.exists():
        return {}
    try:
        with open(path, 'r') as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return {}

def _save_all_data(data: Dict) -> bool:
    """Save all player data to file."""
    path = _get_data_path()
    try:
        with open(path, 'w') as f:
            json.dump(data, f, indent=2)
        return True
    except IOError:
        return False

def load_player(name: str) -> Optional[int]:
    """
    Load player chips by name.
    Returns None if player doesn't exist, otherwise returns chip count.
    """
    data = _load_all_data()
    key = _hash_name(name)
    
    if key in data:
        return data[key].get("chips", None)
    return None

def save_player(name: str, chips: int) -> bool:
    """Save player chips."""
    data = _load_all_data()
    key = _hash_name(name)
    
    data[key] = {
        "name": name,
        "chips": max(0, chips)  # Never save negative chips
    }
    
    return _save_all_data(data)

def is_new_player(name: str) -> bool:
    """Check if player is new (no saved data)."""
    return load_player(name) is None

# --- Session Management ---

def save_session(username: str):
    """Save the last active user session."""
    try:
        DATA_DIR.mkdir(exist_ok=True)
        with open(SESSION_FILE, 'w') as f:
            json.dump({"last_active_user": username}, f)
    except IOError:
        pass

def load_session() -> Optional[str]:
    """Load the last active user."""
    if not SESSION_FILE.exists():
        return None
    try:
        with open(SESSION_FILE, 'r') as f:
            data = json.load(f)
            return data.get("last_active_user")
    except (json.JSONDecodeError, IOError):
        return None

# --- Backup & Restore Logic ---

CURRENT_SAVE_SLOT: Optional[Path] = None

def get_available_backups() -> List[Path]:
    """Returns a list of all valid save-* directories, sorted by newest first."""
    if not BACKUP_ROOT.exists():
        return []
    
    saves = []
    for item in BACKUP_ROOT.iterdir():
        if item.is_dir() and item.name.startswith("save-"):
            saves.append(item)
    
    # Sort by modification time, newest first
    return sorted(saves, key=lambda p: p.stat().st_mtime, reverse=True)

def find_latest_backup() -> Optional[Path]:
    """Finds the most recently modified save-* directory."""
    backups = get_available_backups()
    return backups[0] if backups else None

def get_next_backup_path(username: str = "unknown") -> Path:
    """Creates a timestamped backup path with username."""
    # Sanitize username
    safe_username = "".join(c for c in username if c.isalnum() or c in ('-', '_')).strip()
    if not safe_username:
        safe_username = "unknown"
        
    timestamp = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    return BACKUP_ROOT / f"save-{safe_username}-{timestamp}"

def save_current_game() -> bool:
    """
    Saves the current game state.
    - If loaded from a backup, updates that backup.
    - If new game, creates a new timestamped backup.
    """
    if not DATA_DIR.exists():
        return False
        
    global CURRENT_SAVE_SLOT
    
    try:
        # Prevent crash if running from the backup directory
        if BACKUP_ROOT.exists() and os.getcwd().startswith(str(BACKUP_ROOT.parent.resolve())):
            os.chdir(Path.home())

        BACKUP_ROOT.mkdir(parents=True, exist_ok=True)
        
        target_dir = CURRENT_SAVE_SLOT
        
        if target_dir and target_dir.exists():
            # Update existing save
            # We use copytree with dirs_exist_ok=True to overwrite
            # CRITICAL: Ignore 'saves' directory to prevent recursive copying of backup folder into itself
            shutil.copytree(DATA_DIR, target_dir, dirs_exist_ok=True, ignore=shutil.ignore_patterns("saves"))
            # Touch the directory to update modification time
            target_dir.touch()
        else:
            # Create new save
            current_user = load_session()
            target_dir = get_next_backup_path(current_user if current_user else "unknown")
            # CRITICAL: Ignore 'saves' directory
            shutil.copytree(DATA_DIR, target_dir, dirs_exist_ok=True, ignore=shutil.ignore_patterns("saves"))
            CURRENT_SAVE_SLOT = target_dir
            
        return True
    except Exception:
        return False

def backup_data() -> bool:
    """Legacy backup function - redirects to save_current_game."""
    return save_current_game()

def restore_data(source_dir: Optional[Path] = None) -> bool:
    """Restores data from a backup source to DATA_DIR."""
    global CURRENT_SAVE_SLOT
    
    if source_dir is None:
        source_dir = find_latest_backup()
        
    if source_dir is None or not source_dir.exists():
        return False
    
    try:
        # CRITICAL: Do NOT delete DATA_DIR if BACKUP_ROOT is inside it!
        # Instead, clean up specific game files before restoring.
        if DATA_FILE.exists():
            os.remove(DATA_FILE)
        if SESSION_FILE.exists():
            os.remove(SESSION_FILE)
            
        questions_dir = DATA_DIR / "questions"
        if questions_dir.exists():
            shutil.rmtree(questions_dir)
            
        # Restore data
        shutil.copytree(source_dir, DATA_DIR, dirs_exist_ok=True, ignore=shutil.ignore_patterns("saves"))
        CURRENT_SAVE_SLOT = source_dir
        return True
    except Exception:
        return False

def reset_data(keep_saves: bool = False) -> bool:
    """
    Deletes the current data directory.
    If keep_saves is True, preserves the saves directory.
    """
    global CURRENT_SAVE_SLOT
    CURRENT_SAVE_SLOT = None
    
    if not DATA_DIR.exists():
        return True
    
    try:
        if keep_saves:
            # Delete specific files/dirs but keep saves
            if DATA_FILE.exists():
                os.remove(DATA_FILE)
            if SESSION_FILE.exists():
                os.remove(SESSION_FILE)
            
            questions_dir = DATA_DIR / "questions"
            if questions_dir.exists():
                shutil.rmtree(questions_dir)
            
        else:
            # Full wipe
            shutil.rmtree(DATA_DIR)
            
        return True
    except Exception:
        return False
