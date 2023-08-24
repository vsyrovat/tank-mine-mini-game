# The Tank game

## Easy demo

- `docker build -t tank-game-demo .`
- `docker run -it --rm tank-game-demo`

To remove image after:
`docker image rm tank-game-demo`

## Developer's guide

- `asdf install`
- `python3 -m venv .venv`
- `source .venv/bin/activate`
- `pip install pipenv`
- `pipenv install`

Now for run tests:
`pytest -v`

For easy demo:
`python main.py`
