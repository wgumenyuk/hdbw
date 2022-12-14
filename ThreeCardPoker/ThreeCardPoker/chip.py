from pathlib import Path
import pygame as pg
from constants import TEXT_LIGHT_COLOR

chip_path = Path("assets/png/poker_chip.png")
chip_place_sound_path = Path("assets/ogg/chip_place.ogg")

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
    amount_text_dest = (dest[0] + chip.get_rect().centerx, dest[1] + chip.get_rect().centery)
    amount_text_rect = amount_text.get_rect(center=amount_text_dest)

    screen.blit(chip, dest)
    screen.blit(amount_text, amount_text_rect)

def play_chip_place_sound() -> None:
    """
    Spielt einen Soundeffekt ab, sobald ein Poker-Chip auf dem Tisch platziert wird.
    """

    chip_place_sound = pg.mixer.Sound(chip_place_sound_path)
    pg.mixer.Sound.set_volume(chip_place_sound, 0.5)
    pg.mixer.Sound.play(chip_place_sound)