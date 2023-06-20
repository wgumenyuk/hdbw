package de.gumenyuk.magic_square;

/**
    Magisches Quadrat.
*/
public class MagicSquare {
    /**
        Anzahl der Zeilen und Spalten.
    */
    private final int n;

    /**
        Magisches Quadrat.
    */
    private final int[][] square;

    /**
        Index der aktuellen Zeile.
    */
    private int currentRow;

    /**
        Index der aktuellen Spalte.
    */
    private int currentCol;

    /**
        Konstruktor.
        @param n Anzahl der Zeilen und Spalten.
    */
    public MagicSquare(int n) {
        this.n = n;
        this.square = new int[n][n];

        // Startposition festlegen
        this.currentRow = 0;
        this.currentCol = (int) Math.floor(n / 2f);
    }

    /**
        Ermittelt die Indexe des nächsten Feldes.
    */
    private void gotoNextField() {
        int nextRow = (this.currentRow - 1 < 0) ?
            this.n - 1 :
            this.currentRow - 1;

        int nextCol = (this.currentCol + 1) % this.n;

        boolean isOccupied = (this.square[nextRow][nextCol] != 0);

        if(isOccupied) {
            nextRow = (this.currentRow + 1) % this.n;
            nextCol = this.currentCol;
        }

        this.currentRow = nextRow;
        this.currentCol = nextCol;
    }

    /**
        Stellt das magische Quadrat als formatierten String dar.
    */
    public String toString() {
        StringBuilder output = new StringBuilder();

        for(int i = 0; i < this.n; i++) {
            for(int j = 0; j < this.n; j++) {
                int number = this.square[i][j];

                output
                    .append(String.format("%2d", number))
                    .append(" ");
            }

            if(i < this.n - 1) {
                output.append('\n');
            }
        }

        return output.toString();
    }

    /**
        Löst das magische Quadrat.
    */
    public void solve() {
        for(int i = 1; i <= Math.pow(this.n, 2); i++) {
            this.square[this.currentRow][this.currentCol] = i;
            this.gotoNextField();
        }
    }
}