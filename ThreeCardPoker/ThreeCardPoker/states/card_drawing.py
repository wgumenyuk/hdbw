import pygame as pg
from states import BaseState
from table import render_table

class CardDrawingState(BaseState):
    """
    Card-Drawing-Zustand.
    Es werden Karten für Spieler und Dealer gezogen.
    """

    def __init__(self) -> None:
        """
        Konstruktor.
        """

        super().__init__()

    def init(self, persistent_data: dict) -> None:
        """
        Initialisiert anhaltende Daten beim Eintreten eines neuen Zustandes.
        """

        super().init(persistent_data)
        
        self.deck = self.persistent_data["deck"]

    def handle_event(self, event: pg.event.Event) -> None:
        """
        Verarbeitet ein vom Spiel eingehendes Event.

        Parameter:
        - `event` (pg.event.Event) - Eingehendes Event.
        """

        if event.type == pg.QUIT:
            self.quit = True
            return

    def render(self, screen: pg.Surface) -> None:
        """
        Rendert die Elemente im Card-Drawing-Zustand.
        
        Parameter:
        - `screen` (pg.Surface) - Bildschirm, auf den gerendert wird.
        """

        render_table(screen)