import pygame as pg
from states import BaseState
from table import render_table

class AnteState(BaseState):
    """
    Ante-Zustand.
    Das Spiel wartet auf die Ante-Wette des Spielers.
    """

    def __init__(self) -> None:
        """
        Konstruktor.
        """

        super().__init__()

    def handle_event(self, event: pg.event.Event) -> None:
        """
        Verarbeitet ein vom Spiel eingehendes Event.

        Parameter:
        - `event` (pg.event.Event) - Eingehendes Event.
        """

        if event.type == pg.QUIT:
            self.quit = True
            return

        pass

    def render(self, screen: pg.Surface) -> None:
        render_table(screen)