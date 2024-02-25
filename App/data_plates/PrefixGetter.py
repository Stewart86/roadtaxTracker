import random
from typing import Final

CARS_PLATES_LETTERS: Final = {
    1:["S"],
    2:["F", "J", "K", "L"],
    3:["A", "B", "C", "D", "E", "F", "G", "H", "J", "K", "L", "M","N", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z",]
}

GOODS_PLATES_LETTERS: Final = {
    1:["G"],
    2:["T", "U", "V", "W", "X", "Y", "Z", "BA", "BB", "BC", "BD", "BE"]
}

class PrefixGetter:

    @staticmethod
    def get_cars_plate_prefix() -> str:
        prefix: str = (f"{random.choice(CARS_PLATES_LETTERS[1])}"
                       f"{random.choice(CARS_PLATES_LETTERS[2])}"
                       f"{random.choice(CARS_PLATES_LETTERS[3])}")
        return prefix
    @staticmethod
    def get_good_plate_prefi() -> str:
        prefix: str = (f"{random.choice(GOODS_PLATES_LETTERS[1])}"
                       f"{random.choice(GOODS_PLATES_LETTERS[2])}")
        return prefix