# Linespacer
In deze map staan verschillende versies van het Linespacer algoritme. Het Linespacer algoritme hebben wij zelf opgesteld. Het verschil tussen de verschillende Linespacer versies zit hem in het ordenen van de netlist, dit wordt in de verschillende versies op andere manieren gedaan.

Als het script klaar is met runnen, wordt er in hetzelfde mapje een CSV-file gevormd met de output. Ook wordt er een visualisatie getoond van de chip bestaande uit gates die verbonden zijn door middel van wires. De wires hebben verschillende kleuren en verbinden 2 gates met elkaar.

* linespacer_withzconstraints.py: In deze code zijn constraints toegevoegd met betrekking tot de z-coördinaat van de wires. Deze code werkt alleen niet voor het optimalisatieprobleem. In de andere Linespacer codes is deze constraint dus gedeeltelijk niet opgenomen.
* linespacer_xdirection.py: In deze code is de netlist geordend op basis van afstand tussen de gates in de x-richting. De netlist is gesorteerd van gates met een kleine afstand tussen elkaar in de x-richting to gates met een grote afstand in de x-richting.
* linespacer_ydirection.py: Deze versie van Linespacer sorteert de netlist op dezelfde manier als de bovenstaande Linespacer versie, maar dan gebaseerd op de afstand in de y-richting.
* linespacer.py: Deze versie van de Linespacer is de originele Linespacer. In dit algoritme wordt de netlist gesorteerd op basis van totale afstand tussen twee gates die verbonden moeten worden. De netlist wordt geordend van kleine afstand naar grote afstand.