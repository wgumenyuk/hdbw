package de.gumenyuk.sudoku;

/**
     Einstiegspunkt in das Programm zum Lösen von Sodokus.
*/
public class Main {
    /**
        Führt das Programm aus.
    */
    public static void main(String[] args) {
        Sudoku sudoku = new Sudoku(new int[][] {
            { 0, 4, 3, 7, 0, 0, 9, 0, 8 },
            { 0, 0, 5, 0, 3, 0, 0, 0, 0 },
            { 0, 1, 0, 0, 0, 0, 3, 0, 0 },
            { 6, 0, 0, 0, 2, 7, 0, 0, 0 },
            { 4, 0, 7, 0, 0, 0, 1, 0, 3 },
            { 0, 0, 0, 5, 4, 0, 0, 0, 9 },
            { 0, 0, 2, 0, 0, 0, 0, 3, 0 },
            { 0, 0, 0, 0, 5, 0, 4, 0, 0 },
            { 5, 0, 4, 0, 0, 1, 2, 6, 0 }
        });

        System.out.printf("Sudoku:\n%s\n", sudoku);

        boolean isSolvable = sudoku.solve();

        if(isSolvable) {
            System.out.printf("Lösung:\n%s", sudoku);
            return;
        }

        System.out.println("Sudoku ist nicht lösbar!");
    }
}