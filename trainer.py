import random
from typing import List, Tuple

from engine.deck import Deck
from engine.card import Card
from engine.preflop import (
    POSITIONS,
    OPEN_RANGES,
    THREEBET_RANGES,
    CALL_RANGES,
    range_percent,
    recommended_action,
)


def display_scenario(pos: str, cards: List[Card], actions: List[Tuple[str, str]]):
    print(f"Ваша позиция: {pos}")
    print(f"Ваши карты: {cards}")
    if actions:
        print("Действия до вас:")
        for p, a in actions:
            print(f"  {p}: {a}")
    else:
        print("Все сбросили до вас")


def play_round() -> None:
    deck = Deck()
    hero_index = random.randint(0, len(POSITIONS) - 1)
    hero_pos = POSITIONS[hero_index]
    hero_cards = deck.deal(2)

    actions: List[Tuple[str, str]] = []
    raise_count = 0
    for pos in POSITIONS[:hero_index]:
        if raise_count == 0:
            act = random.choice(['fold', 'limp', 'raise'])
        elif raise_count == 1:
            act = random.choice(['fold', 'call', 'reraise'])
        else:
            act = 'fold'
        if act in ('raise', 'reraise'):
            raise_count += 1
        actions.append((pos, act))

    display_scenario(hero_pos, hero_cards, actions)
    hero_action = input('Ваш ход? (fold/call/raise/reraise): ').strip().lower()

    rec = recommended_action(hero_pos, hero_cards, [a for _, a in actions])
    if hero_action == rec:
        print('Правильно!')
    else:
        print(f'Неверно. Следовало {rec}.')

    if rec == 'raise' and raise_count == 0:
        rng = OPEN_RANGES[hero_pos]
    elif rec == 'reraise':
        rng = THREEBET_RANGES[hero_pos]
    elif rec == 'call':
        rng = CALL_RANGES[hero_pos]
    else:
        rng = set()
    if rng:
        percent = range_percent(rng)
        print(f'Рекомендуемый диапазон {rec}: {sorted(rng)}')
        print(f'Процент: {percent:.1f}%')


if __name__ == "__main__":
    play_round()
