# Terminal Blackjack

**The classic casino experience, re-engineered for the command line.**

A feature-rich Python application that combines a beautiful terminal UI with serious functionality. Includes multi-user profile management, auto-backups to prevent data loss, and an integrated Trivia Engine to earn in-game currency. Built to prove that terminal apps can be as beautiful as they are functional.

![Terminal Blackjack](https://img.shields.io/badge/Made%20with-Rich-blueviolet?style=flat-square) ![Python](https://img.shields.io/badge/Python-3.12+-blue?style=flat-square) ![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)

## Features

Key Engineering Highlights:
* **Modern TUI:** Built with [Rich](https://pypi.org/project/rich/) and [Questionary](https://pypi.org/project/questionary/) for a polished visual experience.

- **Robust Save System**: 
    -   **Multi-User Support**: Create separate profiles for different players.
    -   **Auto-Save**: Progress is saved automatically after every round.
    -   **Smart Backups**: Timestamped backups allow you to restore previous sessions.
- **Trivia Mode**: running low on cash? Earn free chips by answering trivia questions!
    -   **General Knowledge**: Built-in questions.
    -   **Custom Topics**: add your own JSON quizzes.
- **CLI Power**: Manage game data directly from the terminal.
- **Distribution:** Full `pip` installable package structure.

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/szxivk/Terminal-Blackjack.git
   cd Terminal-Blackjack
   ```

2. **Install the package**:
   ```bash
   pip install .
   ```
   *(Note: You can also use pipx install . if you prefer an isolated installation)*

## Usage

Once installed, you can launch the game from anywhere in your terminal:

```bash
pybjack
```

### CLI Commands

- **Start Game**: `pybjack`
-   **Help**: `pybjack -help` (Show all available commands)
-   **Reset Data**: `pybjack -reset` (Wipes all saves and settings)
-   **Uninstall**: `pybjack -remove` (Clean uninstallation, optionally keeps saves)

## How to Play

1.  **Objective**: Beat the dealer's hand without going over 21.
2.  **Unlocks**:
    -   **Earn Chips**: Answer trivia questions to build your bankroll.
3.  **Controls**:
    -   Use **Arrow Keys** (↑/↓) to navigate menus.
    -   Press **Enter** to select.

## Custom Trivia

You can add your own trivia questions!

1.  Navigate to `~/.terminal_blackjack/questions/`.
2.  Create a new JSON file (e.g., `history.json`).
3.  Format it like this:
    ```json
    {
        "topic": "History",
        "questions": [
            {
                "question": "Who was the first US President?",
                "options": ["Lincoln", "Washington", "Jefferson", "Adams"],
                "correct_index": 1
            }
        ]
    }
    ```
4.  Launch the game, go to **Earn Chips > Custom MCQs**, and select your topic!


## Security & Privacy

-   **Local Only**: All data (chips, saves, sessions) is stored locally on your machine. No data is sent to any external server.
All game data is stored securely in your home directory:
`~/.terminal_blackjack/`
-   **Open Source**: The code is fully transparent and open source.

---
**by szxivk**
