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
        self.ui.clear()
        self.ui.show_message("[bold gold1]Welcome to Blackjack![/bold gold1]", style="blue")
        time.sleep(1)
        name = self.ui.console.input("[bold]Enter your name: [/bold]")
        self.player.name = name if name else "Player"
        
        while True:
            try:
                chips = int(self.ui.console.input("[bold]Enter buy-in amount (chips): [/bold]"))
                if chips > 0:
                    self.player.chips = chips
                    break
            except ValueError:
                pass

    def play_round(self):
        # 1. Place Bet
        self.ui.display_table(self.player, self.dealer, "betting")
        bet = self.ui.get_bet(self.player.chips)
        if not self.player.place_bet(bet):
            self.ui.show_message("Not enough chips!", "red")
            return

        # 2. Deal Initial Cards
        self.player.clear_hand()
        self.dealer.clear_hand()
        
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
                    self.ui.display_table(self.player, self.dealer, "finished", "BUSTED!")
                    self.ui.show_message("You Busted!", "red")
                    self.player.lose_bet()
                    return

            elif action in ['u', 'surrender']:
                # Surrender: Lose half bet
                self.player.chips += (self.player.bet // 2)
                self.player.bet = 0 # Hand over
                self.ui.show_message("Surrendered!", "yellow")
                return # End round immediately
            
            elif action in ['s', 'stand']:
                break
        
        # 5. Dealer Turn
        self.ui.display_table(self.player, self.dealer, "dealer_turn", "Dealer's Turn...")
        time.sleep(1)
        
        while self.dealer.should_hit():
            self.dealer.add_card(self.deck.deal())
            self.ui.display_table(self.player, self.dealer, "dealer_turn")
            time.sleep(1)

        # 6. Resolve
        self.ui.display_table(self.player, self.dealer, "finished")
        
        p_val = self.player.hand_value
        d_val = self.dealer.hand_value
        
        if self.dealer.is_busted:
            self.ui.show_message("Dealer Busted! You Win!", "green")
            self.player.win_bet()
        elif d_val > p_val:
            self.ui.show_message("Dealer Wins!", "red")
            self.player.lose_bet()
        elif d_val < p_val:
            self.ui.show_message("You Win!", "green")
            self.player.win_bet()
        else:
            self.ui.show_message("Push (Tie).", "yellow")
            self.player.push_bet()

    def run(self):
        self.welcome()
        while True:
            if self.player.chips <= 0:
                self.ui.show_message("Game Over! You ran out of chips.", "red")
                break
            
            self.play_round()
            
            if not self.ui.ask_play_again():
                break
        
        self.ui.show_message(f"Thanks for playing! Final Chips: {self.player.chips}", "bold cyan")

