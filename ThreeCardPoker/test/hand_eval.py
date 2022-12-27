from os import system
from random import shuffle

SUITS = [ "club", "diamond", "heart", "spade" ]
RANKS = [ "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A" ]
RANKINGS = {
    "High Card": 0,
    "Pair": 1,
    "Flush": 2,
    "Straight": 3,
    "Three of a Kind": 4,
    "Straight Flush": 5
}

class Card:
    def __init__(self, suit_value: int, suit_name: str, rank_value: int, rank_name: str) -> None:
        self.suit_value = suit_value
        self.suit_name = suit_name
        self.rank_value = rank_value
        self.rank_name = rank_name

    def __repr__(self) -> str:
        return f"[{self.suit_name} | {self.rank_name}]"

class Hand:
    def __init__(self, cards: list[Card]) -> None:
        self.cards = cards

    def is_straight(self) -> bool:
        ranks = list(map(lambda card: card.rank_value, self.cards))
        max_rank = max(ranks)
        return ranks.count(max_rank - 1) == 1 and ranks.count(max_rank - 2) == 1

    def is_flush(self) -> bool:
        suits = list(map(lambda card: card.suit_value, self.cards))
        return all(suit == suits[0] for suit in suits)

    def is_three_of_a_kind(self) -> bool:
        ranks = list(map(lambda card: card.rank_value, self.cards))
        return all(rank == ranks[0] for rank in ranks)

    def is_pair(self) -> bool:
        ranks = set(map(lambda card: card.rank_value, self.cards))
        return len(ranks) == 2

    def is_straight_flush(self) -> bool:
        return self.is_straight() and self.is_flush()

    def get_ranking_name(self) -> str:
        if self.is_straight():
            return "Straight Flush" if self.is_flush() else "Straight"

        if self.is_three_of_a_kind():
            return "Three of a Kind"

        if self.is_flush():
            return "Flush"

        if self.is_pair():
            return "Pair"

        return "High Card"

    def get_highest_card(self) -> Card:
        return max(self.cards, key=lambda card: card.rank_value)

    def get_ranking_info(self) -> tuple[str, int, int]:
        ranking_name = self.get_ranking_name()
        ranking_level = RANKINGS[ranking_name]
        ranking_sum = sum(card.rank_value for card in self.cards)
        return (ranking_name, ranking_level, ranking_sum)

    def is_qualified(self) -> bool:
        ranking_name, *_ = self.get_ranking_info()
        highest_card = self.get_highest_card()

        if ranking_name == "High Card" and highest_card.rank_value < 10:
            return False

        return True

def determine_winner(p_hand: Hand, d_hand: Hand) -> None:
    system("cls")

    p_ranking_name, p_ranking_level, p_ranking_sum = p_hand.get_ranking_info()
    d_ranking_name, d_ranking_level, d_ranking_sum = d_hand.get_ranking_info()

    print("Player")
    print(p_hand.cards)
    print(p_hand.get_ranking_info(), end="\n\n")

    print("Dealer")
    print(d_hand.cards)
    print(d_hand.get_ranking_info(), end="\n\n")

    # Ranking (z.B. Paar, Flush, usw.)
    if p_ranking_level < d_ranking_level:
        # Spieler hat verloren
        print("Player hat verloren!")
        return

    if p_ranking_level > d_ranking_level:
        # Spieler hat gewonnen
        print("Player hat gewonnen!")
        return

    # Ranking Sum (Summe aller Rank-Werte der Karten)
    if p_ranking_sum < d_ranking_sum:
        print("Player hat verloren!")
        return
    
    if p_ranking_sum > d_ranking_sum:
        # Spieler hat gewonnen
        print("Player hat gewonnen!")
        return

    # Suits vergleichen
    player_highest_card = p_hand.get_highest_card()
    dealer_highest_card = d_hand.get_highest_card()

    if player_highest_card.suit_value < dealer_highest_card.suit_value:
        # Spieler hat verloren
        print("Player hat verloren!")
    else:
        # Spieler hat gewonnen
        print("Player hat gewonnen!")

deck = []

for suit_value, suit_name in enumerate(SUITS):
    for rank_value, rank_name in enumerate(RANKS):
        card = Card(suit_value, suit_name, rank_value, rank_name)
        deck.append(card)

shuffle(deck)

p_hand = Hand([ deck.pop(0) for _ in range(3) ])
d_hand = Hand([ deck.pop(0) for _ in range(3) ])

determine_winner(p_hand, d_hand)