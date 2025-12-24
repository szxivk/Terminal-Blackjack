from blackjack import storage
from pathlib import Path
import shutil

# 1. Setup Data
print("Setting up data...")
storage.DATA_DIR.mkdir(parents=True, exist_ok=True)
storage.BACKUP_ROOT.mkdir(parents=True, exist_ok=True)

(storage.DATA_DIR / "players.json").touch()
(storage.BACKUP_ROOT / "save-TestUser-123").mkdir()

print(f"BACKUP_ROOT is: {storage.BACKUP_ROOT}")
assert storage.BACKUP_ROOT == Path.home() / ".terminal_blackjack" / "saves"

# 2. Test Keep Saves Reset
print("Testing Reset (Keep Saves)...")
storage.reset_data(keep_saves=True)

if not (storage.BACKUP_ROOT / "save-TestUser-123").exists():
    print("FAILURE: Backup missing after keep_saves=True")
else:
    print("SUCCESS: Backup preserved")

if (storage.DATA_DIR / "players.json").exists():
    print("FAILURE: players.json persists after reset")
else:
    print("SUCCESS: players.json deleted")

# 3. Test Full Reset
print("Testing Full Reset...")
storage.reset_data(keep_saves=False)

if storage.DATA_DIR.exists():
    print("FAILURE: DATA_DIR still exists")
else:
    print("SUCCESS: Full wipe verified")
