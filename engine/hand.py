from enum import Enum
from typing import List, Tuple
from collections import Counter
from itertools import combinations
from .card import Card, Rank, RANK_ORDER


class HandRank(Enum):
    HIGH_CARD = 0
    ONE_PAIR = 1
    TWO_PAIR = 2
    THREE_OF_A_KIND = 3
    STRAIGHT = 4
    FLUSH = 5
    FULL_HOUSE = 6
    FOUR_OF_A_KIND = 7
    STRAIGHT_FLUSH = 8


def _rank_five(cards: List[Card]) -> Tuple[int, List[int]]:
    ranks = sorted([RANK_ORDER[c.rank] for c in cards], reverse=True)
    suits = [c.suit for c in cards]
    counts = Counter(ranks)
    counts_sorted = sorted(counts.items(), key=lambda x: (-x[1], -x[0]))
    ordered_ranks = [r for r, _ in counts_sorted]
    counts_only = [c for _, c in counts_sorted]

    is_flush = len(set(suits)) == 1
    uniq = sorted(set(ranks), reverse=True)
    # check straight
    is_straight = False
    high_straight = None
    if len(uniq) >= 5:
        for i in range(len(uniq) - 4 + 1):
            span = uniq[i:i+5]
            if span[0] - span[-1] == 4:
                is_straight = True
                high_straight = span[0]
                break
    if not is_straight and set([12, 3, 2, 1, 0]).issubset(ranks):
        is_straight = True
        high_straight = 3  # five-high straight

    if is_straight and is_flush:
        return HandRank.STRAIGHT_FLUSH.value, [high_straight]
    if counts_only == [4, 1]:
        return HandRank.FOUR_OF_A_KIND.value, ordered_ranks
    if counts_only == [3, 2]:
        return HandRank.FULL_HOUSE.value, ordered_ranks
    if is_flush:
        return HandRank.FLUSH.value, ranks
    if is_straight:
        return HandRank.STRAIGHT.value, [high_straight]
    if counts_only == [3, 1, 1]:
        return HandRank.THREE_OF_A_KIND.value, ordered_ranks
    if counts_only == [2, 2, 1]:
        return HandRank.TWO_PAIR.value, ordered_ranks
    if counts_only == [2, 1, 1, 1]:
        return HandRank.ONE_PAIR.value, ordered_ranks
    return HandRank.HIGH_CARD.value, ranks


def evaluate_best_hand(cards: List[Card]) -> Tuple[HandRank, List[int]]:
    best = (HandRank.HIGH_CARD.value, [])
    for comb in combinations(cards, 5):
        rank = _rank_five(list(comb))
        if rank > best:
            best = rank
    return HandRank(best[0]), best[1]
