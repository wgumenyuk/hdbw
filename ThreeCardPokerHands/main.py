from deck import Deck
from hand import Hand, probabilities

# Deck zufällig generieren
deck = Deck()
deck.generate()

# Drei zufällige Karten ziehen
cards = [ deck.draw_card() for _ in range(3) ]

# Blatt erstellen
hand = Hand(cards)

# Ranking und Wahrscheinlichkeit des Blattes ermitteln
hand_ranking = hand.get_ranking()
probability = probabilities[hand_ranking]

# Ergebnisse ausdrucken
print(hand)
print(hand_ranking, probability)