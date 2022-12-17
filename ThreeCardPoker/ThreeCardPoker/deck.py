from random import shuffle
from card import Card, SUITS, RANKS

class Deck:
    """
    Stellt ein standard 52er-Kartendeck dar.
    """

    def __init__(self) -> None:
        """
        Konstruktor.
        """

        self.cards: list[Card] = []

        for suit_value, suit_name in enumerate(SUITS):
            for rank_value, rank_name in enumerate(RANKS):
                card = Card(suit_name, suit_value, rank_name, rank_value)
                self.cards.append(card)
        
        shuffle(self.cards)

    def draw(self) -> Card:
        """
        Zieht die oberste Karte aus dem Deck heraus.
        """

        return self.cards.pop(0)