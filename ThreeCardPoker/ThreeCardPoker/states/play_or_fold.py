import pygame as pg
from states import BaseState
from hand import Hand
from table import render_table
from chip import render_chip
from constants import (
    TEXT_LIGHT_COLOR,
    ANTE_CHIP_POS,
    PAIR_PLUS_CHIP_POS,
    HAND_PLAYER_CARD_POS,
    HAND_DEALER_CARD_POS,
    HAND_PLAYER_RANKING_TEXT_POS,
    GameState
)

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

        self.font = pg.font.Font(None, 24)

    def init(self, persistent_data: dict) -> None:
        """
        Initialisiert anhaltende Daten beim Eintreten eines neuen Zustandes.
        """

        super().init(persistent_data)

        self.balance: int = self.persistent_data["balance"]
        self.ante: int = self.persistent_data["ante"]
        self.pair_plus: int = self.persistent_data.get("pair_plus")
        self.player_hand: Hand = self.persistent_data["player_hand"]
        self.dealer_hand: Hand = self.persistent_data["dealer_hand"]
        
        self.balance_text = self.font.render(f"Guthaben: ${self.balance}", True, TEXT_LIGHT_COLOR)
        self.hand_ranking_text = self.font.render(self.player_hand.get_ranking_name(), True, TEXT_LIGHT_COLOR)
        self.hand_ranking_text_rect = self.hand_ranking_text.get_rect(center=HAND_PLAYER_RANKING_TEXT_POS)

    def handle_event(self, event: pg.event.Event) -> None:
        """
        Verarbeitet ein vom Spiel eingehendes Event.

        Parameter:
        - `event` (pg.event.Event) - Eingehendes Event.
        """

        if event.type == pg.QUIT:
            self.quit = True
            return

        if event.type == pg.KEYUP:
            # Backspace
            if event.key == pg.K_BACKSPACE:
                self.next_state = GameState.FOLD
                self.persistent_data["is_folded"] = True
                self.is_done = True

            # Enter
            elif event.key == pg.K_RETURN:
                self.next_state = GameState.PLAY
                self.persistent_data["balance"] -= self.ante
                self.persistent_data["is_folded"] = False
                self.is_done = True

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

        screen.blit(self.balance_text, (50, 50))
        screen.blit(self.hand_ranking_text, self.hand_ranking_text_rect)

        self.player_hand.render(screen, HAND_PLAYER_CARD_POS)
        self.dealer_hand.render(screen, HAND_DEALER_CARD_POS, hidden=(True, True, True))