# Toguz kumalak minimax
Jednoduchá implementace hry Toguz kumalak a minimax algoritmu na zápočet programování na MFF UK.

Algoritmus rekuzivně prochází strom hry do pevně stanovené hloubky a vyhodnocuje pozici. V nejnižší úrovni stromu se vyhodnocení pozice určuje jako rozdíl počtu kuliček v pokladničkách jednotlivých hráčů.

## Pravidla
Kompletní pravidla naleznete na webu [mankala.cz](https://www.mankala.cz/toguz.php).

Základní princip: každý hráč má 9 jamek s kameny a pokladničku. Hráči se střídají a ve svém tahu vždy vyberou jednu ze svých jamek a kuličky z ní rozdají do ostatních jamek obou hráčů. Snaží se přitom získat kuličky do své pokladničky podle pravidla o vybrání kuliček z jamky nebo pomocí pastiček. Další pravidla upravují, jak se kuličky rozdávají, jak se tvoří pastička a co se děje se zbylými kuličkami na konci hry.

## Spuštění

```bash
python main.py <player1_depth | "human"> <player2_depth | "human">
```

Jako `player_depth` se zadává hloubka, do které má minimax algoritmus prohledávat strom hry. Pokud je zadáno `human`, hraje daný hráč ručně. Doporučená hloubka pro minimax algoritmus je 6; analýza prvních tahů pak trvá řádově sekundy.

Uživatel zadává číslo jamky od 1 do 9, přičemž horní řádek se počítá zprava doleva. Stav desky se vypisuje jako dva řádky důlků, na jejichž koncích je vypsán stav pokladničky. Jako důlek je vypsán počet kuliček v něm, respektive `_`, pokud je důlek pastičkou.
