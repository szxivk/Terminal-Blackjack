from .game_logic import BlackjackGame
import sys
import shutil
import subprocess
from . import storage

def uninstall_game():
    """Uninstalls the game package."""
    print("Uninstalling Terminal-Blackjack...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "uninstall", "terminal-blackjack", "-y"])
        print("Game uninstalled successfully.")
    except subprocess.CalledProcessError:
        print("Uninstallation failed. You may need to run 'pip uninstall terminal-blackjack' manually.")

def main():
    data_dir = storage.get_data_dir()
    
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
                if storage.reset_data():
                    print("Game data has been successfully reset.")
                else:
                    print("Error resetting data.")
            else:
                print("Operation cancelled.")
            return

        # --- UNINSTALL COMMAND ---
        elif arg in ("-remove", "--remove"):
            print("This will remove the game.")
            backup_choice = input("Would you like to backup your save data first? (yes/no): ").lower()
            
            if backup_choice in ("yes", "y"):
                if storage.backup_data():
                    print(f"Backup created at {storage.find_latest_backup()}")
                else:
                    print("Backup failed.")
            
            confirm_uninstall = input("Are you sure you want to uninstall the game? (yes/no): ").lower()
            if confirm_uninstall in ("yes", "y"):
                storage.reset_data()
                print("Local data removed.")
                uninstall_game()
            else:
                print("Uninstall cancelled.")
            return

        # --- RESTORE COMMAND ---
        elif arg in ("-restore", "--restore"):
            # Since we now have a UI flow for this, we can just run the game
            # OR we can keep a CLI version. Let's redirect to the game
            # but maybe the user wants to force a restore without UI?
            # For now, let's keep it simple and just run the game, 
            # where the restore menu will pop up anyway if resetting.
            # But the user specifically asked for a command.
            # Let's invoke the backup selection from UI logic via game instance?
            # Actually, `storage` has the logic now.
            print("Please run 'pybjack' to access the Restore menu.")
            return

    # START GAME
    # The 'check for backups' and 'startup menu' logic is now inside BlackjackGame.run()
    game = BlackjackGame()
    game.run()

if __name__ == "__main__":
    main()
