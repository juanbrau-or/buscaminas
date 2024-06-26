import random

# se declaran las variables globales, como la altura, ancho y la cantidad de minas

# 18 14 40
width = 18
height = 14
mines = 40
matrix_user = []
matrix_program = []

# los siguientes arreglos son para revisar las las casillas alrededor de otra
dir_x = [-1, 0, 1]
dir_y = [-1, 0, 1]

def restart():
    # borra todas las minas y vacia los numeros
    for i in range(0, height, 1):
        for j in range(0, width, 1):
            matrix_user[i][j] = '.'
            matrix_program[i][j] = 0

    # vuelve a poner las minas
    cnt = 0
    while cnt < mines:
        # elige coordenadas random x y y
        x = random.randint(0, width - 1)
        y = random.randint(0, height - 1)
        # si ya hay una mina en esa posicion lo vuelve a calcular
        if matrix_program[y][x] == -1:
            continue
        else:
            matrix_program[y][x] = -1
            cnt += 1

    # calcula cuantas minas hay alrededor de una casilla
    for i in range(0, height, 1):
        for j in range(0, width, 1):
            if matrix_program[i][j] == -1:
                continue
            else:
                #nuevamente se revisan las casillas alrededor de la que estamos calculando
                for a in range(0, 3, 1):
                    for b in range(0, 3, 1):
                        y = i+dir_x[a]
                        x = j+dir_y[b]
                        # si hay una mina alrededor le sumamos uno al calculo de minas
                        if 0 <= x < width and 0 <= y < height and matrix_program[y][x] == -1:
                            matrix_program[i][j]+=1
    return


def create_game():
    # crea el tablero que se mostrara al jugador
    for i in range(0, height, 1):
        matrix_user.append([])
        for j in range(0, width, 1):
            matrix_user[i].append(".")

    # crea el tablero de referencia con la solucion
    for i in range(0, height, 1):
        matrix_program.append([])
        for j in range(0, width, 1):
            matrix_program[i].append(0)

    # elegir las posiciones de las minas
    restart()


def print_user():
    i_row = ord('A')
    # imprime los numeros de referencia para el usuario
    for i in range(0, width+1, 1):
        if i == 0:
            print(" ", end = "  ")
        # si es menor a 10 imprime un espacio extra (por la falta de unidades)
        elif i <= 9:
            print(i, end = "  ")
        else:
            print(i, end = " ")
    print()

    # va imprimiendo la letra de coordenada y cada fila
    for i in range(0, height, 1):
        # imprime la letra de la fila usando i_row
        print(chr(i_row), end = "  ")
        # suma 1 a la letra de la fila actual
        i_row+=1
        for j in range(0, width, 1):
            print(matrix_user[i][j], end = "  ")
        print()

    return


def print_program():
    # esta funcion es para debuggear, pues imprime el tablero respuesta
    for i in range(0, height, 1):
        for j in range(0, width, 1):
            # si hay una mina imprime un #
            if matrix_program[i][j] == -1:
                print("#", end = " ")
            # si no hay mina imprime el numero que corresponde
            else:
                print(matrix_program[i][j], end = " ")
        print()
    return


def game_lost():
    # imprime el tablero como estaba revelando las casillas con minas
    for i in range(0, height, 1):
        for j in range(0, width, 1):
            # si en una casilla habia una mina la cambia por una 'X'
            if matrix_program[i][j] == -1:
                matrix_user[i][j] = 'X'
    print_user()
    print("Has perdido")
    return


def game_won():
    # imprime el tablero reemplazando las minas con #
    for i in range(0, height, 1):
        for j in range(0, width, 1):
            if matrix_program[i][j] == -1:
                matrix_user[i][j] = '#'
    print_user()
    print("Has ganado")
    return


