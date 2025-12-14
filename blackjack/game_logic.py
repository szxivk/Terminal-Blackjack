from .models.card import Deck
from .models.player import Player, Dealer
from .ui import BlackjackUI
import time

class BlackjackGame:
    def __init__(self):
        self.ui = BlackjackUI()
        self.deck = Deck(num_decks=6) # Standard casino shoe
        self.player = Player("Player") # Name will be set later
        self.dealer = Dealer()

    def welcome(self):
        self.ui.console.print()
        self.ui.console.print("[bold gold1]♠ ♥ TERMINAL BLACKJACK ♦ ♣[/bold gold1]")
        self.ui.console.print()
        name = self.ui.console.input("[bold]Your name: [/bold]")
        self.player.name = name if name else "Player"
        
        while True:
            try:
                chips = int(self.ui.console.input("[bold]Buy-in chips: [/bold]"))
                if chips > 0:
                    self.player.chips = chips
                    break
            except ValueError:
                pass


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
        d_val = self.dealer.hand_value
        
        # Check dealer peek (if needed, simplified here)
        
        if p_val == 21:
             # Just show table, no auto-win (game continues unless logic dictates otherwise, but 21 usually means wait for dealer)
             # Actually, if player has 21, they can stand. Let's let them play (stand basically).
             pass

        # 4. Player Turn
        first_action = True
        while not self.player.is_busted:
            self.ui.display_table(self.player, self.dealer, "playing")
            
            # Simple Hit or Stand
            action = self.ui.get_action(can_surrender=first_action)
            first_action = False
            
            if action in ['h', 'hit']:
                self.player.add_card(self.deck.deal())
                if self.player.is_busted:
                    bet_amount = self.player.bet
                    self.player.lose_bet()
                    self.ui.display_table(self.player, self.dealer, "finished", "BUSTED!", f"-${bet_amount}")
                    time.sleep(1.5)
                    return

            elif action in ['u', 'surrender']:
                # Surrender: Lose half bet
                half_bet = self.player.bet // 2
                self.player.chips += half_bet
                self.player.bet = 0
                self.ui.display_table(self.player, self.dealer, "finished", "Surrendered", f"-${half_bet}")
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
        
        time.sleep(1.5)

    def run(self):
        self.welcome()
        while True:
            if self.player.chips <= 0:
                self.ui.clear_screen()
                self.ui.console.print("[bold red]Game Over! You ran out of chips.[/bold red]")
                break
            
            self.play_round()
            
            if not self.ui.ask_play_again():
                break
        
        self.ui.clear_screen()
        self.ui.console.print(f"[bold cyan]Thanks for playing! Final Chips: ${self.player.chips}[/bold cyan]")

