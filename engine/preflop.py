from typing import List, Set
from .card import Card, RANK_ORDER

POSITIONS = ["UTG", "MP", "HJ", "CO", "BTN"]


def canonical(cards: List[Card]) -> str:
    if len(cards) != 2:
        raise ValueError("need two cards")
    c1, c2 = sorted(cards, reverse=True)
    if c1.rank == c2.rank:
        return c1.rank.value + c2.rank.value
    suited = 's' if c1.suit == c2.suit else 'o'
    return f"{c1.rank.value}{c2.rank.value}{suited}"


def combo_count(code: str) -> int:
    if len(code) == 2:
        return 6
    return 4 if code.endswith('s') else 12


def range_percent(hand_set: Set[str]) -> float:
    combos = sum(combo_count(c) for c in hand_set)
    return combos / 1326 * 100


OPEN_RANGES = {
    "UTG": {
        "AA", "KK", "QQ", "JJ", "TT",
        "AKs", "AKo", "AQs", "AJs", "KQs",
    },
    "MP": {
        "AA", "KK", "QQ", "JJ", "TT", "99",
        "AKs", "AKo", "AQs", "AJs", "KQs", "AQo", "KJs",
    },
    "HJ": {
        "AA", "KK", "QQ", "JJ", "TT", "99", "88", "77",
        "AKs", "AKo", "AQs", "AJs", "KQs", "AQo", "ATs",
        "KJs", "QJs", "JTs",
    },
    "CO": {
        "AA", "KK", "QQ", "JJ", "TT", "99", "88", "77", "66", "55",
        "AKs", "AKo", "AQs", "AJs", "KQs", "AQo", "ATs", "KJs", "QJs", "JTs",
        "AJo", "KTs", "QTs", "T9s",
    },
    "BTN": {
        "AA", "KK", "QQ", "JJ", "TT", "99", "88", "77", "66", "55", "44", "33", "22",
        "AKs", "AKo", "AQs", "AJs", "KQs", "AQo", "ATs", "KJs", "QJs", "JTs", "AJo",
        "KTs", "QTs", "J9s", "T9s", "98s", "87s", "76s",
        "A9s", "A8s", "A7s", "A6s", "A5s", "A4s", "A3s", "A2s",
        "A9o", "KJo", "QJo",
    },
}

THREEBET_RANGES = {
    pos: {
        "AA", "KK", "QQ", "JJ", "AKs", "AKo", "AQs"
    } for pos in POSITIONS
}

CALL_RANGES = {
    pos: {
        "TT", "99", "88", "77", "AJs", "AQo", "KQs"
    } for pos in POSITIONS
}


def recommended_action(position: str, cards: List[Card], previous_actions: List[str]) -> str:
    canon = canonical(cards)
    raise_count = previous_actions.count('raise') + previous_actions.count('reraise')
    if raise_count == 0:
        return 'raise' if canon in OPEN_RANGES[position] else 'fold'
    elif raise_count == 1:
        if canon in THREEBET_RANGES[position]:
            return 'reraise'
        if canon in CALL_RANGES[position]:
            return 'call'
        return 'fold'
    else:
        return 'reraise' if canon in {"AA", "KK", "QQ", "AKs", "AKo"} else 'fold'

