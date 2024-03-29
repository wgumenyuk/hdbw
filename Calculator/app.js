const setup = () => {
    const display = document.getElementById("calculator__display");
    const buttons = document.querySelectorAll(".calculator__button[value]");
    const buttonClear = document.getElementById("calculator__button-clear");
    const buttonAns = document.getElementById("calculator__button-ans");
    const buttonParentheses = document.getElementById("calculator__button-parentheses");
    const buttonEquals = document.getElementById("calculator__button-equals");

    let input = "";
    let ans = "";
    let isParenthesesOpen = false;

    // Event-Listener für alle Knöpfe mit "value"-Attribut hinzufügen
    for(const button of buttons) {
        button.addEventListener("click", () => {
            input += button.value;
            display.innerText += button.dataset.displayValue || button.value;
            scrollDisplay();
        });
    }

    /**
        Zählt die Anzahl der Nachkommastellen.
    */
    const countDecimals = (number) => {
        if(Math.floor(number) === number) return 0;
        return number.toString().split(".")[1]?.length || 0;
    };

    /**
        Verschiebt die Ansicht im Display ganz nach rechts.
    */
    const scrollDisplay = () => {
        display.scrollBy({ left: display.offsetWidth, behavior: "smooth" });
    };

    /**
        Setzt den Taschenrechner zurück.
    */
    const clear = () => {
        input = "";
        isParenthesesOpen = false;
        display.innerText = input;
    };

    /**
        Fügt, falls vorhanden, das vorherige Ergebnis ein. 
    */
    const addAns = () => {
        if(!ans) return;
        input += ans;
        display.innerText = input;
        scrollDisplay();
    };

    /**
        Öffnet und schließt Klammern.
    */
    const toggleParentheses = () => {
        const char = (isParenthesesOpen) ? ")" : "("; 
        
        input += char;
        display.innerText += char;

        isParenthesesOpen = !isParenthesesOpen;
    };

    /**
        Berechnet die eingegebene Funktion.
    */
    const calculate = () => {
        try {
            let result = eval(input);
            
            // Nur Zahlen als Ergebnis akzeptieren
            if(typeof result !== "number") {
                throw null;
            }

            // Nachkommastellen kürzen, falls mehr als 2
            if(countDecimals(result) > 2) {
                result = result.toFixed(2);
            }

            input = result.toString();
            ans = result.toString();

            display.innerText = result;
            scrollDisplay();
        } catch(error) {
            display.innerText = "Error";
            input = "";
        }
    };

    buttonClear.addEventListener("click", clear);
    buttonAns.addEventListener("click", addAns);
    buttonParentheses.addEventListener("click", toggleParentheses);
    buttonEquals.addEventListener("click", calculate);
};

window.addEventListener("load", setup);