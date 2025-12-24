from rich.console import Console, Group
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich.prompt import Prompt
from rich.align import Align
from rich import box
import os

from .models.card import Card
from .models.player import Player, Dealer

console = Console()

class BlackjackUI:
    def __init__(self):
        self.console = console
        import questionary
        from questionary import Style
        
        self.custom_style = Style([
            ('qmark', 'fg:yellow bold'),
            ('question', 'fg:white bold'),
            ('answer', 'fg:green bold'),
            ('pointer', 'fg:green bold'),
            ('highlighted', 'fg:green bold'),
            ('selected', 'fg:green'),
        ])

    def show_start_menu(self, last_backup_name: str = None) -> str:
        """Show the initial start menu."""
        import questionary
        choices = []
        if last_backup_name:
            # Parse username from filename: save-USERNAME-TIMESTAMP
            parts = last_backup_name.split('-')
            if len(parts) >= 3:
                display_name = parts[1]
            else:
                display_name = last_backup_name
            choices.append(f"Continue ({display_name})")
        
        choices.append("New Game")
        
        if last_backup_name:
            choices.append("Load Game")
            
        choices.append("Exit")
        
        self.console.print(" [bold yellow]✦[/bold yellow] [bold](Use arrow keys)[/bold]")
        choice = questionary.select(
            "",
            choices=choices,
            style=self.custom_style,
            use_indicator=False,
            pointer="►",
            qmark="",
            instruction=" "
        ).ask()
        
        if choice and choice.startswith("Continue"):
            return "continue"
        elif choice == "New Game":
            return "new"
        elif choice == "Load Game":
            return "load"
        else:
            return "exit"

    def show_backup_selection(self, backups: list) -> any:
        """Show menu to select a backup file."""
        self.clear_screen()
        self.print_header()
        import questionary
        
        choices = []
        for b in backups:
            name_parts = b.name.split('-')
            # Format: save-USERNAME-TIMESTAMP (e.g., save-Alice-2023-12-23-06-34-29)
            # Legacy: save-TIMESTAMP (e.g., save-1 or save-2023-12-23-...)
            
            if len(name_parts) >= 8: # save + username + 6 date parts
                username = name_parts[1]
                timestamp = "-".join(name_parts[2:])
                display_name = f"{username} ({timestamp})"
            elif len(name_parts) >= 7: # Maybe legacy timestamped? save-2025...
                display_name = f"Unknown ({'-'.join(name_parts[1:])})"
            else:
                display_name = b.name
            
            choices.append(questionary.Choice(title=display_name, value=b))
            
        choices.append(questionary.Choice(title="Back to Menu", value="CANCEL"))
        
        self.console.print(" [bold yellow]✦[/bold yellow] [bold]Select a backup to restore:[/bold]")
        choice = questionary.select(
            "",
            choices=choices,
            style=self.custom_style,
            use_indicator=False,
            pointer="►",
            qmark="",
            instruction=" "
        ).ask()
        
        if choice == "CANCEL":
            return None
        return choice

    def print_header(self, chips: int = None, username: str = None):
        """Display the game title header."""
        self.console.print()
        self.console.print("[bold gold1]♠ ♥ TERMINAL BLACKJACK ♦ ♣[/bold gold1]")
        self.console.print("[dim]─────────────────────────[/dim]")
        
        left_text = f"[dim]{username}[/dim]" if username else "[dim]by Sz[/dim]"
        
        if chips is not None:
            self.console.print(f"{left_text} [dim]• Chips:[/dim] [bold green]${chips}[/bold green]")
        else:
            self.console.print(left_text)
        
        self.console.print()

    def get_card_color(self, card: Card) -> str:
        if card.suit in ['Hearts', 'Diamonds']:
            return "red"
        return "white"

    def render_hidden_card(self, is_last: bool) -> tuple:
        """Render a gothic-style card back for hidden cards."""
        if is_last:
            return (
                "┌─────┐",
                "│░▒▓▒░│",
                "│▓ ╳ ▓│",
                "│░▒▓▒░│",
                "└─────┘"
            )
        else:
            return (
                "┌───",
                "│░▒▓",
                "│▓ ╳",
                "│░▒▓",
                "└───"
            )

    def render_cards_ascii(self, cards: list, hide_second: bool = False) -> Text:
        """Render cards in overlapping ASCII art style."""
        if not cards:
            # Return empty text for empty boards
            return Text("")
        
        lines = ["", "", "", "", ""]
        result = Text()
        
        for i, card in enumerate(cards):
            is_last = (i == len(cards) - 1)
            is_hidden = (i == 1 and hide_second)
            
            if is_hidden:
                back = self.render_hidden_card(is_last)
                for j in range(5):
                    lines[j] += back[j]
            else:
                color = self.get_card_color(card)
                rank = card.rank_symbol
                suit = card.symbol
                
                if is_last:
                    lines[0] += "┌─────┐"
                    lines[1] += f"│{rank:<2}   │"
                    lines[2] += f"│  {suit}  │"
                    lines[3] += f"│   {rank:>2}│"
                    lines[4] += "└─────┘"
                else:
                    lines[0] += "┌───"
                    lines[1] += f"│{rank:<2} "
                    lines[2] += f"│ {suit} "
                    lines[3] += "│   "
                    lines[4] += "└───"
        
        for j, line in enumerate(lines):
            result.append(line + ("\n" if j < 4 else ""), style="bold")
        
        return result

    def build_info_panel(self, player: Player, game_status: str, message: str = "", bet_result: str = "") -> Panel:
        """Build the left info panel with centered suits and bottom status."""
        # Panel width=15, borders=2, so inner=13, but visually center needs adjustment
        inner_width = 11
        
        info_text = Text()
        
        # Center-aligned suits
        suits = "♠ ♥ ♦ ♣"
        info_text.append(suits.center(inner_width) + "\n\n", style="bold white")
        
        # Chips and Bet display
        info_text.append("Chips ", style="dim")
        info_text.append(f"${player.chips}\n", style="bold green")
        
        # Bet display - show +/- on result
        info_text.append("Bet   ", style="dim")
        if bet_result:
            bet_color = "green" if bet_result.startswith("+") else "red"
            info_text.append(f"{bet_result}\n", style=f"bold {bet_color}")
        else:
            info_text.append(f"${player.bet}\n", style="bold yellow")
        
        # Message in middle if present
        if message:
            info_text.append("\n", style="dim")
            msg_centered = message.center(inner_width)
            msg_color = "green" if "Win" in message else ("red" if "Bust" in message or "Lose" in message or "Dealer" in message else "white")
            info_text.append(msg_centered + "\n", style=f"bold {msg_color}")
        
        # Spacer to push status to bottom
        spacer_lines = 4 if message else 6
        info_text.append("\n" * spacer_lines, style="dim")
        
        # Status at bottom, centered
        status_color = {
            "playing": "cyan",
            "betting": "yellow", 
            "dealer_turn": "magenta",
            "finished": "green"
        }.get(game_status, "white")
        
        status_centered = game_status.upper().center(inner_width)
        info_text.append(status_centered, style=f"bold {status_color}")
        
        return Panel(
            info_text,
            title="[bold]BLACKJACK[/bold]",
            border_style="white",
            width=15,
            height=14
        )

    def build_board_panel(self, name: str, cards: list, value, hide_second: bool = False) -> Panel:
        """Build a card board panel."""
        cards_display = self.render_cards_ascii(cards, hide_second)
        
        return Panel(
            cards_display,
            title=f"[bold green]{name}[/bold green] [dim]({value})[/dim]",
            border_style="green",
            width=34,
            height=7,
            padding=(0, 1)
        )

    def build_game_layout(self, player: Player, dealer: Dealer, game_status: str, message: str = "", bet_result: str = "") -> Table:
        """Build the complete game layout."""
        info_panel = self.build_info_panel(player, game_status, message, bet_result)
        
        dealer_val = "?" if game_status == "playing" else str(dealer.hand_value)
        hide_hole = (game_status == "playing")
        dealer_panel = self.build_board_panel("DEALER", dealer.hand, dealer_val, hide_hole)
        
        player_panel = self.build_board_panel(player.name.upper(), player.hand, player.hand_value)
        
        right_grid = Table.grid(padding=0)
        right_grid.add_column()
        right_grid.add_row(dealer_panel)
        right_grid.add_row(player_panel)
        
        main_grid = Table.grid(padding=0)
        main_grid.add_column()
        main_grid.add_column()
        main_grid.add_row(info_panel, right_grid)
        
        return main_grid

    def clear_screen(self):
        """Clear the terminal screen."""
        os.system('cls' if os.name == 'nt' else 'clear')

    def display_table(self, player: Player, dealer: Dealer, game_status: str, message: str = "", bet_result: str = ""):
        """Display the game table with screen clear for clean updates."""
        self.clear_screen()
        layout = self.build_game_layout(player, dealer, game_status, message, bet_result)
        self.console.print(layout)

    def show_main_menu(self) -> str:
        """Show main menu with arrow key navigation."""
        import questionary
        from questionary import Style
        
        custom_style = Style([
            ('qmark', 'fg:yellow bold'),
            ('question', 'fg:white bold'),
            ('answer', 'fg:green bold'),
            ('pointer', 'fg:green bold'),
            ('highlighted', 'fg:green bold'),
            ('selected', 'fg:green'),
        ])
        
        choices = [
            "Play Game",
            "Earn Chips",
            "About Game",
            "Exit"
        ]
        
        self.console.print(" [bold yellow]✦[/bold yellow] [bold](Use arrow keys)[/bold]")
        result = questionary.select(
            "",
            choices=choices,
            style=custom_style,
            use_indicator=False,
            pointer="►",
            qmark="",
            instruction=" "
        ).ask()
        
        if result is None:
            return "exit"
        elif "Play" in result:
            return "play"
        elif "Earn" in result:
            return "earn"
        elif "About" in result:
            return "about"
        else:
            return "exit"

    def get_bet(self, player_chips: int) -> int:
        while True:
            bet_str = Prompt.ask(f"[bold]Bet[/bold] [dim](${player_chips})[/dim]")
            if bet_str.isdigit():
                bet = int(bet_str)
                if 0 < bet <= player_chips:
                    return bet
                self.console.print("[red]Invalid bet.[/red]")
            else:
                self.console.print("[red]Enter a number.[/red]")

    def get_action(self, can_surrender: bool = False) -> str:
        """Get player action using arrow key selection."""
        import questionary
        from questionary import Style
        
        custom_style = Style([
            ('pointer', 'fg:green bold'),
            ('highlighted', 'fg:green bold'),
            ('selected', 'fg:green bold'),
        ])
        
        choices = ["Hit", "Stand"]
        if can_surrender:
            choices.append("Surrender")
        
        self.console.print(" [bold yellow]✦[/bold yellow] [bold]Choose action[/bold]")
        result = questionary.select(
            "",
            choices=choices,
            style=custom_style,
            instruction=" ",
            use_indicator=False,
            pointer="►",
            qmark=""
        ).ask()
        
        if result is None:
            return "s"  # Default to stand on cancel
        elif "Hit" in result:
            return "h"
        elif "Stand" in result:
            return "s"
        elif "Surrender" in result:
            return "u"
        return "s"

    def show_message(self, message: str, style: str = "white"):
        """Show message - kept for compatibility."""
        pass

    def ask_play_again(self, message: str = "Another round?") -> bool:
        """Ask if player wants another round using arrow keys."""
        import questionary
        from questionary import Style
        
        custom_style = Style([
            ('pointer', 'fg:green bold'),
            ('highlighted', 'fg:green bold'),
        ])
        
        self.console.print(f" [bold yellow]✦[/bold yellow] [bold]{message}[/bold]")
        result = questionary.select(
            "",
            choices=["Yes", "No"],
            style=custom_style,
            instruction=" ",
            use_indicator=False,
            pointer="►",
            qmark=""
        ).ask()
        
        return result is not None and "Yes" in result
    
    def show_about_page(self):
        """Display the about page."""
        self.clear_screen()
        # Assuming print_header exists or will be added. If not, this will cause an error.
        # For now, commenting it out to ensure syntactical correctness with the provided document.
        self.print_header() 
        from .about import ABOUT_TEXT, RULES_TEXT
        from rich.panel import Panel
        content = Text()
        
        # About section
        content.append("ABOUT\n", style="bold yellow")
        content.append("────────────────────────────────────────────\n", style="dim")
        content.append(ABOUT_TEXT + "\n\n")
        
        # Rules section
        content.append("RULES (For those who don't know!)\n", style="bold yellow")
        content.append("────────────────────────────────────────────\n", style="dim")
        content.append(RULES_TEXT)
        
        # Create panel with gothic/retro box
        panel = Panel(
            content,
            title="[bold cyan]About & Rules[/bold cyan]",
            border_style="cyan",
            box=box.HEAVY,
            padding=(1, 2)
        )
        
        self.console.print(panel)
        self.console.print()
        
        # Use simple select for back
        import questionary
        from questionary import Style
        
        custom_style = Style([
            ('pointer', 'fg:green bold'),
            ('highlighted', 'fg:green bold'),
        ])
        
        self.console.print(" [bold yellow]✦[/bold yellow] [bold](Use arrow keys)[/bold]")
        questionary.select(
             "",
             choices=["Back to Menu"],
             style=custom_style,
             instruction=" ",
             use_indicator=False,
             pointer="►",
             qmark=""
        ).ask()

    def show_earn_menu(self) -> str:
        """Show the Earn Chips sub-menu."""
        import questionary
        from questionary import Style

        custom_style = Style([
            ('qmark', 'fg:yellow bold'),
            ('question', 'fg:white bold'),
            ('answer', 'fg:green bold'),
            ('pointer', 'fg:green bold'),
        ])

        choices = [
            "General Trivia ($3)",
            "Custom MCQs ($10)",
            "Back to Menu"
        ]

        self.console.print(" [bold yellow]✦[/bold yellow] [bold](Use arrow keys)[/bold]")
        result = questionary.select(
            "",
            choices=choices,
            style=custom_style,
            use_indicator=False,
            pointer="►",
            qmark="",
            instruction=" "
        ).ask()

        if result is None or "Back" in result:
            return "back"
        elif "General" in result:
            return "general"
        elif "Custom" in result:
            return "custom"
        return "back"

    def show_custom_topics_menu(self, topics: list, current_chips: int = None, username: str = None) -> str:
        """Show available custom topics."""
        self.clear_screen()
        self.print_header(current_chips, username)
        import questionary
        from questionary import Style

        custom_style = Style([
            ('pointer', 'fg:green bold'),
        ])

        if not topics:
            return None

        # topics is list of (name, path)
        choices = [f"{t[0]}" for t in topics]
        choices.append("Back to Menu")

        self.console.print(" [bold yellow]✦[/bold yellow] [bold](Use arrow keys)[/bold]")
        result = questionary.select(
            "",
            choices=choices,
            style=custom_style,
            use_indicator=False,
            pointer="►",
            qmark="",
            instruction=" "
        ).ask()

        if result is None or "Back" in result:
            return "back"
        
        # Find path based on selection
        selected_name = result
        for name, path in topics:
            if name == selected_name:
                return path
        return "back"

    def ask_trivia_question(self, question_data: dict, current_chips: int = None, username: str = None) -> object:
        """
        Ask a trivia question. 
        Returns:
            True: Correct
            False: Incorrect
            None: Exit/Back to Menu
        """
        import questionary
        from questionary import Style

        self.clear_screen()
        self.print_header(current_chips, username)

        q_text = question_data["question"]
        options = list(question_data["options"]) # Copy to avoid modifying original
        
        # Add Exit option
        exit_opt = "Back to Menu"
        options.append(exit_opt)
        
        correct_idx = question_data["correct_index"]
        # Ensure index is valid
        if 0 <= correct_idx < len(question_data["options"]):
            correct_answer = question_data["options"][correct_idx]
        else:
            correct_answer = "" # Should not happen with valid data

        custom_style = Style([
            ('qmark', 'fg:yellow bold'),
            ('question', 'fg:cyan bold'),
            ('answer', 'fg:white'),
            ('pointer', 'fg:green bold'),
            ('selected', 'fg:green'),
        ])

        # No bold for question text to keep it readable, but yellow ✦
        self.console.print(f" [bold yellow]✦[/bold yellow] {q_text}")
        answer = questionary.select(
            "",
            choices=options,
            style=custom_style,
            instruction=" ",
            use_indicator=False,
            pointer="►",
            qmark=""
        ).ask()

        if answer is None or answer == exit_opt:
            return None
            
        return answer == correct_answer

    def show_trivia_result(self, is_correct: bool, reward: int):
        """Show result of the question."""
        self.console.print()
        if is_correct:
            self.console.print(f"[bold green]Correct! You earned ${reward}[/bold green]")
        else:
            self.console.print("[bold red]Wrong answer![/bold red]")
        
        import time
        time.sleep(1.5)

