# engine/card.py

from enum import Enum


class Suit(Enum):
    CLUBS = 'c'
    DIAMONDS = 'd'
    HEARTS = 'h'
    SPADES = 's'

    def symbol(self):
        return {
            'c': '♣',
            'd': '♦',
            'h': '♥',
            's': '♠',
        }[self.value]


class Rank(Enum):
    TWO = '2'
    THREE = '3'
    FOUR = '4'
    FIVE = '5'
    SIX = '6'
    SEVEN = '7'
    EIGHT = '8'
    NINE = '9'
    TEN = 'T'
    JACK = 'J'
    QUEEN = 'Q'
    KING = 'K'
    ACE = 'A'


RANK_MAP = {r.value: r for r in Rank}
SUIT_MAP = {s.value: s for s in Suit}
RANK_ORDER = {r: i for i, r in enumerate(Rank)}


class Card:
    def __init__(self, card_str: str):
        if len(card_str) != 2:
            raise ValueError("Card string must be two characters (e.g., 'As', 'Td')")
        rank_char = card_str[0].upper()
        suit_char = card_str[1].lower()

        if rank_char not in RANK_MAP or suit_char not in SUIT_MAP:
            raise ValueError(f"Invalid card string: {card_str}")

        self.rank = RANK_MAP[rank_char]
        self.suit = SUIT_MAP[suit_char]

    def __repr__(self):
        return f"{self.rank.value}{self.suit.symbol()}"

    def __lt__(self, other):
        return RANK_ORDER[self.rank] < RANK_ORDER[other.rank]

    def __eq__(self, other):
        return self.rank == other.rank and self.suit == other.suit
