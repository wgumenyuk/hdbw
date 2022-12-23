import pygame as pg
from card import Card

RANKINGS = {
    "High Card": 0,
    "Pair": 1,
    "Flush": 2,
    "Straight": 3,
    "Three of a Kind": 4,
    "Straight Flush": 5
}

class Hand:
    """
    Stellt eine Kartenhand dar.

    Attribute:
    - `cards` (list[Card]) Karten, aus denen die Hand besteht.
    """

    def __init__(self) -> None:
        """
        Konstruktor.
        """

        self.cards: list[Card] = []

    def is_straight(self) -> bool:
        """
        Überprüft, ob die Kartenhand ein Straight ist.
        """

        ranks = list(map(lambda card: card.rank_value, self.cards))
        max_rank = max(ranks)
        return ranks.count(max_rank - 1) == 1 and ranks.count(max_rank - 2) == 1

    def is_flush(self) -> bool:
        """
        Überprüft, ob die Kartenhand ein Flush ist.
        """

        suits = list(map(lambda card: card.suit_value, self.cards))
        return all(suit == suits[0] for suit in suits)

    def is_three_of_a_kind(self) -> bool:
        """
        Überprüft, ob die Kartenhand ein Three of a Kind ist.
        """

        ranks = list(map(lambda card: card.rank_value, self.cards))
        return all(rank == ranks[0] for rank in ranks)

    def is_pair(self) -> bool:
        """
        Überprüft, ob die Hand ein Paar enthält.
        """

        ranks = set(map(lambda card: card.rank_value, self.cards))
        return len(ranks) == 2

    def is_straight_flush(self) -> bool:
        """
        Überprüft, ob die Kartenhand ein Straight Flush ist.
        """

        return self.is_straight() and self.is_flush()

    def get_ranking(self) -> str:
        """
        Ermittelt das Ranking der Kartenhand und gibt dieses als String zurück.
        """

        if self.is_straight():
            return "Straight Flush" if self.is_flush() else "Straight"

        if self.is_three_of_a_kind():
            return "Three of a Kind"

        if self.is_flush():
            return "Flush"

        if self.is_pair():
            return "Pair"

        return "High Card"

    def get_ranking_level(self) -> int:
        """
        Ermittelt das Ranking der Kartenhand und gibt dieses als Integer zurück.
        """

        ranking = self.get_ranking()
        return RANKINGS[ranking]

    def get_highest_card(self) -> Card:
        """
        Gibt die Karte mit dem höchsten Wert zurück.
        """

        return max(self.cards, key=lambda card: card.rank_value)

    def is_qualified(self) -> bool:
        """
        Ermittelt, ob die Hand qualifiziert ist. Nur für den Dealer relevant.
        Alle Hands schlechter als Queen High gelten als nicht-qualifiziert.
        """

        ranking = self.get_ranking()
        highest_card = self.get_highest_card()

        if ranking == "High Card" and highest_card.rank_value < 10:
            return False

        return True

    def add_card(self, card: Card) -> None:
        """
        Fügt der Hand eine Karte hinzu.
        """

        self.cards.append(card)

    def remove_card(self) -> Card:
        """
        Entfernt die letzte Karte aus der Hand.
        """

        return self.cards.pop(len(self.cards) - 1)

    def render(self, screen: pg.Surface, pos: list[tuple[int]], degrees: int = None, hidden: tuple[bool] = None) -> None:
        """
        Rendert die Karten auf den Tisch.

        Parameter:
        Parameter:
        - `screen` (pg.Surface)     - Fläche, auf der das Spiel gerendert wird.
        - `pos` (list[tuple[int]])  - Positionen der jeweiligen Karten auf dem Tisch.
        - `degrees` (int)           - Winkel, um den die Karten gedreht werden.
        - `hidden` (tuple[bool])    - Tuple mit Werten für die jeweilige versteckte Karten.
        """

        for i, card in enumerate(self.cards):
            is_hidden = True if isinstance(hidden, tuple) and hidden[i] else False
            texture = card.get_texture(hidden=is_hidden)

            if degrees != None:
                texture = pg.transform.rotate(texture, degrees)

            screen.blit(texture, pos[i])