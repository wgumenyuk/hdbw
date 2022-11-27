from random import shuffle
from card import Card, suits, ranks

class Deck:
    """
        Stellt ein standard 52er-Kartendeck dar.

        Attribute:
            - `cards` - Im Deck enthaltene Karten.
    """

    def __init__(self) -> None:
        """
            Konstruktor.
        """
        
        self.cards: list[Card] = []

    def generate(self) -> None:
        """
            Generiert ein Kartendeck und mischt dieses anschließend mit `random.shuffle()` durch.
        """

        for suit_val, suit_sym in enumerate(suits):
            for rank_val, rank_sym in enumerate(ranks):
                card = Card(suit_sym, suit_val, rank_sym, rank_val)
                self.cards.append(card)

        shuffle(self.cards)

    def draw_card(self) -> Card:
        """
            Zieht die oberste Karte aus dem Deck.
        """

        return self.cards.pop(0)