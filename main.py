from game.game import Game, decode_space, Unit, Field


def main():
    # fmt: off
    tanks = "T.T.TT\n" +\
            ".T.T..\n" +\
            "...T.."
    mines = "M..M\n" +\
            ".MM.\n" +\
            ".MMM"
    # fmt: on
    game = Game(decode_space(tanks, Unit), decode_space(mines, Field))

    print("Beforeplay field:")
    print(game.drawmap())
    print("Now play...")
    game.play()
    print("Is game finished?", game.is_finished())
    print("Is game won?", game.is_won())
    print("Afterplay field:")
    print(game.drawmap())


main()
