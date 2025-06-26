from typing import List
from .card import Card


class Player:
    def __init__(self, name: str, chips: int = 0):
        self.name = name
        self.chips = chips
        self.hole_cards: List[Card] = []

    def reset(self) -> None:
        self.hole_cards.clear()

    def receive(self, cards: List[Card]) -> None:
        self.hole_cards.extend(cards)
