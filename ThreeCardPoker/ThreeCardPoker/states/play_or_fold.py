import pygame as pg
from states import BaseState
from card import Card
from table import render_table
from chip import render_chip
from constants import ANTE_CHIP_POS, PAIR_PLUS_CHIP_POS, HAND_PLAYER_CARD_POS, HAND_DEALER_CARD_POS, PLAY_CARD_POS

class PlayOrFoldState(BaseState):
    """
    Play-or-Fold-Zustand.
    Der Spieler entscheidet, ob er spielen oder falten will.
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
        self.pair_plus: int = self.persistent_data["pair_plus"]
        self.player_hand: list[Card] = persistent_data["player_hand"]
        self.dealer_hand: list[Card] = persistent_data["dealer_hand"]

        print("PLAY OR FOLD!")

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
        Rendert die Elemente im Play-or-Fold-Zustand.
        
        Parameter:
        - `screen` (pg.Surface) - Bildschirm, auf den gerendert wird.
        """

        render_table(screen)
        render_chip(screen, self.ante, ANTE_CHIP_POS)

        if self.pair_plus:
            render_chip(screen, self.pair_plus, PAIR_PLUS_CHIP_POS)

        for i, card in enumerate(self.player_hand):
            screen.blit(card.get_texture(), HAND_PLAYER_CARD_POS[i])

        for i, card in enumerate(self.dealer_hand):
            screen.blit(card.get_texture(hidden=True), HAND_DEALER_CARD_POS[i])