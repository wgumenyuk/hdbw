import pygame as pg
from states import BaseState
from deck import Deck
from table import render_table
from chip import render_chip
from constants import ANTE_CHIP_POS, PAIR_PLUS_CHIP_POS

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
        
        self.ante: int = self.persistent_data["ante"]
        self.pair_plus: int = self.persistent_data.get("pair_plus")
        self.deck: Deck = self.persistent_data["deck"]

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
        render_chip(screen, self.ante, ANTE_CHIP_POS)

        if self.pair_plus:
            render_chip(screen, self.pair_plus, PAIR_PLUS_CHIP_POS)

        