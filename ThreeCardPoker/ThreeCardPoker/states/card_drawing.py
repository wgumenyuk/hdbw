import os.path as path
from random import choice
import pygame as pg
from states import BaseState
from hand import Hand
from deck import Deck
from card import play_card_place_sound
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

DEAL_CARD_EVENT = pg.USEREVENT + 1
DEAL_CARD_EVENT_DELAY = 750

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

        base_path = path.join(path.dirname(path.abspath(__file__)), "../../assets")

        self.next_state = GameState.PLAY_OR_FOLD
        self.font = pg.font.Font(None, 24)

        self.card_place_sounds = [
            pg.mixer.Sound(path.join(base_path, "ogg/card_place_1.ogg")),
            pg.mixer.Sound(path.join(base_path, "ogg/card_place_2.ogg")),
            pg.mixer.Sound(path.join(base_path, "ogg/card_place_3.ogg"))
        ]

    def init(self, persistent_data: dict) -> None:
        """
        Initialisiert anhaltende Daten beim Eintreten eines neuen Zustandes.
        """

        super().init(persistent_data)

        self.balance: int = self.persistent_data["balance"]
        self.ante: int = self.persistent_data["ante"]
        self.pair_plus: int = self.persistent_data.get("pair_plus")
        
        self.deck = Deck()
        self.player_hand = Hand()
        self.dealer_hand = Hand()
        
        self.balance_text = self.font.render(f"Guthaben: ${self.balance}", True, TEXT_LIGHT_COLOR)
        self.hand_ranking_text = None
        self.hand_ranking_text_rect = None
        
        self.card_id = 0

        pg.time.set_timer(DEAL_CARD_EVENT, DEAL_CARD_EVENT_DELAY)

    def handle_event(self, event: pg.event.Event) -> None:
        """
        Verarbeitet ein vom Spiel eingehendes Event.

        Parameter:
        - `event` (pg.event.Event) - Eingehendes Event.
        """

        if event.type == pg.QUIT:
            self.quit = True
            return

        if event.type == DEAL_CARD_EVENT:
            card = self.deck.draw()

            # Player-Hand
            if self.card_id <= 2:
                self.player_hand.add_card(card)

            # Dealer-Hand
            elif self.card_id <= 5:
                self.dealer_hand.add_card(card)
            
            # Ende
            else:
                pg.time.set_timer(DEAL_CARD_EVENT, 0)
                self.persistent_data["player_hand"] = self.player_hand
                self.persistent_data["dealer_hand"] = self.dealer_hand
                self.is_done = True
                return

            play_card_place_sound()
            self.card_id += 1

            # Hand-Ranking ermitteln und rendern 
            if len(self.player_hand.cards) == 3 and self.hand_ranking_text == None:
                self.hand_ranking_text = self.font.render(self.player_hand.get_ranking(), True, TEXT_LIGHT_COLOR)
                self.hand_ranking_text_rect = self.hand_ranking_text.get_rect(center=HAND_PLAYER_RANKING_TEXT_POS)

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

        screen.blit(self.balance_text, (50, 50))

        if self.hand_ranking_text:
            screen.blit(self.hand_ranking_text, self.hand_ranking_text_rect)

        self.player_hand.render(screen, HAND_PLAYER_CARD_POS)
        self.dealer_hand.render(screen, HAND_DEALER_CARD_POS, hidden=(True, True, True))