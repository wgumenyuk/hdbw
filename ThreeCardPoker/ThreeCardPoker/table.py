import os.path as path
import pygame as pg

base_path = path.join(path.dirname(path.abspath(__file__)), "../assets")
table_path = path.join(base_path, "png/table.png")

table = pg.image.load(table_path)

def render_table(screen: pg.Surface) -> None:
    """
    Rendert den Tisch.

    Parameter:
    - `screen` (pg.Surface) - Fläche, auf der das Spiel gerendert wird.
    """

    screen.blit(table, (0, 0))