import pygame as pg
from states import BaseState
from hand import Hand
from table import render_table
from chip import render_chip
from constants import (
    TEXT_LIGHT_COLOR,
    ANTE_CHIP_POS,
    PAIR_PLUS_CHIP_POS,
    PLAY_CHIP_POS,
    HAND_DEALER_CARD_POS,
    HAND_REVEAL_CARD_POS,
    HAND_PLAYER_RANKING_TEXT_POS,
    HAND_DEALER_RANKING_TEXT_POS,
    GameState
)

ANTE_BONUS_PAYOUTS = {
    "Straight": 2,
    "Three of a Kind": 5,
    "Straight Flush": 6
}

PAIR_PLUS_BONUS_PAYOUTS = {
    "Pair": 2,
    "Flush": 5,
    "Straight": 7,
    "Three of a Kind": 31,
    "Straight Flush": 41
}

class PayoutState(BaseState):
    """
    Payout-Zustand.
    Der Dealer zahlt Payouts oder sammelt die Wetten ein.
    """

    def __init__(self) -> None:
        """
        Konstruktor.
        """

        super().__init__()

        self.next_state = GameState.ANTE
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
        self.hand_player_ranking_text = self.font.render(self.player_hand.get_ranking(), True, TEXT_LIGHT_COLOR)
        self.hand_player_ranking_text_rect = self.hand_player_ranking_text.get_rect(center=HAND_PLAYER_RANKING_TEXT_POS)
        self.hand_dealer_ranking_text = self.font.render(self.dealer_hand.get_ranking(), True, TEXT_LIGHT_COLOR)
        self.hand_dealer_ranking_text_rect = self.hand_dealer_ranking_text.get_rect(center=HAND_DEALER_RANKING_TEXT_POS)
        
        self.time_active = 0

        self.determine_winner()

    def update(self, tick: int) -> None:
        """
        Aktualisiert den Zustand.

        Parameter:
        - `tick` (int) - Wie viele Millisekunden seit dem letzten Update vergangen sind. 
        """

        if self.time_active >= 5000:
            self.is_done = True
            return

        self.time_active += tick

    def handle_event(self, event: pg.event.Event) -> None:
        """
        Verarbeitet ein vom Spiel eingehendes Event.

        Parameter:
        - `event` (pg.event.Event) - Eingehendes Event.
        """

        if event.type == pg.QUIT:
            self.quit = True
            return

    def payout(self, player_hand_ranking: str) -> None:
        """
        Zahlt die Gewinne an den Spieler, falls er gewinnt.
        """

        payout = self.ante * 4

        ante_bonus_multiplier = ANTE_BONUS_PAYOUTS.get(player_hand_ranking)
        pair_plus_multiplier = PAIR_PLUS_BONUS_PAYOUTS.get(player_hand_ranking)

        # Ante Bonus
        if ante_bonus_multiplier:
            payout += self.ante * ante_bonus_multiplier

        # Paar-Plus
        if self.pair_plus and pair_plus_multiplier:
            payout += self.pair_plus * pair_plus_multiplier

        self.balance += payout
        self.persistent_data["balance"] = self.balance

    def determine_winner(self) -> None:
        """
        Ermittelt den Gewinner und zahlt gegebenenfalls die jeweiligen Payouts.
        """

        # Folded
        if self.is_folded:
            return

        # Push (Dealer nicht qualifiziert)
        if not self.dealer_hand.is_qualified():
            self.balance += self.ante * 3
            return

        player_ranking = self.player_hand.get_ranking_level()
        player_ranking_name = self.player_hand.get_ranking()
        dealer_ranking = self.dealer_hand.get_ranking_level()

        # Gewinn des Dealers
        if player_ranking < dealer_ranking:
            # TODO Ergebnis anzeigen
            return

        # Gewinn des Spielers
        if player_ranking > dealer_ranking:
            self.payout(player_ranking_name)
            # TODO Ergebnis anzeigen
            return

        player_highest_card = self.player_hand.get_highest_card().rank_value
        dealer_highest_card = self.dealer_hand.get_highest_card().rank_value

        # Gewinn des Dealers
        if player_highest_card < dealer_highest_card:
            # TODO Ergebnis anzeigen
            return

        # Gewinn des Spielers
        if player_highest_card > dealer_highest_card:
            self.payout(player_ranking_name)
            # TODO Ergebnis anzeigen

    def render(self, screen: pg.Surface) -> None:
        """
        Rendert die Elemente im Payout-Zustand.
        
        Parameter:
        - `screen` (pg.Surface) - Bildschirm, auf den gerendert wird.
        """

        render_table(screen)
        render_chip(screen, self.ante, ANTE_CHIP_POS)

        if self.pair_plus:
            render_chip(screen, self.pair_plus, PAIR_PLUS_CHIP_POS)

        if not self.is_folded:
            render_chip(screen, self.ante, PLAY_CHIP_POS)

        screen.blit(self.balance_text, (50, 50))
        screen.blit(self.hand_player_ranking_text, self.hand_player_ranking_text_rect)
        screen.blit(self.hand_dealer_ranking_text, self.hand_dealer_ranking_text_rect)

        self.player_hand.render(screen, HAND_REVEAL_CARD_POS)  
        self.dealer_hand.render(screen, HAND_DEALER_CARD_POS)