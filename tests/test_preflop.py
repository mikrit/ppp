import sys
import pathlib

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

from engine.card import Card
from engine.preflop import canonical


def make(card1: str, card2: str):
    return [Card(card1), Card(card2)]


def test_canonical_pair():
    assert canonical(make('As', 'Ah')) == 'AA'


def test_canonical_suited():
    assert canonical(make('Ah', 'Kh')) == 'AKs'


def test_canonical_offsuit():
    assert canonical(make('As', 'Kd')) == 'AKo'
