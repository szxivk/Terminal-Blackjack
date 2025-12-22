"""
Player data persistence module.
Stores player chips locally in a secure JSON file.
"""
import json
import os
import hashlib
from pathlib import Path
from typing import Optional, Dict

# Store data in user's home directory
DATA_DIR = Path.home() / ".terminal_blackjack"
DATA_FILE = DATA_DIR / "players.json"

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
