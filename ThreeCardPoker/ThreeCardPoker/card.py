import os.path as path
from random import choice
import pygame as pg

SUITS = [ "club", "diamond", "heart", "spade" ]
RANKS = [ "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A" ]

base_path = path.join(path.dirname(path.abspath(__file__)), "../assets")

class Card:
    """
    Stellt eine Spielkarte dar.

    Attribute:
    - `suit_value` (int)        - Wert des Suits.
    - `rank_value` (int)        - Wert des Ranks.
    - `back_img` (pg.Surface)   - Textur der Kartenrückseite.
    - `front_img` (pg.Surface)  - Textur der Kartenvorderseite.
    """

    def __init__(self, suit_name: str, suit_value: int, rank_name: str, rank_value: int) -> None:
        """
        Konstruktor.
        """

        self.suit_value: int = suit_value
        self.rank_value: int = rank_value

        back_path = path.join(base_path, "png/back.png")
        front_path = path.join(base_path, f"png/{suit_name}_{rank_name}.png")

        self.back_img: pg.Surface = pg.transform.scale(pg.image.load(back_path), (110, 160))
        self.front_img: pg.Surface = pg.transform.scale(pg.image.load(front_path), (110, 160))

    def get_texture(self, degrees: int = None, hidden: bool = False) -> pg.Surface:
        """
        Gibt das zu rendernde Element zurück.

        Parameter:
        - `degrees` (int) - Um wie viel Grad die Textur gedreht werden soll.
        - `hidden` (bool) - Ob die Karte umgedreht ist.
        """

        img = self.back_img if hidden else self.front_img
        return pg.transform.rotate(img, degrees) if degrees != None else img

def play_card_place_sound() -> None:
    """
    Spielt einen zufälligen Soundeffekt beim Kartenziehen ab.
    """

    card_place_sounds = [
        pg.mixer.Sound(path.join(base_path, "ogg/card_place_1.ogg")),
        pg.mixer.Sound(path.join(base_path, "ogg/card_place_2.ogg")),
        pg.mixer.Sound(path.join(base_path, "ogg/card_place_3.ogg"))
    ]

    card_place_sound = choice(card_place_sounds)
    pg.mixer.Sound.play(card_place_sound)

def play_card_shuffle_sound() -> None:
    """
    Spielt einen Soundeffekt beim Kartenmischen.
    """

    card_shuffle_sound_path = path.join(base_path, "ogg/card_shuffle.ogg")
    card_shuffle_sound = pg.mixer.Sound(card_shuffle_sound_path)
    pg.mixer.Sound.play(card_shuffle_sound)