def bfs(a, b):
    """
    esta funcion es para cuando se hace clic en una casilla en blanco, basicamente "expande" las casillas
    reveladas mientras mientras haya casillas blancas, es una tecnica llamada bfs, en la que se tiene una
    cola en la que se agregan las casillas que hay que expandir
    """
    # agrega la coordenada de la primer casilla a las casillas a expandir
    queue = [[a, b]]
    # cnt es para contar cuantas casillas nuevas han sido reveladas
    cnt = 1
    # el ciclo se acaba cuando no quedan casillas por expandir
    while queue:
        # elimina la casilla que se va a expandir de la fila y guarda sus coordenadas
        node = queue.pop(0)
        a = node[0]
        b = node[1]
        # si era una casilla en blanco la cambia por un espacio en la matriz del usuario
        if matrix_program[a][b] == 0:
            matrix_user[a][b] = ' '
        # si era una casilla con numero, lo muestra al usuario y NO la agrega a la lista de casillas por expandir
        else:
            matrix_user[a][b] = chr(matrix_program[a][b]+ord('0'))
            # el continue es para que no la agregue a la lista
            continue
        # se revisan las casillas de alrededor
        for i in range(0, 3, 1):
            for j in range(0, 3, 1):
                x = b+dir_x[j]
                y = a+dir_y[i]
                # si las coordenadas estan dentro del tablero y no han sido exploradas, se agregan a la cola
                if 0 <= x < width and 0 <= y < height and matrix_user[y][x] == '.':
                    # se marcan con f para marcarlas como "visitadas"
                    matrix_user[y][x] = 'f'
                    # se agregan a la lista de casillas a expandir
                    queue.append([y, x])
                    cnt+=1

    # regresa la cantidad de casillas descubiertas
    return cnt


def clic(a, b):
    # esta funcion regresa dos parametros, el primero indica si el usuario "sobrevivio", y el segundo cuantas casillas
    # se descubrieron

    # si ya se ha hecho clic en esa casilla no hace nada
    if matrix_user[a][b] != '.':
        return True, 0

    # si la casilla tiene un numero, solamente revela ese numero
    if 1 <= matrix_program[a][b] <= 8:
        matrix_user[a][b] = chr(matrix_program[a][b]+ord('0'))
        return True, 1

    # si el usuario hizo clic en una mina, perdio
    if matrix_program[a][b] == -1:
        # se imprime el tablero de perdedor
        game_lost()
        # indica al programa que el usuario perdio
        return False, 0

    # si se llego aqui es que se hizo clic en una casilla en blanco, asi que se llama a la funcion correspondiente
    return True, bfs(a, b)


def right_clic(a, b):
    # esta funcion sirve para cuando se hace clic derecho sobre una casilla

    # si el usuario hizo clic en una casilla que ya ha descubierto, no hace nada
    if matrix_user[a][b] != '.' and matrix_user[a][b] != '#':
        return 0

    # si se hizo clic sobre una bandera, la quita
    if matrix_user[a][b] == '#':
        matrix_user[a][b] = '.'
        return -1
    # si llego aqui significa que hizo clic en una casilla vacia, asi que pone una bandera ('#')
    else:
        matrix_user[a][b] = '#'
        return 1


