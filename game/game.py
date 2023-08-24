from enum import Enum
from copy import deepcopy
from itertools import chain
import numpy as np


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
    units = None
    mines = None
    age = None
    size = [None, None]

    def __init__(self, units: UnitMap, mines: FieldMap):
        self.units = np.array(units)
        self.mines = np.array(mines)
        self.age = 0
        self.size = [len(units[0]) * 2 + len(mines[0]), max(len(units), len(mines))]  # type: ignore
        self.board = self.generate_board()
        self.mines_offset = len(units[0])
        self.winline_offset = self.mines_offset + len(mines[0])

    def generate_board(self):
        return np.full((self.size[1], self.size[0]), None, dtype=object)

    def info(self):
        return {"size": self.size}

    def is_finished(self):
        alive_units = np.any(self.units != Unit.NONE)
        return self.age >= self.winline_offset or not alive_units

    def is_won(self):
        alive_tanks = np.sum(self.units == Unit.TANK)
        return self.is_finished() and alive_tanks >= 2

    def drawmap(self):
        field = np.copy(self.board)

        for j, line in enumerate(self.mines):
            field[j, self.mines_offset : self.mines_offset + len(line)] = line

        field[: len(self.units), self.age : self.age + len(self.units[0])] = self.units

        encode = np.vectorize(lambda x: x.value if x else ".")
        encoded_field = encode(field)

        return "\n".join([f"{''.join(line)}" for line in encoded_field])

    def step(self):
        self.age += 1
        for j in range(len(self.units)):
            for i in range(len(self.units[0])):
                mi = i - len(self.units[0]) + self.age
                if 0 <= mi < len(self.mines[j]) and self.units[j, i] == Unit.TANK:
                    if self.mines[j, mi] == Field.MINE:
                        self.units[j, i] = Unit.NONE
                        self.mines[j, mi] = Field.NONE

    def play(self):
        while not self.is_finished():
            self.step()
