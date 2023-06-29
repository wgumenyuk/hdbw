**Semester**|**Kurs**|**Datum**
-----|-----|-----
SoSe 2023|Softwareentwicklung 2|29.06.2023

# Sudoku
Programm zum Lösen von Sudokus.

> Bei diesem Projekt handelt es sich um ein benotetes Übungsprojekt.

## Beispiel
**Input**
```
-------------------------
|   4 3 | 7     | 9   8 |
|     5 |   3   |       |
|   1   |       | 3     |
-------------------------
| 6     |   2 7 |       |
| 4   7 |       | 1   3 |
|       | 5 4   |     9 |
-------------------------
|     2 |       |   3   |
|       |   5   | 4     |
| 5   4 |     1 | 2 6   |
-------------------------
```

**Output**
```
-------------------------
| 2 4 3 | 7 1 6 | 9 5 8 |
| 9 8 5 | 2 3 4 | 7 1 6 |
| 7 1 6 | 8 9 5 | 3 4 2 |
-------------------------
| 6 3 9 | 1 2 7 | 5 8 4 |
| 4 5 7 | 9 6 8 | 1 2 3 |
| 8 2 1 | 5 4 3 | 6 7 9 |
-------------------------
| 1 6 2 | 4 7 9 | 8 3 5 |
| 3 7 8 | 6 5 2 | 4 9 1 |
| 5 9 4 | 3 8 1 | 2 6 7 |
-------------------------
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
$ java -jar ./build/libs/Sudoku.jar
```