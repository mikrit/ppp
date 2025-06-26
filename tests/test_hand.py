import sys
import pathlib
import pytest

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

from engine.card import Card
from engine.hand import evaluate_best_hand, HandRank


def make_cards(*codes):
    return [Card(code) for code in codes]


def test_no_straight_with_pair():
    cards = make_cards('9s', 'Kc', '6s', '7d', 'Th', '7h', '3s')
    rank, _ = evaluate_best_hand(cards)
    assert rank == HandRank.ONE_PAIR


def test_detect_straight():
    cards = make_cards('5s', '6d', '7h', '8c', '9s', '2d', 'Qh')
    rank, aux = evaluate_best_hand(cards)
    assert rank == HandRank.STRAIGHT
    assert aux == [7]


def test_wheel_straight():
    cards = make_cards('As', '2d', '3c', '4h', '5s', 'Kh', 'Qd')
    rank, aux = evaluate_best_hand(cards)
    assert rank == HandRank.STRAIGHT
    assert aux == [3]

def test_two_pair_example():
    """Player with Qd Jh vs board Jd 9d Qh 4c 7h should make two pair"""
    cards = make_cards('Qd', 'Jh', 'Jd', '9d', 'Qh', '4c', '7h')
    rank, aux = evaluate_best_hand(cards)
    assert rank == HandRank.TWO_PAIR
    assert aux == [10, 9, 7]


def test_high_card_example():
    """Opponent with 6c 5h should only have high card"""
    cards = make_cards('6c', '5h', 'Jd', '9d', 'Qh', '4c', '7h')
    rank, aux = evaluate_best_hand(cards)
    assert rank == HandRank.HIGH_CARD
    assert aux == [10, 9, 7, 5, 4]
