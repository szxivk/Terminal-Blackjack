
import pytest
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from blackjack.models.card import Card, Deck
from blackjack.models.player import Player, Dealer

# Tests for Card
def test_card_values():
    """Test that cards have correct values."""
    assert Card('Two', 'Hearts').value == 2
    assert Card('Ten', 'Spades').value == 10
    assert Card('King', 'Diamonds').value == 10
    assert Card('Ace', 'Clubs').value == 11

def test_card_str():
    """Test string representation."""
    card = Card('Ace', 'Spades')
    assert str(card) == "Ace of Spades"

# Tests for Deck
def test_deck_initialization():
    """Test deck creation and size."""
    deck = Deck(num_decks=1)
    assert len(deck) == 52
    
    deck6 = Deck(num_decks=6)
    assert len(deck6) == 52 * 6

def test_deal():
    """Test dealing reduces deck size."""
    deck = Deck(num_decks=1)
    card = deck.deal()
    assert isinstance(card, Card)
    assert len(deck) == 51

def test_auto_reshuffle():
    """Test deck reshuffles when empty."""
    deck = Deck(num_decks=1)
    deck.cards = [] # Force empty
    card = deck.deal()
    assert card is not None
    assert len(deck) == 51 # 52 - 1

# Tests for Player
@pytest.fixture
def player():
    return Player("TestPlayer", chips=100)

def test_betting_success(player):
    """Test placing a valid bet."""
    result = player.place_bet(50)
    assert result is True
    assert player.chips == 50
    assert player.bet == 50

def test_betting_fail(player):
    """Test betting more than available chips."""
    result = player.place_bet(150)
    assert result is False
    assert player.chips == 100
    assert player.bet == 0

def test_hand_value_hard(player):
    """Test simple hard totals."""
    player.add_card(Card('Ten', 'Spades'))
    player.add_card(Card('Seven', 'Hearts'))
    assert player.hand_value == 17
    assert not player.is_busted

def test_hand_value_soft_ace(player):
    """Test Ace being 11."""
    player.add_card(Card('Ace', 'Spades')) # 11
    player.add_card(Card('Eight', 'Hearts')) # 8
    assert player.hand_value == 19

def test_hand_value_ace_reduction(player):
    """Test Ace reducing to 1 to prevent bust."""
    player.add_card(Card('Ace', 'Spades')) # 11
    player.add_card(Card('King', 'Hearts')) # 10
    player.add_card(Card('Five', 'Clubs')) # 5 -> Total 26 -> Ace becomes 1 -> Total 16
    
    assert player.hand_value == 16
    assert not player.is_busted

def test_multiple_aces(player):
    """Test multiple aces reducing correctly."""
    player.add_card(Card('Ace', 'Spades'))
    player.add_card(Card('Ace', 'Hearts'))
    # 11 + 11 = 22 -> one ace becomes 1 -> 12
    assert player.hand_value == 12

def test_bust(player):
    """Test busting logic."""
    player.add_card(Card('King', 'Spades'))
    player.add_card(Card('Queen', 'Hearts'))
    player.add_card(Card('Five', 'Clubs'))
    assert player.hand_value == 25
    assert player.is_busted

def test_win_bet(player):
    """Test winning adds chips correctly."""
    player.place_bet(50)
    player.win_bet(1.0) # Standard 1:1 win
    assert player.chips == 150 # 50 (left) + 50 (bet) + 50 (win) = 150

def test_blackjack_payout(player):
    """Test blackjack payout (usually 1.5)."""
    player.place_bet(10) # 90 left
    player.win_bet(1.5)
    # 90 + 10 (bet) + 15 (win) = 115
    assert player.chips == 115

# Tests for Dealer
@pytest.fixture
def dealer():
    return Dealer()

def test_should_hit(dealer):
    """Test dealer hit logic (<17)."""
    dealer.add_card(Card('Ten', 'Spades'))
    dealer.add_card(Card('Six', 'Hearts')) # 16
    assert dealer.should_hit()

def test_should_stand(dealer):
    """Test dealer stand logic (>=17)."""
    dealer.add_card(Card('Ten', 'Spades'))
    dealer.add_card(Card('Seven', 'Hearts')) # 17
    assert not dealer.should_hit()
