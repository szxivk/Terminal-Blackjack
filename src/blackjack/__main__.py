from .game_logic import BlackjackGame
import sys
import shutil
import os
import subprocess
from pathlib import Path
from datetime import datetime
from .storage import get_data_dir

# New Backup Structure
BACKUP_ROOT = Path.home() / "Documents" / "pybjack-saves"

def get_next_backup_path() -> Path:
    """Creates a timestamped backup path (e.g., save-2023-12-23-14-30-00)."""
    timestamp = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    return BACKUP_ROOT / f"save-{timestamp}"

def get_available_backups() -> list[Path]:
    """Returns a list of all valid save-* directories, sorted by newest first."""
    if not BACKUP_ROOT.exists():
        return []
    
    saves = []
    for item in BACKUP_ROOT.iterdir():
        if item.is_dir() and item.name.startswith("save-"):
            saves.append(item)
    
    # Sort by modification time, newest first
    return sorted(saves, key=lambda p: p.stat().st_mtime, reverse=True)

def prompt_backup_selection() -> Path | None:
    """Lists backups and asks user to select one."""
    backups = get_available_backups()
    if not backups:
        print("No backups found.")
        return None

    print("\nAvailable Backups:")
    for i, backup in enumerate(backups, 1):
        # formatted_time = datetime.fromtimestamp(backup.stat().st_mtime).strftime("%Y-%m-%d %H:%M:%S")
        print(f"{i}. {backup.name}")
    
    print(f"{len(backups) + 1}. Cancel/Skip")
    
    while True:
        try:
            choice = input("\nSelect a backup to restore (number): ")
            if not choice.isdigit():
                continue
            
            idx = int(choice) - 1
            if 0 <= idx < len(backups):
                return backups[idx]
            elif idx == len(backups):
                return None
            else:
                print("Invalid selection.")
        except KeyboardInterrupt:
            return None

def backup_data(data_dir: Path):
    """Backups data to a new timestamped save slot."""
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
        source_dir = prompt_backup_selection()
        
    if source_dir is None:
        print("Restore cancelled.")
        return False
        
    if not source_dir.exists():
        print(f"No valid backup found at {source_dir}")
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
    # Only check if data directory doesn't exist (fresh install state) but valid backups exist
    backups = get_available_backups()
    if not data_dir.exists() and backups:
        print(f"Found {len(backups)} backup(s).")
        restore_choice = input("Would you like to restore your save data? (yes/no): ").lower()
        if restore_choice in ("yes", "y"):
            restore_data(data_dir)

    game = BlackjackGame()
    game.run()

if __name__ == "__main__":
    main()
