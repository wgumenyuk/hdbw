from pathlib import Path
import pygame as pg

table_path = Path("assets/png/table.png")
table = pg.image.load(table_path)

def render_table(screen: pg.Surface) -> None:
    """
    Rendert den Tisch.

    Parameter:
    - `screen` (pg.Surface) - Fläche, auf der das Spiel gerendert wird.
    """

    screen.blit(table, (0, 0))