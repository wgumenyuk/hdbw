from card import Card

# Wahrscheinlichkeiten jeder Handkombination
# Übernommen aus http://people.math.sfu.ca/~alspach/comp16
probabilities = {
    "Straight Flush": "0,22%",
    "Three of a Kind": "0,24%",
    "Straight": "3,26%",
    "Flush": "4,95%",
    "Pair": "16,94%",
    "High Card": "74,39%"
}

class Hand:
    """
        Stellt eine Hand im Drei-Karten-Poker dar.

        Attribute:
            - `cards` - Karten, welche in der Hand enthalten sind.
    """

    def __init__(self, cards: list[Card]) -> None:
        """
            Konstruktor.
        """

        self.cards = cards

    def __repr__(self) -> str:
        """
            Repräsentiert die Hand als String.
        """

        cards = map(lambda card: card.__repr__(), self.cards)
        return " ".join(cards)

    def is_straight(self) -> bool:
        """
            Überprüft, ob die Hand einen Straight enthält.
        """

        ranks = list(map(lambda card: card.rank_val, self.cards))
        max_rank = max(ranks)
        return ranks.count(max_rank - 1) == 1 and ranks.count(max_rank - 2) == 1

    def is_flush(self) -> bool:
        """
            Überprüft, ob die Hand einen Flush enthält.
        """

        suits = list(map(lambda card: card.suit_val, self.cards))
        return all(suit == suits[0] for suit in suits)

    def is_three_of_a_kind(self) -> bool:
        """
            Überprüft, ob die Hand einen Drilling enthält.
        """

        ranks = list(map(lambda card: card.rank_val, self.cards))
        return all(rank == ranks[0] for rank in ranks)

    def is_pair(self):
        """
            Überprüft, ob die Hand ein Paar enthält.
        """

        ranks = set(map(lambda card: card.rank_val, self.cards))
        return len(ranks) == 2

    def is_straight_flush(self):
        """
            Überprüft, ob die Hand einen Straight Flush enthält.
        """

        return self.is_straight() and self.is_flush()

    def get_ranking(self):
        """
            Ermittelt das Ranking der Hand.
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