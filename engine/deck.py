from typing import List
import random
from .card import Card, Rank, Suit


class Deck:
    """Standard 52-card deck."""

    def __init__(self) -> None:
        self.cards: List[Card] = [Card(rank.value + suit.value) for suit in Suit for rank in Rank]
        self.shuffle()

    def shuffle(self) -> None:
        random.shuffle(self.cards)

    def deal(self, n: int) -> List[Card]:
        if n > len(self.cards):
            raise ValueError("Not enough cards in the deck")
        dealt = self.cards[:n]
        self.cards = self.cards[n:]
        return dealt
