import pygame as pg
from states import BaseState
from hand import Hand
from table import render_table
from chip import render_chip
from card import play_card_place_sound
from constants import (
    TEXT_LIGHT_COLOR,
    ANTE_CHIP_POS,
    PAIR_PLUS_CHIP_POS,
    HAND_PLAYER_CARD_POS,
    HAND_DEALER_CARD_POS,
    HAND_REVEAL_CARD_POS,
    HAND_PLAYER_RANKING_TEXT_POS,
    GameState
)

MOVE_CARD_EVENT = pg.USEREVENT + 2
MOVE_CARD_EVENT_DELAY = 750

class FoldState(BaseState):
    """
    Fold-Zustand.
    Der Spieler gibt seine Kartenhand weg.
    """

    def __init__(self) -> None:
        """
        Konstruktor.
        """

        super().__init__()

        self.next_state = GameState.REVEAL
        self.font = pg.font.Font(None, 24)

    def init(self, persistent_data: dict) -> None:
        """
        Initialisiert anhaltende Daten beim Eintreten eines neuen Zustandes.
        """

        super().init(persistent_data)

        self.ante: int = self.persistent_data["ante"]
        self.pair_plus: int = self.persistent_data["pair_plus"]
        self.balance: int = self.persistent_data["balance"]
        self.player_hand: Hand = self.persistent_data["player_hand"]
        self.dealer_hand: Hand = self.persistent_data["dealer_hand"]
        
        self.balance_text = self.font.render(f"Guthaben: ${self.balance}", True, TEXT_LIGHT_COLOR)
        self.hand_ranking_text = self.font.render(self.player_hand.get_ranking(), True, TEXT_LIGHT_COLOR)
        self.hand_ranking_text_rect = self.hand_ranking_text.get_rect(center=HAND_PLAYER_RANKING_TEXT_POS)
        
        self.folded_hand = Hand()
        self.card_id = 0

        pg.time.set_timer(MOVE_CARD_EVENT, MOVE_CARD_EVENT_DELAY)

    def handle_event(self, event: pg.event.Event) -> None:
        """
        Verarbeitet ein vom Spiel eingehendes Event.

        Parameter:
        - `event` (pg.event.Event) - Eingehendes Event.
        """

        if event.type == pg.QUIT:
            self.quit = True
            return

        if event.type == MOVE_CARD_EVENT:
            if self.card_id == 3:
                pg.time.set_timer(MOVE_CARD_EVENT, 0)
                self.persistent_data["player_hand"] = self.folded_hand
                self.persistent_data["is_folded"] = True
                self.is_done = True
                return

            play_card_place_sound()
            card = self.player_hand.remove_card()
            self.folded_hand.add_card(card)
            self.card_id += 1

    def render(self, screen: pg.Surface) -> None:
        """
        Rendert die Elemente im Fold-Zustand.
        
        Parameter:
        - `screen` (pg.Surface) - Bildschirm, auf den gerendert wird.
        """

        render_table(screen)
        render_chip(screen, self.ante, ANTE_CHIP_POS)

        if self.pair_plus:
            render_chip(screen, self.pair_plus, PAIR_PLUS_CHIP_POS)

        screen.blit(self.balance_text, (50, 50))
        screen.blit(self.hand_ranking_text, self.hand_ranking_text_rect)

        # Player-Hand
        if len(self.player_hand.cards) > 0:
            self.player_hand.render(screen, HAND_PLAYER_CARD_POS)

        # Gefoldete Karten an Reveal-Position
        if len(self.folded_hand.cards) > 0:
            self.folded_hand.render(screen, HAND_REVEAL_CARD_POS, hidden=(True, True, True))

        self.dealer_hand.render(screen, HAND_DEALER_CARD_POS, hidden=(True, True, True))