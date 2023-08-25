# The Tank game

## Easy demo

- `docker build -t tank-game-demo .`
- `docker run -it --rm tank-game-demo`

You will see something like that:

```bash
Beforeplay field:
T.T.TTM..M......
.T.T...MM.......
...T...MMM......

Now play...

Is game finished? True
Is game won? True
Afterplay field:
..........T.T...
................
........MM......
```

To remove image after:
`docker image rm tank-game-demo`


## The game principles

Tanks represented by the "T" char and mines represented by the "M" char.
Tanks moves from left to the right. When tank moves onto mine - they mutually destroys.
If two tanks remain alive after moving through the minefield - the game is won.

In the example the battlefield consist of three parts:

1. The tanks disposition:

```bash
T.T.TT
.T.T..
...T..
```

2. The minefield:

```bash
M..M
.MM.
.MMM
```

3. And the third part is the place where the tanks should be placed after moving through the minefield.
It is empty so represented only with dots.

```bash
......
......
......
```

The game consist of steps, with each step the tanks moving on one positition to the right.
If tank moves onto a mine - they both destroys and this battlefield cell becomes a dot.
(Of course IRL killed tank not dissappears trom it's death place, but this game is just dumb simulator of something).

## Developer's guide

- `python3 -m venv .venv`
- `source .venv/bin/activate`
- `pip install pipenv`
- `pipenv install`

Now for run tests:
`pytest -v`

For easy demo:
`python main.py`
