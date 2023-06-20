**Semester**|**Kurs**|**Datum**
-----|-----|-----
SoSe 2023|Softwareentwicklung 2|20.06.2023

# Magic Square
Programm zum Lösen von magischen Quadraten für $n\in\lbrace[2,10]\backslash2\mathbb{N}\rbrace$.

> Bei diesem Projekt handelt es sich um ein benotetes Übungsprojekt.

## Beispiel
Ein magisches Quadrat für $n=5$.

```
17 24  1  8 15 
23  5  7 14 16 
 4  6 13 20 22 
10 12 19 21  3
11 18 25  2  9
```

## Verwendung
1. Mit Gradle kompilieren
```
$ gradle build 
```

oder

```
$ ./gradlew
```

2. Ausführen
```
$ java -jar ./build/libs/MagicSquare.jar 5
```

## Anerkennungen
- WikiHow: https://www.wikihow.com/Solve-a-Magic-Square
