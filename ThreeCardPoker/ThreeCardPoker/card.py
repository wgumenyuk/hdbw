import os.path as path
import pygame as pg

SUITS = [ "club", "diamond", "heart", "spade" ]
RANKS = [ "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A" ]

class Card:
    """
    Stellt eine Spielkarte dar.

    Attribute:
    - `is_hidden` (bool)        - Ob die Karte umgedreht ist.
    - `suit_value` (int)        - Wert des Suits.
    - `rank_value` (int)        - Wert des Ranks.
    - `back_img` (pg.Surface)   - Textur der Kartenrückseite.
    - `front_img` (pg.Surface)  - Textur der Kartenvorderseite.
    """

    def __init__(self, suit_name: str, suit_value: int, rank_name: str, rank_value: int) -> None:
        """
        Konstruktor.
        """

        self.is_hidden: bool = False
        self.suit_value: int = suit_value
        self.rank_value: int = rank_value

        base_path = path.join(path.dirname(path.abspath(__file__)), "../assets/png")
        back_path = path.join(base_path, "back.png")
        front_path = path.join(base_path, f"{suit_name}_{rank_name}.png")

        self.back_img: pg.Surface = pg.image.load(back_path)
        self.front_img: pg.Surface = pg.image.load(front_path)

    def get_texture(self) -> pg.Surface:
        """
        Gibt das zu rendernde Element zurück.
        """

        return self.back_img if self.is_hidden else self.front_img 