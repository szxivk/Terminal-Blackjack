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
            "► Play Game",
            "► Earn Chips",
            "► About Game",
            "► Exit"
        ]
        
        result = questionary.select(
            "Select an option:",
            choices=choices,
            style=custom_style,
            instruction="(↑↓ to move, Enter to select)"
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
        
        choices = ["► Hit", "► Stand"]
        if can_surrender:
            choices.append("► Surrender")
        
        result = questionary.select(
            "Your move:",
            choices=choices,
            style=custom_style,
            instruction="(↑↓ Enter)"
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

    def ask_play_again(self) -> bool:
        """Ask if player wants another round using arrow keys."""
        import questionary
        from questionary import Style
        
        custom_style = Style([
            ('pointer', 'fg:green bold'),
            ('highlighted', 'fg:green bold'),
        ])
        
        result = questionary.select(
            "Another round?",
            choices=["► Yes", "► No"],
            style=custom_style,
            instruction="(↑↓ Enter)"
        ).ask()
        
        return result is not None and "Yes" in result
    
    def show_about_page(self):
        """Display About & Rules page."""
        from .about import ABOUT_TEXT, RULES_TEXT
        
        self.clear_screen()
        
        # Title
        self.console.print()
        self.console.print("[bold gold1]♠ ♥ TERMINAL BLACKJACK ♦ ♣[/bold gold1]")
        self.console.print("[dim]─────────────────────────[/dim]")
        self.console.print("[dim]by Sz[/dim]")
        self.console.print()
        
        # Page title
        self.console.print("[bold cyan]═══════════════ About & Rules ═══════════════[/bold cyan]")
        self.console.print()
        
        # About section
        self.console.print("[bold yellow]ABOUT[/bold yellow]")
        self.console.print("[dim]────────────────────────────────────────────[/dim]")
        self.console.print(ABOUT_TEXT)
        self.console.print()
        
        # Rules section
        self.console.print("[bold yellow]RULES (For those who don't know!)[/bold yellow]")
        self.console.print("[dim]────────────────────────────────────────────[/dim]")
        self.console.print(RULES_TEXT)
        self.console.print()
        self.console.print("[dim]Press Enter to return to menu...[/dim]")
        input()
