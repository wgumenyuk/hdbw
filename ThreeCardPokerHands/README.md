**Semester**|**Kurs**|**Datum**
-----|-----|-----
WS 2022/23|Softwareentwicklung|27.11.2022

# ThreeCardPokerHands
Dieses Programm generiert ein standard 52er-Kartendeck und mischt dieses anschließend mit `random.shuffle()`durch.
Aus dem generierten Deck wird eine Hand mit drei Karten zusammengestellt. Zum Schluss wird nach Spielregeln des Drei-Karten-Pokers das Ranking und die Wahrscheinlichkeit der Hand ermittelt.

## Verwendung
```sh-session
$ python main.py
```

**Ausgabe**
```
[♦️ | A] [♣️ | 7] [♦️ | 7]
Pair 16,94%
```

## Angewandtes Wissen
- Imports
- Listen
- Sets
- Dictionaries
- `for`-Schleifen
- Funktionen
- Klassen

## Funktionsweise
### Karten
Jede Karte besitzt einen Wert für ihre Kartenfarbe (`suit_val`) und einen Wert für ihren Kartenwert (`rank_val`), die zum Ermitteln des Rankings verwendet werden.

**Kartenfarben und ihre Werte**
**♣️**|**♦️**|**♥️**|**♠️**
:-----:|:-----:|:-----:|:-----:
0|1|2|3

**Kartenwerte und ihre Werte**
**2**|**3**|**4**|**5**|**6**|**7**|**8**|**9**|**10**|**J**|**Q**|**K**|**A**
:-----:|:-----:|:-----:|:-----:|:-----:|:-----:|:-----:|:-----:|:-----:|:-----:|:-----:|:-----:|:-----:
0|1|2|3|4|5|6|7|8|9|10|11|12

### Generieren des Decks
Mithilfe von `for`-Schleifen werden alle möglichen 52 Kombinationen der Spielkarten erstellt und in einer Liste gespeichert.
Diese Liste wird anschließend mit `random.shuffle()` durchgemischt.

### Hand-Rankings im Drei-Karten-Poker
Im Drei-Karten-Poker gibt es eine feste Reihenfolge der Hand-Rankings:

**Ranking**|**Hand**|**Erklärung**
-----|-----|-----
1|Straight Flush|Straight mit Karten derselben Farbe.
2|Three of a Kind|Drei Karten desselben Werts.
3|Straight|Hand mit drei aufeinander folgenden Karten.
4|Flush|Drei Karten derselben Farbe.
5|Pair|Zwei Karten desselben Werts.
6|High Card|Höchste Karte der Hand.

### Programmatische Ermittlung der Rankings
#### Straight Flush
Mithilfe der Methoden überprüfen, ob die Hand ein Straight und ein Flush ist.

#### Straight
1. Größten Kartenwert `max_rank` mit `max()` finden.
2. Mit `count()` überprüfen, ob Kartenwerte `max_rank - 1` und `max_rank - 2` in der Hand vorhanden sind.

#### Flush
Mit `all()` überprüfen, ob die Farben der restlichen Karten der Farbe der ersten Karte gleichen.

#### Three of a Kind
Mit `all()` überprüfen, ob die restlichen Kartenwerte dem Kartenwert der ersten Karte gleichen.

#### Pair
1. Kartenwerte in ein Set umwandeln.
2. Überprüfen, ob das Set eine Länge von `2` hat.

> In Sets können nur einzigartige Elemente vorkommen. Beträgt die Länge des Sets also `2` anstelle von `3`, bedeutet das, dass die Hand ein Paar enthält.

#### High Card
Erfüllt die Hand keine der vorherigen Bedingungen, kann es sich nur um eine High Card handeln.

## Ausgeben der jeweiligen Wahrscheinlichkeiten
Die jeweiligen Wahrscheinlichkeiten werden in einem Dictionary gespeichert. Die Werte wurden aus diesem [Dokument](http://people.math.sfu.ca/~alspach/comp16) übernommen.
Nach Ermitteln des Rankings wird die Wahrscheinlichkeit aus dem Dictionary abgerufen und ausgegeben.