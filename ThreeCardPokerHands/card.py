# Alle Kartensymbole und -werte
suits = [ "♣️", "♦️", "♥️", "♠️" ]
ranks = [ "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A" ]

class Card:
    """
        Stellt eine Spielkarte dar.

        Attribute:
            - `suit_sym` - Symbol der Farbe (z.B. Pik oder Kreuz).
            - `suit_val` - Wert der Farbe.
            - `rank_sym` - Symbol des Kartenwertes (z.B. Q oder 6).
            - `rank_val` - Wert des Kartenwertes.
    """

    def __init__(self, suit_sym: str, suit_val: int, rank_sym: str, rank_val: int) -> None:
        """
            Konstruktor.
        """

        self.suit_sym = suit_sym
        self.suit_val = suit_val
        self.rank_sym = rank_sym
        self.rank_val = rank_val

    def __repr__(self) -> str:
        """
            Repräsentiert die Spielkarte als String.
        """

        return f"[{self.suit_sym} | {self.rank_sym}]"