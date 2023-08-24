from game.game import Game, Unit, Field, encode_space, decode_space


# fmt: off
def test_encode_space():
    assert encode_space([[Unit.NONE, Unit.TANK],
                         [Unit.TANK, Unit.NONE]]) == ".T\nT."


def test_decode_space():
    assert decode_space("\n.T\n", Unit) == [[Unit.NONE, Unit.TANK]]
    assert decode_space(""".T
                           T.""", Unit) == \
        [[Unit.NONE, Unit.TANK],
         [Unit.TANK, Unit.NONE]]
# fmt: on


def test_game1():
    game = Game(decode_space("T", Unit), decode_space(".", Field))
    assert game.info() == {"size": [3, 1]}
    assert game.drawmap() == "T.."
    assert not game.is_finished()
    assert not game.is_won()

    game.step()
    assert game.drawmap() == ".T."
    assert not game.is_finished()
    assert not game.is_won()

    game.step()
    assert game.drawmap() == "..T"
    assert game.is_finished()
    assert not game.is_won()  # two+ alive tanks required


def test_game2():
    game = Game(decode_space("T", Unit), decode_space("M", Field))
    assert game.info() == {"size": [3, 1]}
    assert game.drawmap() == "TM."
    assert not game.is_finished()

    game.step()
    assert game.drawmap() == "..."
    assert game.is_finished()
    assert not game.is_won()  # the tank has been destroyed


def test_game3():
    game = Game(decode_space("TT", Unit), decode_space(".", Field))
    assert game.info() == {"size": [5, 1]}
    assert game.drawmap() == "TT..."

    game.step()
    assert game.drawmap() == ".TT.."
    assert not game.is_finished()

    game.step()
    assert game.drawmap() == "..TT."
    assert not game.is_finished()

    game.step()
    assert game.drawmap() == "...TT"
    assert game.is_finished()
    assert game.is_won()


def test_game4():
    game = Game(decode_space("TT", Unit), decode_space("M", Field))
    assert game.info() == {"size": [5, 1]}
    assert game.drawmap() == "TTM.."

    game.step()
    assert game.drawmap() == ".T..."
    assert not game.is_finished()

    game.step()
    game.step()
    game.step()
    assert game.is_finished()
    assert not game.is_won()


# fmt: off
def test_game():
    game = Game(
        decode_space("""T.T.TT
                        .T.T..
                        ...T..""", Unit),
        decode_space("""M..M
                        .MM.
                        .MMM""", Field)
    )
    assert game.info() == {"size": [16, 3]}
    assert game.drawmap() == "T.T.TTM..M......\n" + \
                             ".T.T...MM.......\n" + \
                             "...T...MMM......"

    game.play()

    assert game.drawmap() == "..........T.T...\n" + \
                             "................\n" + \
                             "........MM......"
    assert game.is_won()
# fmt: on
