const setup = () => {
    const display = document.getElementById("calculator__display");
    const buttons = document.querySelectorAll(".calculator__button[value]");
    const buttonClear = document.getElementById("calculator__button-clear");
    const buttonAns = document.getElementById("calculator__button-ans");
    const buttonEquals = document.getElementById("calculator__button-equals");

    let input = "";
    let ans = "";

    // Event-Listener für alle Knöpfe mit "value"-Attribut hinzufügen
    for(const button of buttons) {
        button.addEventListener("click", () => {
            input += button.value;
            display.innerText += button.dataset.displayValue || button.value;
        });
    }

    /**
        Zählt die Anzahl der Nachkommastellen.
    */
    const countDecimals = (number) => {
        if(Math.floor(number) === number) return 0;
        return number.toString().split(".")[1]?.length || 0;
    };

    const addAns = () => {
        if(!ans) return;
        input += ans;
        display.innerText = input;
    };

    /**
        Setzt den Taschenrechner zurück.
    */
    const clear = () => {
        input = "";
        display.innerText = input;
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
            display.scrollBy({ left: display.offsetWidth, behavior: "smooth" });
        } catch(error) {
            display.innerText = "Error";
            input = "";
        }
    };

    buttonClear.addEventListener("click", clear);
    buttonAns.addEventListener("click", addAns);
    buttonEquals.addEventListener("click", calculate);
};

window.addEventListener("load", setup);