from enum import Enum

TITLE = "Three Card Poker"
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800
FPS = 60
TEXT_LIGHT_COLOR = (255, 255, 255) #FFFFFF
BG_COLOR = (180, 120, 200) #B478C8

class GameState(Enum):
    """
    Enum für alle möglichen Zustände des Spiels.
    """

    MENU = "MENU"
    ANTE = "ANTE"
    PAIR_PLUS = "PAIR_PLUS"
    CARD_DRAWING = "CARD_DRAWING"