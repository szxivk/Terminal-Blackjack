from blackjack import storage
from pathlib import Path

# Setup dummy session
storage.save_session("VerifiedUser")

# Trigger save
storage.DATA_DIR.mkdir(parents=True, exist_ok=True)
storage.save_current_game()

# Check
backups = list(storage.BACKUP_ROOT.glob("save-VerifiedUser-*"))
if backups:
    print(f"SUCCESS: Created {backups[0].name}")
else:
    print("FAILURE: No named backup found")
