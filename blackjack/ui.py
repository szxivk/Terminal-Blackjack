from rich.console import Console
from rich.layout import Layout
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich.align import Align
from rich.prompt import Prompt
from rich.columns import Columns
from rich import box
import os
import time

from .models.card import Card
from .models.player import Player, Dealer

console = Console()

class BlackjackUI:
    def __init__(self):
        self.console = console

    def clear(self):
        # Cross-platform clear
        os.system('cls' if os.name == 'nt' else 'clear')

    def get_card_color(self, card: Card) -> str:
        if card.suit in ['Hearts', 'Diamonds']:
            return "red"
        return "white"

    def render_card(self, card: Card, hidden: bool = False) -> Panel:
        if hidden:
            content = Text("\n\n  ??  \n\n", justify="center", style="bold blue")
            return Panel(content, width=10, height=7, title="Card", style="bold blue")

        color = self.get_card_color(card)
        rank = card.rank_symbol
        suit = card.symbol
        
        # ASCII Art representation for the card inside a panel
        # Top Left
        top = f"{rank}{suit}"
        # Bottom Right
        bottom = f"{suit}{rank}"
        
        # Center big suit
        center = f"{suit}"

        grid = Table.grid(expand=True)
        grid.add_column(justify="left")
        grid.add_column(justify="center")
        grid.add_column(justify="right")
        
        grid.add_row(f"[{color}]{top}[/{color}]", "", "")
        grid.add_row("", "", "")
        grid.add_row("", f"[{color}]{center}[/{color}]", "")
        grid.add_row("", "", "")
        grid.add_row("", "", f"[{color}]{bottom}[/{color}]")

        return Panel(grid, width=12, height=7, style=f"bold {color}", border_style=f"{color}")

    def display_table(self, player: Player, dealer: Dealer, game_status: str, message: str = ""):
        self.clear()
        
        # Main Layout
        layout = Layout()
        layout.split(
            Layout(name="header", size=3),
            Layout(name="dealer_area", ratio=1),
            Layout(name="info_area", size=3),
            Layout(name="player_area", ratio=1),
            Layout(name="footer", size=5)
        )

        # Header
        layout["header"].update(Panel(Align.center("[bold gold1]TERMINAL BLACKJACK[/bold gold1]"), style="blue"))

        # Dealer Area
        dealer_cards = []
        for i, card in enumerate(dealer.hand):
            # Hide dealer's second card if game is active and not showing yet
            # For simplicity, we'll let the game logic pass a 'reveal' flag, but here we assume
            # dealer.hand[1] is hidden if status is 'playing'
            # ACTUALLY: Easier to let Game Logic handle hiding by passing a dummy card or flag.
            # But standard blackjack: Dealer shows one card up, one down.
            # We'll implement a 'hide_hole_card' logic in the UI render parameter.
            is_hole_card = (i == 1 and game_status == "playing")
            dealer_cards.append(self.render_card(card, hidden=is_hole_card))
        
        dealer_val = "?" if game_status == "playing" else str(dealer.hand_value)
        layout["dealer_area"].update(
            Panel(
                Align.center(Columns(dealer_cards)), 
                title=f"DEALER (Value: {dealer_val})",
                border_style="red"
            )
        )

        # Info Area
        info_text = f"Status: [bold cyan]{game_status.upper()}[/bold cyan] | Bet: [bold green]${player.bet}[/bold green] | Chips: [bold gold1]${player.chips}[/bold gold1]"
        layout["info_area"].update(Align.center(Text.from_markup(info_text), vertical="middle"))

        # Player Area
        player_cards = [self.render_card(c) for c in player.hand]
        layout["player_area"].update(
            Panel(
                Align.center(Columns(player_cards)), 
                title=f"{player.name.upper()} (Value: {player.hand_value})",
                border_style="green"
            )
        )

        # Footer / Messages
        msg_panel = Panel(Align.center(message), title="Messages", style="white")
        layout["footer"].update(msg_panel)

        self.console.print(layout)

    def get_bet(self, player_chips: int) -> int:
        while True:
            bet_str = Prompt.ask(f"[bold]Enter bet amount[/bold] (Chips: [green]{player_chips}[/green])")
            if bet_str.isdigit():
                bet = int(bet_str)
                if 0 < bet <= player_chips:
                    return bet
                self.console.print("[red]Invalid bet amount. check your chips.[/red]")
            else:
                self.console.print("[red]Please enter a valid number.[/red]")

    def get_action(self, can_double: bool = False) -> str:
        options = "[cyan]H[/cyan]it, [cyan]S[/cyan]tand"
        choices_list = ["h", "s", "H", "S"]
        
        if can_double:
            options += ", [cyan]D[/cyan]ouble"
            choices_list.extend(["d", "D"])

        action = Prompt.ask(f"[bold]Action?[/bold] ({options})", choices=choices_list, default="h")
        return action.lower()

    def show_message(self, message: str, style: str = "white"):
        self.console.print(Panel(message, style=style))
        time.sleep(1.5)

    def ask_play_again(self) -> bool:
        ans = Prompt.ask("Play another round?", choices=["y", "n"], default="y")
        return ans.lower() == 'y'
