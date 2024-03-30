from enum import Enum

class Color(Enum):
    EMPTY: str = '.'
    WHITE: str = 'O'
    BLACK: str = 'X'
    TIE: str = 'T'