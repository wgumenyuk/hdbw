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
        self.hand_player_ranking_text = self.font.render(self.player_hand.get_ranking_name(), True, TEXT_LIGHT_COLOR)
        self.hand_player_ranking_text_rect = self.hand_player_ranking_text.get_rect(center=HAND_PLAYER_RANKING_TEXT_POS)
        self.hand_dealer_ranking_text = self.font.render(self.dealer_hand.get_ranking_name(), True, TEXT_LIGHT_COLOR)
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

    def payout_bonuses(self, ranking_name: str) -> None:
        """
        Zahlt Boni für Ante und Paar-Plus, falls zutreffend.

        Parameter:
        - `ranking_name` (str) - Name des Rankings (z.B. Flush).
        """

        payout = 0

        ante_bonus = ANTE_BONUS_PAYOUTS.get(ranking_name)
        pair_plus_bonus = PAIR_PLUS_BONUS_PAYOUTS.get(ranking_name)

        if ante_bonus:
            payout += self.ante * ante_bonus

        if self.pair_plus and pair_plus_bonus:
            payout += self.ante * pair_plus_bonus

        self.balance += payout
        self.persistent_data["balance"] = self.balance

    def payout_push(self) -> None:
        """
        Zahlt Gewinne an den Spieler aus, wenn Push gespielt wird.
        """

        # Play Push, Ante 1:1
        payout = self.ante * 3

        self.balance += payout
        self.persistent_data["balance"] = self.balance

    def payout_win(self) -> None:
        """
        Zahlt Gewinne an den Spieler aus.

        Parameter:
        - `ranking_name` (str) - Name des Rankings (z.B. Flush).
        """

        # Ante und Play jeweils 1:1
        payout = self.ante * 4

        self.balance += payout
        self.persistent_data["balance"] = self.balance

    def determine_winner(self) -> None:
        """
        Ermittelt das Ergebnis und zahlt Gewinne an den Spieler aus oder nimmt
        die Wetten ein.
        """

        player_ranking_name, \
        player_ranking_level, \
        player_ranking_sum = self.player_hand.get_ranking_info()

        _, dealer_ranking_level, \
        dealer_ranking_sum = self.dealer_hand.get_ranking_info()

        if not self.is_folded:
            self.payout_bonuses(player_ranking_name)

        if not self.dealer_hand.is_qualified():
            self.payout_push()
            return

        # Ranking (z.B. Paar, Flush, usw.)
        if player_ranking_level < dealer_ranking_level:
            # Spieler hat verloren
            print("Player hat verloren!")
            return

        if player_ranking_level > dealer_ranking_level:
            # Spieler hat gewonnen
            self.payout_win()
            return

        # Ranking Sum (Summe aller Rank-Werte der Karten)
        if player_ranking_sum < dealer_ranking_sum:
            print("Player hat verloren!")
            return
        
        if player_ranking_sum > dealer_ranking_sum:
            # Spieler hat gewonnen
            self.payout_win()
            return

        # Suits vergleichen
        player_highest_card = self.player_hand.get_highest_card()
        dealer_highest_card = self.dealer_hand.get_highest_card()

        if player_highest_card.suit_value > dealer_highest_card.suit_value:
            # Spieler hat gewonnen
            self.payout_win()
            return

        # Spieler hat verloren

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