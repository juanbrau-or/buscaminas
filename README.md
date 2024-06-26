# buscaminas-terminal

Este programa permite jugar buscaminas clásico desde la terminal utilizando python básico, funciona a base de comandos de teclado y un sistema coordenado, puede personalizarse desde el archivo main.py, pudiendo tener un máximo de 26 filas (pues éstas son identificadas con letras), y un número infinito de columnas. Al inicio del juego se puede elegir obtener una ayuda inicial, con la que se hace clic sobre una casilla en blanco que descubre varias casillas.

## Consideraciones

El programa utiliza una BFS (Breadth First Search) para expandir el tablero cuando se hace clic sobre una casilla en blanco.
La única librería utilizada es random, que permite generar números aleatorios para la colocación de las minas.
Cuando se utiliza la ayuda inicial, el programa busca la casilla en blanco que descubre más casillas.
El programa detecta comandos incorrectos, indicándole al usuario cuándo fue introducido un comando inválido.
