import pygame as pg
from states import BaseState
from table import render_table
from constants import TEXT_LIGHT_COLOR, GameState

ANTE_STEP = 5

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

        self.font = pg.font.Font(None, 24)
        self.ante = 5
        self.ante_text = self.font.render(f"Ante: ${self.ante}", True, TEXT_LIGHT_COLOR)
    
    def init(self, persistent_data: dict) -> None:
        """
        Initialisiert anhaltende Daten beim Eintreten eines neuen Zustandes.
        """

        super().init(persistent_data)
        
        self.balance = self.persistent_data["balance"] - self.ante
        self.max_ante = self.balance / 2
        self.balance_text = self.font.render(f"Guthaben: ${self.balance}", True, TEXT_LIGHT_COLOR)

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
            if event.key == pg.K_UP and self.balance - ANTE_STEP >= self.max_ante:
                self.ante += ANTE_STEP
                self.balance -= ANTE_STEP
            elif event.key == pg.K_DOWN and self.ante - ANTE_STEP > 0:
                self.ante -= ANTE_STEP
                self.balance += ANTE_STEP
            elif event.key == pg.K_RETURN:
                if self.ante < self.max_ante:
                    self.next_state = GameState.PAIR_PLUS
                else:
                    # TODO self.next_state = GameState.CARD_DRAWING
                    pass
                
                self.persistent_data["balance"] = self.balance
                self.persistent_data["ante"] = self.ante
                self.is_done = True

        self.balance_text = self.font.render(f"Guthaben: ${self.balance}", True, TEXT_LIGHT_COLOR)
        self.ante_text = self.font.render(f"Ante: ${self.ante}", True, TEXT_LIGHT_COLOR)

    def render(self, screen: pg.Surface) -> None:
        render_table(screen)
        screen.blit(self.balance_text, (50, 50))
        screen.blit(self.ante_text, (50, 75))