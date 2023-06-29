package de.gumenyuk.sudoku;

/**
    Sudoku-Löser.
*/
public class Sudoku {
    /**
        Zu lösendes Sudoku.
    */
    private final int[][] sudoku;

    /**
        Konstrurktor.
        @param sudoku Zu lösendes Sudoku.
    */
    public Sudoku(int[][] sudoku) {
        this.sudoku = sudoku;
    }

    /**
        Findet das nächste leere Feld.
        @return Das nächste leere Feld.
                Null, wenn keins mehr gefunden wird.
    */
    private int[] findEmptyCell() {
        for(int i = 0; i < 9; i++) {
            for(int j = 0; j < 9; j++) {
                if(this.sudoku[i][j] == 0) {
                    return new int[] { i, j };
                }
            }
        }

        return null;
    }

    /**
        Überprüft, ob das Einsetzen der Nummer an der gegebenen Stelle
        in Ordnung ist.
        @param number Einzusetzende Nummer.
        @param row Zeile.
        @param col Spalte.
        @return Ob das Einsetzen in Ordnung ist.
    */
    private boolean isValid(int number, int row, int col) {
        // Zeile überprüfen
        for(int i = 0; i < 9; i++) {
            if(this.sudoku[row][i] == number) {
                return false;
            }
        }

        // Spalte überprüfen
        for(int i = 0; i < 9; i++) {
            if(this.sudoku[i][col] == number) {
                return false;
            }
        }

        // 3x3-Matrix überprüfen
        int startRow = row - (row % 3);
        int startCol = col - (col % 3);

        for(int i = 0; i < 3; i++) {
            for(int j = 0; j < 3; j++) {
                int matrixRow = startRow + i;
                int matrixCol = startCol + j;

                if(this.sudoku[matrixRow][matrixCol] == number) {
                    return false;
                }
            }
        }

        return true;
    }

    /**
        Stellt das Sudoku als String dar.
        @return Repräsentation des Sudokus als String.
    */
    public String toString() {
        StringBuilder output = new StringBuilder();

        for(int i = 0; i < 9; i++) {
            if(i % 3 == 0) {
                output
                    .append("-".repeat(25))
                    .append("\n");
            }

            for(int j = 0; j < 9; j++) {
                if(j % 3 == 0) {
                    output.append("| ");
                }

                int cell = this.sudoku[i][j];

                if(cell != 0) {
                    output
                        .append(cell)
                        .append(" ");
                } else {
                    output.append("  ");
                }
            }

            output.append("|\n");
        }

        output
            .append("-".repeat(25))
            .append("\n");

        return output.toString();
    }

    /**
        Löst (falls möglich) das Sudoku rekursiv mit dem
        Backtracking-Algorithmus.
        @return Ob das Sudoku lösbar ist.
    */
    public boolean solve() {
        int[] emptyCell = this.findEmptyCell();

        if(emptyCell == null) {
            return true;
        }

        int row = emptyCell[0];
        int col = emptyCell[1];

        for(int i = 1; i <= 9; i++) {
            if(this.isValid(i, row, col)) {
                this.sudoku[row][col] = i;

                if(this.solve()) {
                    return true;
                }

                this.sudoku[row][col] = 0;
            }
        }

        return false;
    }
}