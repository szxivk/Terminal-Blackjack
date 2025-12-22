# Terminal Blackjack

A beautiful, simplified terminal-based Blackjack game written in Python.

## Features

- **Beautiful UI**: Powered by [Rich](https://pypi.org/project/rich/)
- **Arrow Key Navigation**: Intuitive menu system and gameplay using [Questionary](https://pypi.org/project/questionary/)
- **Player Persistence**: Your chips are saved locally and restored on return


## Requirements

- **Python**: 3.12+ (tested on Python 3.12.1)
- **Dependencies**:
  - `rich==14.2.0` - Terminal UI framework
  - `questionary==2.1.1` - Arrow key menu navigation

## Installation

1. Clone the repository
2. Create and activate a virtual environment (recommended):
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```
3. Install the required dependencies:
   ```bash
   pip install rich questionary
   ```
   Or use the requirements file:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

Start the game by running:

```bash
python3 main.py
```

Use arrow keys (↑↓) to navigate menus and select options. Press Enter to confirm your choice.

## Game Data

Player data is stored locally in `~/.terminal_blackjack/players.json`. Your chips are automatically saved after each round.

---
**by szxivk**

