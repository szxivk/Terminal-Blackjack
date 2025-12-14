from typing import List
from .card import Card

class Player:
    def __init__(self, name: str, chips: int = 0):
        self.name = name
        self.chips = chips
        self.hand: List[Card] = []
        self.bet = 0
        self.is_standing = False

    def add_card(self, card: Card):
        self.hand.append(card)

    def clear_hand(self):
        self.hand = []
        self.is_standing = False

    def place_bet(self, amount: int) -> bool:
        if amount > self.chips:
            return False
        self.bet = amount
        self.chips -= amount
        return True

    def win_bet(self, payout_multiplier: float = 1.0):
        # payout_multiplier 1.0 means even money (get bet back + equal amount)
        # So total return is bet + (bet * multiplier)
        winnings = int(self.bet + (self.bet * payout_multiplier))
        self.chips += winnings
        self.bet = 0
        
    def push_bet(self):
        self.chips += self.bet
        self.bet = 0

    def lose_bet(self):
        self.bet = 0

    @property
    def hand_value(self) -> int:
        value = 0
        aces = 0
        for card in self.hand:
            value += card.value
            if card.rank == 'Ace':
                aces += 1
        
        while value > 21 and aces:
            value -= 10
            aces -= 1
            
        return value
    
    @property
    def is_busted(self) -> bool:
        return self.hand_value > 21

    def __str__(self):
        return f"{self.name} (Chips: {self.chips})"

class Dealer(Player):
    def __init__(self):
        super().__init__("Dealer", 0)

    def should_hit(self) -> bool:
        # Dealer hits on 16 or less, stands on 17
        return self.hand_value < 17
