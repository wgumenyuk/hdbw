from enum import Enum
import pygame as pg
from states import BaseState
from hand import Hand
from table import render_table
from chip import render_chip, play_chip_place_sound
from constants import (
    TEXT_LIGHT_COLOR,
    TEXT_WIN_COLOR,
    TEXT_LOSE_COLOR,
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

TIMER_EVENT = pg.USEREVENT + 5
TIMER_EVENT_INTERVAL = 1000

class Result(Enum):
    """
    Enum für alle möglichen Rundenergebnisse.
    """

    FOLDED = "FOLDED"
    LOSE = "LOSE"
    BONUS_ONLY = "BONUS_ONLY"
    PUSH = "PUSH"
    WIN = "WIN"

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
        
        self.payout = 0
        self.time_active = 0
        self.show_result = False
        self.result: Result = None
        self.result_text: pg.Surface = None
        self.payout_text: pg.Surface = None

        self.determine_winner()
        pg.time.set_timer(TIMER_EVENT, TIMER_EVENT_INTERVAL)

    def handle_event(self, event: pg.event.Event) -> None:
        """
        Verarbeitet ein vom Spiel eingehendes Event.

        Parameter:
        - `event` (pg.event.Event) - Eingehendes Event.
        """

        if event.type == pg.QUIT:
            self.quit = True
            return

        if event.type == TIMER_EVENT:
            # Nach 2 Sekunden: Payout anzeigen, falls vorhanden
            if self.time_active == 2000:
                self.display_result()

            # Nach 5 Sekunden: Nächsten Zustand aufrufen
            if self.time_active >= 5000:
                pg.time.set_timer(TIMER_EVENT, 0)
                self.persistent_data["balance"] = self.balance + self.payout
                self.is_done = True
                return

            self.time_active += 1000

    def payout_bonuses(self, ranking_name: str) -> None:
        """
        Zahlt Boni für Ante und Paar-Plus, falls zutreffend.

        Parameter:
        - `ranking_name` (str) - Name des Rankings (z.B. Flush).
        """

        ante_bonus = ANTE_BONUS_PAYOUTS.get(ranking_name)
        pair_plus_bonus = PAIR_PLUS_BONUS_PAYOUTS.get(ranking_name)

        if ante_bonus:
            self.payout += self.ante * ante_bonus

        if self.pair_plus and pair_plus_bonus:
            self.payout += self.ante * pair_plus_bonus
        
        if self.payout > 0:
            self.result = Result.BONUS_ONLY

    def payout_push(self) -> None:
        """
        Zahlt Gewinne an den Spieler aus, wenn Push gespielt wird.
        """

        self.result = Result.PUSH

        # Play Push, Ante 1:1
        self.payout += self.ante * 3

    def payout_win(self) -> None:
        """
        Zahlt Gewinne an den Spieler aus.

        Parameter:
        - `ranking_name` (str) - Name des Rankings (z.B. Flush).
        """

        self.result = Result.WIN

        # Ante und Play jeweils 1:1
        self.payout = self.ante * 4

    def loss(self) -> None:
        """
        Setzt das Ergebnis der Runde auf "Verlust".
        """

        if self.result == Result.BONUS_ONLY:
            return

        self.result = Result.LOSE  

    def display_result(self) -> None:
        """
        Zeigt das Ergebnis am Ende der Runde an.
        """     

        # Spieler hat gefolded
        if self.result == Result.FOLDED:
            self.result_text = self.font.render("Du hast gefolded!", True, TEXT_LOSE_COLOR) 

        # Spieler hat verloren
        elif self.result == Result.LOSE:
            self.result_text = self.font.render("Du hast verloren!", True, TEXT_LOSE_COLOR) 

        # Spieler hat verloren, aber einen Ante- oder Paar-Plus-Bonus erhalten
        elif self.result == Result.BONUS_ONLY:
            self.result_text = self.font.render("Du hast einen Bonus erhalten!", True, TEXT_WIN_COLOR) 

        # Push (Dealer nicht qualifiziert)
        elif self.result == Result.PUSH:
            self.result_text = self.font.render("Push! Der Dealer ist nicht qualifiziert.", True, TEXT_WIN_COLOR) 

        # Spieler hat gewonnen
        elif self.result == Result.WIN:
            self.result_text = self.font.render("Du hast gewonnen!", True, TEXT_WIN_COLOR) 

        # Payout anzeigen und Soundeffekt abspielen
        if self.result in [ Result.WIN, Result.PUSH, Result.BONUS_ONLY ]:
            self.payout_text = self.font.render(f"+ ${self.payout}", True, TEXT_WIN_COLOR)
            play_chip_place_sound()

        self.show_result = True

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

        if self.is_folded:
            self.result_text = self.font.render("Du hast gefolded!", True, TEXT_LOSE_COLOR)
            self.show_result = True
            return

        self.payout_bonuses(player_ranking_name)

        if not self.dealer_hand.is_qualified():
            self.payout_push()
            return

        # Ranking (z.B. Paar, Flush, usw.)
        if player_ranking_level < dealer_ranking_level:
            # Spieler hat verloren
            self.loss()
            return

        if player_ranking_level > dealer_ranking_level:
            # Spieler hat gewonnen
            self.payout_win()
            return

        # Ranking Sum (Summe aller Rank-Werte der Karten)
        if player_ranking_sum < dealer_ranking_sum:
            # Spieler hat verloren
            self.loss()
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
        self.loss()

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

        if self.payout_text and self.show_result:
            screen.blit(self.payout_text, (50, 75))

        if self.result_text and self.show_result:
            screen.blit(self.result_text, (50, 100))

        screen.blit(self.hand_player_ranking_text, self.hand_player_ranking_text_rect)
        screen.blit(self.hand_dealer_ranking_text, self.hand_dealer_ranking_text_rect)

        self.player_hand.render(screen, HAND_REVEAL_CARD_POS)  
        self.dealer_hand.render(screen, HAND_DEALER_CARD_POS)