import os.path as path
import pygame as pg
from constants import TEXT_LIGHT_COLOR

CHIP_TEXT_OFFSET_X = 25
CHIP_TEXT_OFFSET_Y = 35

base_path = path.join(path.dirname(path.abspath(__file__)), "../assets")
chip_path = path.join(base_path, "png/poker_chip.png")

chip = pg.transform.scale(pg.image.load(chip_path), (80, 80))

def render_chip(screen: pg.Surface, amount: int, dest: tuple[int]) -> None:
    """
    Rendert einen Poker-Chip mit einem Wert.

    Parameter:
    - `screen` (pg.Surface) - Fläche, auf der das Spiel gerendert wird.
    - `amount` (int)        - Wert des Poker-Chips.
    - `dest` (tuple[int])   - Koordinaten, an die der Poker-Chip gerendert wird.
    """

    font = pg.font.Font(None, 26)
    amount_text = font.render(f"${amount}", True, TEXT_LIGHT_COLOR)

    screen.blit(chip, dest)
    screen.blit(amount_text, (dest[0] + CHIP_TEXT_OFFSET_X, dest[1] + CHIP_TEXT_OFFSET_Y))