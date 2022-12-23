import pygame as pg
from states import BaseState
from hand import Hand
from table import render_table
from chip import render_chip, play_chip_place_sound
from card import play_card_place_sound
from constants import (
    TEXT_LIGHT_COLOR,
    ANTE_CHIP_POS,
    PAIR_PLUS_CHIP_POS,
    PLAY_CHIP_POS,
    HAND_PLAYER_CARD_POS,
    HAND_DEALER_CARD_POS,
    HAND_PLAY_CARD_POS,
    HAND_PLAYER_RANKING_TEXT_POS,
    GameState
)

MOVE_EVENT = pg.USEREVENT + 2
MOVE_EVENT_DELAY = 750

class PlayState(BaseState):
    """
    Play-Zustand.
    Der Spieler wettet auf seine Kartenhand.
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

        self.balance: int = self.persistent_data["balance"]
        self.ante: int = self.persistent_data["ante"]
        self.pair_plus: int = self.persistent_data.get("pair_plus")
        self.player_hand: Hand = self.persistent_data["player_hand"]
        self.dealer_hand: Hand = self.persistent_data["dealer_hand"]

        self.balance_text = self.font.render(f"Guthaben: ${self.balance}", True, TEXT_LIGHT_COLOR)
        self.hand_ranking_text = self.font.render(self.player_hand.get_ranking(), True, TEXT_LIGHT_COLOR)
        self.hand_ranking_text_rect = self.hand_ranking_text.get_rect(center=HAND_PLAYER_RANKING_TEXT_POS)
        
        self.played_hand = Hand()
        self.show_play_chip = False
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
            # Gespielte Karten verschieben
            if self.move_id <= 2:
                play_card_place_sound()
                card = self.player_hand.remove_card()
                self.played_hand.add_card(card)

            # Poker-Chip für Play-Wette platzieren
            elif self.move_id == 3:
                self.show_play_chip = True
                play_chip_place_sound()
            
            # Ende
            elif self.move_id == 4:
                pg.time.set_timer(MOVE_EVENT, 0)
                self.persistent_data["player_hand"] = self.played_hand
                self.is_done = True
                return
            
            self.move_id += 1

    def render(self, screen: pg.Surface) -> None:
        """
        Rendert die Elemente im Play-Zustand.
        
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

        # Gespielte Karten an Play-Position
        if len(self.played_hand.cards) > 0:
            self.played_hand.render(screen, HAND_PLAY_CARD_POS, degrees=90, hidden=(True, True, True))

        if self.show_play_chip:
            render_chip(screen, self.ante, PLAY_CHIP_POS)

        self.dealer_hand.render(screen, HAND_DEALER_CARD_POS, hidden=(True, True, True))