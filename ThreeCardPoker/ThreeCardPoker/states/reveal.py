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
    PLAY_CHIP_POS,
    HAND_DEALER_CARD_POS,
    HAND_PLAY_CARD_POS,
    HAND_REVEAL_CARD_POS,
    HAND_PLAYER_RANKING_TEXT_POS,
    HAND_DEALER_RANKING_TEXT_POS,
    GameState
)

MOVE_EVENT = pg.USEREVENT + 3
MOVE_EVENT_DELAY = 750

class RevealState(BaseState):
    """
    Reveal-Zustand.
    Der Dealer deckt seine Karten auf.
    """

    def __init__(self) -> None:
        """
        Konstruktor.
        """

        super().__init__()

        self.next_state = GameState.PAYOUT
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
        self.is_folded: bool = self.persistent_data["is_folded"]

        self.balance_text = self.font.render(f"Guthaben: ${self.balance}", True, TEXT_LIGHT_COLOR)
        self.hand_player_ranking_text = self.font.render(self.player_hand.get_ranking_name(), True, TEXT_LIGHT_COLOR)
        self.hand_player_ranking_text_rect = self.hand_player_ranking_text.get_rect(center=HAND_PLAYER_RANKING_TEXT_POS)
        self.hand_dealer_ranking_text = self.font.render(self.dealer_hand.get_ranking_name(), True, TEXT_LIGHT_COLOR)
        self.hand_dealer_ranking_text_rect = self.hand_dealer_ranking_text.get_rect(center=HAND_DEALER_RANKING_TEXT_POS)
        
        self.revealed_player_hand = Hand()
        self.hand_player_state = (True, True, True)
        self.hand_dealer_state = (True, True, True)
        self.show_hand_dealer_ranking = False
        self.move_id = 0

        pg.time.set_timer(MOVE_EVENT, MOVE_EVENT_DELAY)

    def handle_event(self, event: pg.event.Event) -> None:
        """
        Verarbeitet ein vom Spiel eingehendes Event.

        Parameter:
        - `event` (pg.event.Event) - Eingehendes Event.
        """

        if event.type == pg.QUIT:
            self.quit = True
            return

        if event.type == MOVE_EVENT:
            # Player-Hand (gespielt) aufdecken
            if self.move_id <= 2 and not self.is_folded:
                card = self.player_hand.remove_card()
                self.revealed_player_hand.add_card(card)

            # Player-Hand (folded) aufdecken
            elif self.move_id == 0:
                self.hand_player_state = (True, True, False)
            elif self.move_id == 1:
                self.hand_player_state = (True, False, False)
            elif self.move_id == 2:
                self.hand_player_state = (False, False, False)

            # Dealer-Hand aufdecken
            elif self.move_id == 3:
                self.hand_dealer_state = (True, True, False)
            elif self.move_id == 4:
                self.hand_dealer_state = (True, False, False)
            elif self.move_id == 5:
                self.hand_dealer_state = (False, False, False)
                self.show_hand_dealer_ranking = True

            # Ende
            else:
                pg.time.set_timer(MOVE_EVENT, 0)

                if self.is_folded:
                    self.persistent_data["player_hand"] = self.player_hand
                else:
                    self.persistent_data["player_hand"] = self.revealed_player_hand

                self.is_done = True
                return

            if self.move_id < 6:
                play_card_place_sound()

            self.move_id += 1

    def render(self, screen: pg.Surface) -> None:
        """
        Rendert die Elemente im Reveal-Zustand.
        
        Parameter:
        - `screen` (pg.Surface) - Bildschirm, auf den gerendert wird.
        """

        render_table(screen)
        render_chip(screen, self.ante, ANTE_CHIP_POS)

        if self.pair_plus:
            render_chip(screen, self.pair_plus, PAIR_PLUS_CHIP_POS)

        screen.blit(self.balance_text, (50, 50))
        screen.blit(self.hand_player_ranking_text, self.hand_player_ranking_text_rect)

        if self.show_hand_dealer_ranking:
            screen.blit(self.hand_dealer_ranking_text, self.hand_dealer_ranking_text_rect)

        # Gespielte Karten an Reveal-Position
        if len(self.revealed_player_hand.cards) > 0:
            self.revealed_player_hand.render(screen, HAND_REVEAL_CARD_POS)  

        # Player-Hand
        if len(self.player_hand.cards) > 0:
            pos = HAND_REVEAL_CARD_POS if self.is_folded else HAND_PLAY_CARD_POS
            degree = 0 if self.is_folded else 90
            self.player_hand.render(screen, pos, degree, self.hand_player_state)

        if not self.is_folded:
            render_chip(screen, self.ante, PLAY_CHIP_POS)

        self.dealer_hand.render(screen, HAND_DEALER_CARD_POS, hidden=self.hand_dealer_state)