def coordinate(command):
    """
    esta funcion interpreta los comandos del usuario y regresa 3 parametros: el primero indica el tipo de accion que
    se tiene que hacer (0 para comando incorrecto, 1 para un clic, 2 para activar modo banderas y 3 para desactivar el
    modo banderas, el segundo parametro que regresa es la coordenada x del clic y el tercero la coordenada y
    """

    if command == "give_me_the_answer_bitch":
        print_program()

    # si no se ingreso nada, regresa que se ingreso un comando incorrecto
    if len(command) == 0:
        return 0, 0, 0
    # si se ingreso un comando de una letra, revisa si se esta activando o desactivando el modo bandera
    if len(command) == 1:
        # si se cumple este if es porque se activo el modo banderas
        if command[0] == 'f' or command[0] == 'F':
            return 2, 0, 0
        # si se cumple este if se desactivo el modo banderas
        elif command[0] == 'n' or command[0] == 'N':
            return 3, 0, 0
        # si no fue ninguno de los dos entonces es un comando incorrecto
        return 0, 0, 0

    # si el usuario ingreso la coordenada en minusculas las vuelve mayusculas
    if 'a' <= command[0] <= 'z':
        x = list(command)
        command = command.replace(command[0], x[0].upper(), 1)

    # si la letra de la coordenada no esta en el abecedario es un comando incorrecto
    if 'A' > command[0] or 'Z' < command[0]:
        return 0, 0, 0

    # guarda la letra de la fila del comando
    a_ = command[0]
    # elimina la letra del comando
    command = command.replace(str(a_),"",1)
    # si el usuario ingreso un espacio entre la fila y columna lo elimina
    command = command.strip()
    n = len(command)
    # si alguno de los caracteres del comando no es un digito entonces detecta un comando incorrecto
    for i in range(0, n, 1):
        if command[i] < '0' or command[i] > '9':
            return 0, 0, 0
    # vuelve la string a un numero y le resta uno para que este indexado en 0
    b = int(command)-1
    # vuelve la coordenada de letra a numero
    a = ord(a_)-ord('A')

    # si la casilla no esta dentro del tablero detecta un comando incorrecto
    if not(0 <= a < height and 0 <= b < width):
        return 0, 0, 0
    # si se llego a este punto regresa que se hizo clic, y las coordenadas del clic
    return 1, a, b


def keep_going():
    # esta funcion pregunta al usuario si se quiere seguir jugando
    while True:
        com = input("¿Desea continuar? s/n, y/n: ")
        # convierte el comando a mayusculas para simplificar
        com = com.upper()
        # si el comando es no, regresa falso
        if com == "N" or com == "NO":
            return False
        # si el comando es afirmativo, regresa true
        elif com == "YES" or com == "Y" or com == "SI" or com == "S":
            return True
        # si no ingreso a ninguno de los anteriores, detecta un comando incorrecto
        print("Comando incorrecto, intente de nuevo")


def initial_help():
    repeat = True
    """
    pregunta si quiere una ayuda inicial, regresa un parametro que es la cantidad de casillas reveladas, la ayuda
    inicial consiste en hacer clic sobre una casilla en blanco, para que se "expanda" a otras casillas, esta funcion
    hace clic sobre la casilla tal que al hacer clic en ella se revele la mayor cantidad de casillas
    """

    # mientras no introduzca un comando valido se repite
    while repeat:
        com = input("¿Desea ayuda inicial? s/n, y/n: ")
        # convierte la string a mayusculas para que sea mas facil la comparacion
        com = com.upper()
        # si el usuario dijo que no queria ayuda inicial acaba la funcion
        if com == "NO" or com == "N":
            return 0
        elif com == "YES" or com == "Y" or com == "S" or com == "SI":
            break
        print("Comando incorrecto, intente de nuevo")

    """crea una matriz de visitados, para ver para cuales casillas ya ha sido calculada la cantidad de casillas que
    revelan"""
    visit = []
    for i in range(0, height, 1):
        visit.append([])
        for j in range(0, width, 1):
            visit[i].append(False)

    # se crean variables de maximos, para guardar la casilla sobre la que hay que hacer clic y cuantas casillas revela
    max_visit = max_i = max_j = 0

    # los for son para recorrer el tablero
    for a_ in range(0, height):
        for b_ in range(0, width):
            # si ya han sido calculado para esta casilla o no es una casilla en blanco, se la salta
            if visit[a_][b_] or matrix_program[a_][b_] != 0:
                continue

            queue = [[a_, b_]]
            cnt = 1
            """
            Si es una casilla en blanco, realiza una bfs para revisar cuantas casillas son reveladas al hacer clic en
            ella, y marca todas las casillas que visita como visitadas, pues si estan en el mismo grupo de casillas
            en blanco, da igual sobre cual se haga clic, entonces esto es mas para no hacer muchas veces lo mismo
            """
            while queue:
                node = queue.pop(0)
                a = node[0]
                b = node[1]
                if matrix_program[a][b] != 0:
                    continue
                for i in range(0, 3, 1):
                    for j in range(0, 3, 1):
                        x = b + dir_x[j]
                        y = a + dir_y[i]
                        if 0 <= x < width and 0 <= y < height and not visit[y][x]:
                            visit[y][x] = True
                            queue.append([y, x])
                            cnt += 1

            # si las casillas reveladas son mas que las calculadas anteriormente guarda los nuevos valores maximos
            if cnt > max_visit:
                max_visit = cnt
                max_i = a_
                max_j = b_

    if max_visit == 0:
        for i in range(height):
            for j in range(width):
                if matrix_program[i][j] != -1:
                    clic(i, j)
                    return 1
        return 0

    # hace "clic" en la casilla vacia con la que se revelan mas casillas
    clic(max_i, max_j)

    # regresa el numero de casillas descubiertas
    return max_visit


