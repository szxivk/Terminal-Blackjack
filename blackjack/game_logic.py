from .models.card import Deck
from .models.player import Player, Dealer
from .ui import BlackjackUI
from . import storage
import time
import getpass
import os
import random

# Funny welcome messages for new players
NEW_PLAYER_MESSAGES = [
    "🎰 Fresh meat! Here's $500 to lose... I mean, to WIN!",
    "🃏 A new challenger! Take these $500 chips and try not to cry.",
    "♠️ Welcome, rookie! $500 on the house. Don't spend it all in one bet!",
    "🎲 Ah, new blood! Here's $500. The house always wins... eventually.",
    "💰 First time? How cute. Take $500 and learn the hard way!",
]

class BlackjackGame:
    def __init__(self):
        self.ui = BlackjackUI()
        self.deck = Deck(num_decks=6)
        self.player = Player("Player")
        self.dealer = Dealer()

    def get_system_username(self) -> str:
        """Get the system username."""
        try:
            return getpass.getuser()
        except Exception:
            return os.environ.get('USER', os.environ.get('USERNAME', 'Player'))
    
    def show_title(self):
        """Display the game title."""
        self.ui.console.print()
        self.ui.console.print("[bold gold1]♠ ♥ TERMINAL BLACKJACK ♦ ♣[/bold gold1]")
        self.ui.console.print("[dim]─────────────────────────[/dim]")
        self.ui.console.print("[dim]by Sz[/dim]")
        self.ui.console.print()

    def welcome(self):
        self.ui.clear_screen()
        self.show_title()
        
        # Get system username
        system_user = self.get_system_username()
        
        # Check chips for preview
        preview_chips = storage.load_player(system_user)
        if preview_chips is not None:
            chips_display = f"[dim][[/dim][bold yellow]${preview_chips}[/bold yellow][dim]][/dim]"
        else:
            chips_display = "[dim][New][/dim]"
        
        # Ask for name - show detected username with chips
        self.ui.console.print(f"[dim]Player:[/dim] [bold cyan]{system_user}[/bold cyan] {chips_display}")
        custom_name = self.ui.console.input("[bold]Your name[/bold] [dim](Enter to use above)[/dim]: ")
        
        player_name = custom_name.strip() if custom_name.strip() else system_user
        self.player.name = player_name
        
        # Check if player exists and load chips (no welcome message yet)
        saved_chips = storage.load_player(player_name)
        
        if saved_chips is not None:
            # Returning player
            self.player.chips = saved_chips
        else:
            # New player - give 500 chips
            self.player.chips = 500
            storage.save_player(player_name, 500)

    def save_progress(self):
        """Save player's current chips."""
        storage.save_player(self.player.name, self.player.chips)

    def play_round(self):
        # Clear hands first so boards are empty at betting time
        self.player.clear_hand()
        self.dealer.clear_hand()
        
        # 1. Place Bet
        self.ui.display_table(self.player, self.dealer, "betting")
        bet = self.ui.get_bet(self.player.chips)
        if not self.player.place_bet(bet):
            self.ui.show_message("Not enough chips!", "red")
            return

        # 2. Deal Initial Cards
        self.player.add_card(self.deck.deal())
        self.dealer.add_card(self.deck.deal())
        self.player.add_card(self.deck.deal())
        self.dealer.add_card(self.deck.deal())

        # 3. Check Natural Blackjack
        p_val = self.player.hand_value
        
        if p_val == 21:
            pass  # Let player stand with 21

        # 4. Player Turn
        first_action = True
        while not self.player.is_busted:
            self.ui.display_table(self.player, self.dealer, "playing")
            
            action = self.ui.get_action(can_surrender=first_action)
            first_action = False
            
            if action in ['h', 'hit']:
                self.player.add_card(self.deck.deal())
                if self.player.is_busted:
                    bet_amount = self.player.bet
                    self.player.lose_bet()
                    self.ui.display_table(self.player, self.dealer, "finished", "BUSTED!", f"-${bet_amount}")
                    self.save_progress()
                    time.sleep(1.5)
                    return

            elif action in ['u', 'surrender']:
                half_bet = self.player.bet // 2
                self.player.chips += half_bet
                self.player.bet = 0
                self.ui.display_table(self.player, self.dealer, "finished", "Surrendered", f"-${half_bet}")
                self.save_progress()
                time.sleep(1.5)
                return
            
            elif action in ['s', 'stand']:
                break
        
        # 5. Dealer Turn
        self.ui.display_table(self.player, self.dealer, "dealer_turn", "Dealer...")
        time.sleep(0.5)
        
        while self.dealer.should_hit():
            self.dealer.add_card(self.deck.deal())
            self.ui.display_table(self.player, self.dealer, "dealer_turn")
            time.sleep(0.5)

        # 6. Resolve
        p_val = self.player.hand_value
        d_val = self.dealer.hand_value
        bet_amount = self.player.bet
        
        if self.dealer.is_busted:
            self.player.win_bet()
            self.ui.display_table(self.player, self.dealer, "finished", "You Win!", f"+${bet_amount}")
        elif d_val > p_val:
            self.player.lose_bet()
            self.ui.display_table(self.player, self.dealer, "finished", "Dealer Wins", f"-${bet_amount}")
        elif d_val < p_val:
            self.player.win_bet()
            self.ui.display_table(self.player, self.dealer, "finished", "You Win!", f"+${bet_amount}")
        else:
            self.player.push_bet()
            self.ui.display_table(self.player, self.dealer, "finished", "Push (Tie)", "$0")
        
        # Save after each round
        self.save_progress()
        time.sleep(1.5)

    def run(self):
        self.welcome()
        
        while True:
            # Clear and show title before menu
            self.ui.clear_screen()
            self.show_title()
            
            # Show main menu
            choice = self.ui.show_main_menu()
            
            if choice == "play":
                # Show welcome message when starting game
                saved_chips = storage.load_player(self.player.name)
                is_returning = saved_chips is not None and saved_chips > 0
                
                if is_returning:
                    self.ui.console.print()
                    self.ui.console.print(f"[bold green]You shouldn't be gambling, {self.player.name}![/bold green]")
                    time.sleep(1)
                
                self.play_game_loop()
            elif choice == "earn":
                self.ui.console.print("\n[bold yellow]💰 Earn Chips - Coming Soon![/bold yellow]")
                self.ui.console.print("[dim]Watch ads, complete challenges, and more...[/dim]")
                time.sleep(2)
            elif choice == "about":
                self.ui.show_about_page()
            else:  # exit
                break
        
        self.ui.clear_screen()
        self.ui.console.print(f"[bold cyan]Thanks for playing, {self.player.name}![/bold cyan]")
        self.ui.console.print(f"[dim]Your chips saved:[/dim] [bold yellow]${self.player.chips}[/bold yellow]")

    def play_game_loop(self):
        """Main game loop for playing rounds."""
        first_round = True
        
        while True:
            if self.player.chips <= 0:
                self.ui.clear_screen()
                self.ui.console.print("[bold red]Game Over! You ran out of chips.[/bold red]")
                self.ui.console.print("[dim]Come back tomorrow for a fresh $500![/dim]")
                self.save_progress()
                time.sleep(2)
                break
            
            self.play_round()
            first_round = False
            
            if not self.ui.ask_play_again():
                break

