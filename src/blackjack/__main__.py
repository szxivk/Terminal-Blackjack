from .game_logic import BlackjackGame
import sys
import shutil
import os
import subprocess
from pathlib import Path
from .storage import get_data_dir

# New Backup Structure
BACKUP_ROOT = Path.home() / "Documents" / "pybjack-saves"

def get_next_backup_path() -> Path:
    """Finds the next available save slot (e.g., save-1, save-2)."""
    i = 1
    while True:
        path = BACKUP_ROOT / f"save-{i}"
        if not path.exists():
            return path
        i += 1

def find_latest_backup() -> Path | None:
    """Finds the most recently modified save-* directory."""
    if not BACKUP_ROOT.exists():
        return None
    
    saves = []
    for item in BACKUP_ROOT.iterdir():
        if item.is_dir() and item.name.startswith("save-"):
            saves.append(item)
    
    if not saves:
        return None
        
    # Sort by modification time, newest first
    return sorted(saves, key=lambda p: p.stat().st_mtime, reverse=True)[0]

def backup_data(data_dir: Path):
    """Backups data to a new save slot."""
    if not data_dir.exists():
        print("No data to backup.")
        return False
    
    try:
        # Prevent crash if running from the backup directory
        if BACKUP_ROOT.exists() and os.getcwd().startswith(str(BACKUP_ROOT.parent.resolve())):
            os.chdir(Path.home())

        BACKUP_ROOT.mkdir(parents=True, exist_ok=True)
        
        target_dir = get_next_backup_path()
        
        shutil.copytree(data_dir, target_dir, dirs_exist_ok=True)
        print(f"Backup created at {target_dir}")
        return True
    except Exception as e:
        print(f"Backup failed: {e}")
        return False

def restore_data(target_dir: Path, source_dir: Path | None = None):
    """Restores data from backup."""
    if source_dir is None:
        source_dir = find_latest_backup()
        
    if source_dir is None or not source_dir.exists():
        print(f"No valid backup found at {source_dir if source_dir else BACKUP_ROOT}")
        return False
    
    try:
        if target_dir.exists():
            shutil.rmtree(target_dir)
        shutil.copytree(source_dir, target_dir)
        print(f"Data restored successfully from {source_dir.name}.")
        return True
    except Exception as e:
        print(f"Restore failed: {e}")
        return False

def uninstall_game():
    """Uninstalls the game package."""
    print("Uninstalling Terminal-Blackjack...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "uninstall", "terminal-blackjack", "-y"])
        print("Game uninstalled successfully.")
    except subprocess.CalledProcessError:
        print("Uninstallation failed. You may need to run 'pip uninstall terminal-blackjack' manually.")

def main():
    data_dir = get_data_dir()
    
    # Argument handling
    if len(sys.argv) > 1:
        arg = sys.argv[1]
        
        # --- RESET COMMAND ---
        if arg in ("-reset", "--reset"):
            if not data_dir.exists():
                print(f"No data found at {data_dir}")
                return

            print(f"WARNING: This will permanently delete all data at {data_dir}")
            
            confirm = input("Are you sure you want to proceed? (yes/no): ").lower()
            if confirm in ("yes", "y"):
                try:
                    shutil.rmtree(data_dir)
                    print("Game data has been successfully reset.")
                except Exception as e:
                    print(f"Error resetting data: {e}")
            else:
                print("Operation cancelled.")
            return

        # --- UNINSTALL COMMAND ---
        elif arg in ("-remove", "--remove"):
            print("This will remove the game.")
            backup_choice = input("Would you like to backup your save data first? (yes/no): ").lower()
            
            if backup_choice in ("yes", "y"):
                backup_data(data_dir)
            
            confirm_uninstall = input("Are you sure you want to uninstall the game? (yes/no): ").lower()
            if confirm_uninstall in ("yes", "y"):
                if data_dir.exists():
                    try:
                        shutil.rmtree(data_dir)
                        print("Local data removed.")
                    except Exception as e:
                        print(f"Could not remove local data: {e}")
                uninstall_game()
            else:
                print("Uninstall cancelled.")
            return

        # --- RESTORE COMMAND ---
        elif arg in ("-restore", "--restore"):
            source = None
            if len(sys.argv) > 2:
                source = Path(sys.argv[2])
            
            restore_data(data_dir, source)
            return

    # --- STARTUP CHECK ---
    # Only check if data directory doesn't exist (fresh install state) but a valid backup does
    latest_backup = find_latest_backup()
    if not data_dir.exists() and latest_backup:
        print(f"A previous backup ({latest_backup.name}) was found.")
        restore_choice = input("Would you like to restore your save data? (yes/no): ").lower()
        if restore_choice in ("yes", "y"):
            restore_data(data_dir, latest_backup)

    game = BlackjackGame()
    game.run()

if __name__ == "__main__":
    main()
