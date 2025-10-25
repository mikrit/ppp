from engine.player import Player
from engine.game import Game


def main() -> None:
    player = Player("You")
    bot = Player("Bot")
    game = Game([player, bot])
    game.start_hand()
    game.flop()
    game.turn()
    game.river()

    for p in game.players:
        print(f"{p.name}: {p.hole_cards}")
    print(f"Community: {game.community}")

    winners, rank, _ = game.best_player()
    if len(winners) == 1:
        print(f"Winner: {winners[0].name} with {rank.name}")
    else:
        names = ', '.join(w.name for w in winners)
        print(f"Tie between {names} with {rank.name}")


if __name__ == "__main__":
    main()
