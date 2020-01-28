# Project Programmeertheorie
### Chips & Circuits
Dit project bestaat uit een optimalisatieprobleem dat moet worden opgelost aan de hand van het testen van verschillende algoritmes. De visualisatie van dit probleem wordt als volgt geïnterpreteerd: er is een chip, die bestaat uit een grid, waar gates op liggen die verbonden moeten worden met elkaar door middel van draden (wires). Welke gates met elkaar verbonden moeten worden en de locaties van de gates zijn van tevoren vastgelegd en gegeven. Het doel van dit project is om de gates op zo'n manier met elkaar te verbinden dat de totale lengte van alle draden bij elkaar opgeteld zo kort mogelijk is.

## Getting started
### Vereisten
De codebase is volledig geschreven in Python. In het bestand requirements.txt is aangegeven welke packages geïnstalleerd moeten worden om alle codes goed te kunnen laten runnen. De packages kunnen geïnstalleerd worden door de volgende command line in te typen in de terminal:

```
pip install -r requirements.txt
```
Of, bij een versie van pip3:
```
pip3 install -r requirements.txt
```

### Structuur
De repository bestaat uit drie belangrijke folders: code, data en linespacer.

#### code
In de folder "code" staat alle belangrijke code opgeslagen. Deze folder bestaat ook weer uit vier belangrijke folders: algorithms, classes, functions en visualisation.

* algorithms: Hierin staan de codes voor een aantal verschillende algoritmes waarmee het optimalisatieprobleem is getest.
* classes: Hierin staan de classes gedefinieerd die gebruikt worden om objecten mee op te slaan.
* functions: Hierin zijn functies gedefinieerd die aangeroepen worden in de Python codes.
* visualisation: Bevat een Python file die een plot creëert van de resultaten.

#### data
In de folder "data" staan alle bestanden die de nodige data bevatten om de algoritmes mee te testen. De databestanden bevatten netlists, die aangeven welke gates met elkaar verbonden moeten worden, en coördinaten van de gates.

#### linespacer
"Linespacer" is een algoritme dat Izhar, Tom en Julia zelf hebben geschreven. In de folder "linespacer" staan de codes voor dit algoritme samen met de output die bij het runnen van het algoritme wordt gevormd.

### Test
Er zijn twee algoritmes die goed zijn uitgewerkt voor dit optimalisatieprobleem: A-star en Linespacer. A-star kan gerund worden vanuit de huidige directory. Om het A-star algoritme te laten runnen moet de main.py file worden aangeroepen op de volgende manier:
```
python main.py
```

Om Linespacer algoritmes te kunnen runnen, moet eerst de directory worden veranderd naar /linespacer. Vervolgens moet het specifieke linespacer algoritme worden aangeroepen in de terminal om dit algoritme te laten runnen. Om als voorbeeld de standaard linespacer te nemen, moet de volgende command line worden ingevoerd in de terminal:
```
python linespacer.py
```

## Auteurs
* Izhar Hamer
* Tom Kamstra
* Julia Linde
* Team: De mandarijntjes
