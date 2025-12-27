
import pytest
import sys
import json
from unittest.mock import patch, MagicMock, mock_open
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from blackjack import storage

def test_hash_name():
    """Test proper hashing of names."""
    h1 = storage._hash_name("TestUser")
    h2 = storage._hash_name("testuser") # Should be case insensitive
    h3 = storage._hash_name("  TestUser  ") # Should strip whitespace
    
    assert h1 == h2
    assert h1 == h3
    assert len(h1) == 16

@patch("blackjack.storage._get_data_path")
@patch("builtins.open")
def test_load_player_exists(mock_file, mock_get_path):
    """Test loading an existing player."""
    # Setup mock data
    fake_data = {
        storage._hash_name("Player1"): {"name": "Player1", "chips": 500}
    }
    
    # Configure the mock open to read our data
    # Create a mock file object
    mock_file_obj = MagicMock()
    mock_file_obj.read.return_value = json.dumps(fake_data)
    
    # Make the context manager return it (`with open(...) as f`)
    mock_file.return_value.__enter__.return_value = mock_file_obj
    
    # Configure path.exists() to return True
    mock_path = MagicMock()
    mock_path.exists.return_value = True
    mock_get_path.return_value = mock_path

    chips = storage.load_player("Player1")
    assert chips == 500

@patch("blackjack.storage._get_data_path")
@patch("builtins.open")
def test_load_player_not_found(mock_file, mock_get_path):
    """Test loading a non-existent player."""
    # Setup mock empty data
    mock_file_obj = MagicMock()
    mock_file_obj.read.return_value = "{}"
    mock_file.return_value.__enter__.return_value = mock_file_obj
    
    mock_path = MagicMock()
    mock_path.exists.return_value = True
    mock_get_path.return_value = mock_path

    chips = storage.load_player("UnknownPlayer")
    assert chips is None

@patch("blackjack.storage._get_data_path")
@patch("builtins.open")
def test_save_player(mock_file, mock_get_path):
    """Test saving a player."""
    # 1. First open() call (Read): return existing data
    # We need a mock that behaves as a context manager
    read_ctx = MagicMock()
    read_file = MagicMock()
    read_ctx.__enter__.return_value = read_file
    read_file.read.return_value = "{}"  # Return empty dict json

    # 2. Second open() call (Write): save new data
    write_ctx = MagicMock()
    write_file = MagicMock()
    write_ctx.__enter__.return_value = write_file
    
    # Configure open() to return these context managers in sequence
    mock_file.side_effect = [read_ctx, write_ctx]
    
    mock_path = MagicMock()
    mock_path.exists.return_value = True
    mock_get_path.return_value = mock_path

    success = storage.save_player("NewPlayer", 1000)
    assert success is True
    
    # Verify write called on the second file handle
    write_file.write.assert_called()

@patch("blackjack.storage.DATA_DIR")
@patch("blackjack.storage.shutil")
def test_reset_data_full(mock_shutil, mock_data_dir):
    """Test full data reset calls rmtree."""
    mock_data_dir.exists.return_value = True
    
    storage.reset_data(keep_saves=False)
    
    mock_shutil.rmtree.assert_called_with(storage.DATA_DIR)

@patch("blackjack.storage.DATA_DIR")
@patch("blackjack.storage.DATA_FILE")
@patch("blackjack.storage.SESSION_FILE")
@patch("blackjack.storage.os.remove")
def test_reset_data_keep_saves(mock_remove, mock_session, mock_data_file, mock_data_dir):
    """Test reset keeping saves only deletes specific files."""
    mock_data_dir.exists.return_value = True
    mock_data_file.exists.return_value = True
    mock_session.exists.return_value = True
    
    storage.reset_data(keep_saves=True)
    
    # Verify removals
    mock_remove.assert_any_call(mock_data_file)
    mock_remove.assert_any_call(mock_session)
