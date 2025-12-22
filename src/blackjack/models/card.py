import random
from typing import List, Optional

SUITS = ['Spades', 'Diamonds', 'Clubs', 'Hearts']
RANKS = ['Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace']
VALUES = {
    'Two': 2, 'Three': 3, 'Four': 4, 'Five': 5, 'Six': 6, 'Seven': 7, 'Eight': 8, 'Nine': 9, 'Ten': 10,
    'Jack': 10, 'Queen': 10, 'King': 10, 'Ace': 11
}
SUIT_SYMBOLS = {'Spades': '♠', 'Diamonds': '♦', 'Clubs': '♣', 'Hearts': '♥'}
RANK_SYMBOLS = {
    'Two': '2', 'Three': '3', 'Four': '4', 'Five': '5', 'Six': '6', 'Seven': '7', 'Eight': '8', 'Nine': '9', 'Ten': '10',
    'Jack': 'J', 'Queen': 'Q', 'King': 'K', 'Ace': 'A'
}

class Card:
    def __init__(self, rank: str, suit: str):
        self.rank = rank
        self.suit = suit
        self.value = VALUES[rank]
        self.symbol = SUIT_SYMBOLS[suit]
        self.rank_symbol = RANK_SYMBOLS[rank]

    def __str__(self):
        return f"{self.rank} of {self.suit}"

    def __repr__(self):
        return f"Card({self.rank}, {self.suit})"

class Deck:
    def __init__(self, num_decks: int = 1):
        self.num_decks = num_decks
        self.cards: List[Card] = []
        self.create_deck()

    def create_deck(self):
        self.cards = []
        for _ in range(self.num_decks):
            for suit in SUITS:
                for rank in RANKS:
                    self.cards.append(Card(rank, suit))
        self.shuffle()

    def shuffle(self):
        random.shuffle(self.cards)

    def deal(self) -> Optional[Card]:
        if not self.cards:
            # Auto-reshuffle if deck is empty (simple rule)
            self.create_deck()
        return self.cards.pop() if self.cards else None

    def __len__(self):
        return len(self.cards)
