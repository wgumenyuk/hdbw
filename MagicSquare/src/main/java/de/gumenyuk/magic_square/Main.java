package de.gumenyuk.magic_square;

/**
    Einstiegspunkt in das Programm zum Lösen von magischen
    Quadraten.
*/
public class Main {
    /**
        Druckt eine Anleitung zur Verwendung des Programmes
        aus.
    */
    private static void displayUsage() {
        String output =
            "Magic Square\n" +
            "Programm zum Lösen von magischen Quadraten.\n\n" +
            "SYNTAX:\n" +
            "  $ java -jar MagicSquare.jar [n]\n\n" +
            "ARGUMENTE:\n" +
            "  [n] Beliebige UNGERADE Zahl zwischen 2 und 10";

        System.err.println(output);
    }

    /**
        Führt das Programm aus.
    */
    public static void main(String[] args) {
        if(args.length == 0) {
            displayUsage();
            System.exit(1);
        }

        int n = 0;

        try {
            n = Integer.parseInt(args[0]);
        } catch(NumberFormatException e) {
            displayUsage();
            System.exit(1);
        }

        if(n % 2 == 0 || n < 2 || n > 10) {
            displayUsage();
            System.exit(1);
        }

        MagicSquare square = new MagicSquare(n);

        square.solve();

        System.out.println(square.toString());
    }
}