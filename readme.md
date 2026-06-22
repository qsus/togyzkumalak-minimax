# Toguz kumalak minimax
Jednoduchá implementace hry Toguz kumalak a minimax algoritmu na zápočet programování na MFF UK.

Algoritmus rekuzivně prochází strom hry do pevně stanovené hloubky a vyhodnocuje pozici. V nejnižší úrovni stromu se vyhodnocení pozice určuje jako rozdíl počtu kuliček v pokladničkách jednotlivých hráčů.

## Pravidla
Kompletní pravidla naleznete na webu [mankala.cz](https://www.mankala.cz/toguz.php).

Základní princip: každý hráč má 9 jamek s kameny a pokladničku. Hráči se střídají a ve svém tahu vždy vyberou jednu ze svých jamek a kuličky z ní rozdají do ostatních jamek obou hráčů. Snaží se přitom získat kuličky do své pokladničky podle pravidla o vybrání kuliček z jamky nebo pomocí pastiček. Další pravidla upravují, jak se kuličky rozdávají, jak se tvoří pastička a co se děje se zbylými kuličkami na konci hry.

## Spuštění

```bash
python main.py
```

Ve výchozím stavu hrají dva počítače proti sobě. Oba hráče lze nezávisle přepnout mezi člověkem a počítačem pomocí proměnných `player1_AI` a `player2_AI` v souboru `main.py`.

Uživatel zadává číslo jamky od 1 do 9.
