import pygame as pg
from states import BaseState
from table import render_table
from chip import render_chip
from constants import TEXT_LIGHT_COLOR, ANTE_CHIP_POS, GameState

PAIR_PLUS_STEP = 5

class PairPlusState(BaseState):
    """
    Paar-Plus-Zustand.
    Das Spiel wartet auf eine optionale Pair-Plus-Wette des Spielers.
    """

    def __init__(self) -> None:
        """
        Konstruktor.
        """

        super().__init__()

        self.font = pg.font.Font(None, 24)
        self.pair_plus = 0
        self.pair_plus_text = self.font.render(f"Paar-Plus: ${self.pair_plus}", True, TEXT_LIGHT_COLOR)
    
    def init(self, persistent_data: dict) -> None:
        """
        Initialisiert anhaltende Daten beim Eintreten eines neuen Zustandes.
        """

        super().init(persistent_data)
        
        self.balance = self.persistent_data["balance"]
        self.ante = self.persistent_data["ante"]
        self.balance_text = self.font.render(f"Guthaben: ${self.balance}", True, TEXT_LIGHT_COLOR)
        self.ante_text = self.font.render(f"Ante: ${self.ante}", True, TEXT_LIGHT_COLOR)

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
            if event.key == pg.K_UP and self.balance - PAIR_PLUS_STEP >= self.ante:
                self.balance -= PAIR_PLUS_STEP
                self.pair_plus += PAIR_PLUS_STEP
            elif event.key == pg.K_DOWN and self.pair_plus - PAIR_PLUS_STEP >= 0:
                self.balance += PAIR_PLUS_STEP
                self.pair_plus -= PAIR_PLUS_STEP
            elif event.key == pg.K_RETURN:
                self.next_state = GameState.CARD_DRAWING
                self.persistent_data["balance"] = self.balance
                self.persistent_data["pair_plus"] = self.pair_plus
                self.is_done = True

        self.balance_text = self.font.render(f"Guthaben: ${self.balance}", True, TEXT_LIGHT_COLOR)
        self.pair_plus_text = self.font.render(f"Paar-Plus: ${self.pair_plus}", True, TEXT_LIGHT_COLOR)

    def render(self, screen: pg.Surface) -> None:
        """
        Rendert die Elemente im Paar-Plus-Zustand.
        
        Parameter:
        - `screen` (pg.Surface) - Bildschirm, auf den gerendert wird.
        """

        render_table(screen)
        render_chip(screen, self.ante, ANTE_CHIP_POS)
        screen.blit(self.balance_text, (50, 50))
        screen.blit(self.ante_text, (50, 75))
        screen.blit(self.pair_plus_text, (50, 100))