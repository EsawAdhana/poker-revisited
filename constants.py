from enum import Enum
from enum import IntEnum

class Hand(Enum):
    ROYAL_FLUSH = 1
    STRAIGHT_FLUSH = 2
    FOUR_OF_A_KIND = 3
    FULL_HOUSE = 4
    FLUSH = 5
    STRAIGHT = 6
    THREE_OF_A_KIND = 7
    TWO_PAIR = 8
    ONE_PAIR = 9
    HIGH_CARD = 10

    def __lt__(self, other):
        return self.value < other.value
    
    def __gt__(self, other):
        return self.value > other.value 
    
    def __ge__(self, other):
        return self.value >= other.value
    
    def __le__(self, other):
        return self.value <= other.value
    
    def __eq__(self, other):
        return self.value == other.value

class Numbers(IntEnum):
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
    SIX = 6
    SEVEN = 7
    EIGHT = 8
    NINE = 9
    TEN = 10
    JACK = 11
    QUEEN = 12
    KING = 13
    ACE = 14

class Suits(Enum):
    CLUBS = '♣️'
    DIAMONDS = '♦️'
    HEARTS = '♥️'
    SPADES = '♠️'

class Better(Enum):
    FIRST_HAND_IS_BETTER = 0
    SECOND_HAND_IS_BETTER = 1
    TIE = 2


if __name__ == '__main__':
    print("Running a file not intended to be run directly")