from typing import List, Tuple

from .deck import Deck
from .player import Player
from .card import Card
from .hand import evaluate_best_hand, HandRank


class Game:
    def __init__(self, players: List[Player]):
        if len(players) < 2:
            raise ValueError("Need at least two players")
        self.players = players
        self.deck = Deck()
        self.community: List[Card] = []

    def start_hand(self) -> None:
        self.deck = Deck()
        self.community.clear()
        for p in self.players:
            p.reset()
            p.receive(self.deck.deal(2))

    def flop(self) -> None:
        self.community.extend(self.deck.deal(3))

    def turn(self) -> None:
        self.community.extend(self.deck.deal(1))

    def river(self) -> None:
        self.community.extend(self.deck.deal(1))

    def best_player(self) -> Tuple[List[Player], HandRank, List[int]]:
        scored = []
        for p in self.players:
            rank = evaluate_best_hand(p.hole_cards + self.community)
            scored.append((rank, p))

        best_rank, _ = max(scored, key=lambda x: (x[0][0].value, x[0][1]))
        winners = [p for r, p in scored if r == best_rank]
        return winners, best_rank[0], best_rank[1]