def main():
    # crea las matrices y coloca las minas
    create_game()
    # esta variable indica cuantas casillas libres de minas han sido descubiertas
    free_cells = 0
    # indica si el modo bandera esta activado
    flag = False
    # indica si se hizo un cambio en el tablero y por lo tanto es necesario imprimirlo
    need_print = True
    # indica cuantas banderas ha puesto el usuario
    flags_set = 0
    # pregunta al usuario si quiere la ayuda inicial y de ser asi suma las casillas descubiertas
    free_cells+=initial_help()
    print("Para usar banderas ingresar 'f' y para descubrir una casilla ingresar 'n'")
    while True:
        # Si se hizo una modificacion al tablero se vuelve a imprimir
        if need_print:
            print("Banderas restantes: ", mines-flags_set)
            print_user()
        need_print = False
        # Obtiene el comando ingresado por el usuario
        com = input("Ingrese el comando a realizar: ")

        """c indica el tipo de comando que indico el usuario, 
        en caso de ser necesario a y b indican las coordenadas del clic"""
        c, a, b = coordinate(com)

        # c = 0 indica un comando invalido
        if c == 0:
            print("Comando incorrecto, intente de nuevo")
            continue
        # c = 2 indica que el usuario activo el modo banderas
        if c == 2:
            flag = True
        # c = 3 indica que el usuario desactivo el modo banderas
        elif c == 3:
            flag = False
        # c = 1 significa que se hizo clic sobre una casilla
        else:
            if flag:
                # si se hizo clic con el modo bandera se manda llamar a la funcion correspondiente
                flags_set+=right_clic(a, b)
                # como se hizo cambio en el tablero se necesita imprimir
                need_print = True
            else:
                # la variable survived guarda si el usuario perdio o no y discovered las nuevas casillas descubiertas
                survived, discovered = clic(a, b)
                # como se hizo clic entonces el tablero cambio y se necesita volver a imprimir el tablero
                need_print = True
                # si el usuario no ha perdido se hacen los cambios al tablero que se necesitan
                if survived:
                    # se suman las casillas descubiertas en el ultimo clic
                    free_cells+=discovered
                    # si las casillas que descubrio el usuario son todas las que no tienen minas significa que gano
                    if free_cells == width*height-mines:
                        game_won()
                        # se pregunta al usuario si quiere seguir jugando
                        if keep_going():
                            # en caso de que si se reinician todos los valores y las variables creadas al inicio
                            restart()
                            free_cells = 0
                            flag = False
                            need_print = True
                            flags_set = 0
                            free_cells+=initial_help()
                            print("Para usar banderas ingresar 'f' y para descubrir una casilla ingresar 'n'")
                        # si no quiere seguir jugando se rompe el ciclo para acabar el juego
                        else:
                            break
                # si se entra aqui significa que el usuario perdio
                else:
                    # se le pregunta al usuario si quiere seguir jugando
                    if keep_going():
                        # si se quiere seguir jugando se reinician todos los valores creados al inicio
                        restart()
                        free_cells = 0
                        flag = False
                        need_print = True
                        flags_set = 0
                        free_cells+=initial_help()
                        # se vuelven a dar las instrucciones
                        print("Para usar banderas ingresar 'f' y para descubrir una casilla ingresar 'n'")
                    # en caso de que no simplemente acaba el juego
                    else:
                        break
    return


main()
