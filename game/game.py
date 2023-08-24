from enum import Enum
from copy import deepcopy
from itertools import chain


class Unit(Enum):
    NONE = "."
    TANK = "T"


class Field(Enum):
    NONE = "."
    MINE = "M"


UnitMap = list[list[Unit]]
FieldMap = list[list[Field]]


def decode_space(ss: str, enu: Enum) -> list[list[Enum]]:
    return [[enu(c) for c in s.strip()] for s in ss.strip().splitlines()]  # type: ignore


def encode_space(map: list[list[Enum]]) -> str:
    return "\n".join(["".join([cell.value for cell in line]) for line in map])


class Game:
    units: list[list[Unit]] = []
    mines: list[list[Field]] = []
    age = 0
    size = [None, None]

    def __init__(self, units: UnitMap, mines: FieldMap):
        self.units = units
        self.mines = mines
        self.age = 0
        self.size = [len(units[0]) * 2 + len(mines[0]), max(len(units), len(mines))]  # type: ignore
        self.field = self.generate_field(self.size[0], self.size[1])
        self.mines_offset = len(units[0])
        self.winline_offset = self.mines_offset + len(mines[0])

    def generate_field(self, w, h):
        return [[None for _ in range(w)] for _ in range(h)]

    def info(self):
        return {"size": self.size}

    def state(self):
        return [self.units, self.mines]

    def is_finished(self):
        alive_units = list(filter(lambda u: u != Unit.NONE, chain(*self.units)))
        return self.age >= self.winline_offset or len(alive_units) == 0

    def is_won(self):
        alive_tanks = list(filter(lambda u: u == Unit.TANK, chain(*self.units)))
        return self.is_finished() and len(alive_tanks) >= 2

    def drawmap(self) -> str:
        field = deepcopy(self.field)

        for j in range(len(self.mines)):
            line = self.mines[j]
            for i in range(len(line)):
                field[j][i + self.mines_offset] = line[i]

        for j in range(len(self.units)):
            line = self.units[j]  # type: ignore
            for i in range(len(line)):
                field[j][i + self.age] = line[i]

        def encode(x):
            return x.value if x else "."

        return "\n".join(["".join([encode(cell) for cell in line]) for line in field])

    def step(self):
        self.age += 1
        for j in range(len(self.units)):
            unit_line = self.units[j]
            for i in range(len(unit_line)):
                unit_cell = self.units[j][i]
                mi = i - len(unit_line) + self.age
                if mi >= 0 and mi < len(self.mines[j]):
                    mine_cell = self.mines[j][mi]
                    match (unit_cell, mine_cell):
                        case (Unit.TANK, Field.MINE):
                            self.units[j][i] = Unit.NONE
                            self.mines[j][mi] = Field.NONE

    def play(self):
        while not self.is_finished():
            self.step()
