import random
from datetime import datetime

def mostrarReglas():
    print("\n\tPASOS PARA JUGAR")
    print("1. Seleccionar la opción nuevo juego de lo contrario no podrá disfrutar la experiencia 🥲")
    print("2. Registrar jugadores (minímo 2 jugadores) sino no habra alguien con quien jugar 😅")
    print("3. Seleccionar la opción iniciar juego teniendo en cuenta los requisitos anteriores 😎")
    print("4. A DISFRUTAR!!! 😁")
    print("\n\tREGLAS: ")
    print("1. Lanzar el dado")
    print("2. LLegar a la casilla numero 30")
    print("3. Eventos y efecto del juego:")
    reglas = [
        {
            "obstaculo/evento": "Trampa de arena",
            "rango": "5-10",
            "efecto": "Retrocede 2 casilleros"
        },
        {
            "obstaculo/evento": "Canonazo",
            "rango": "11-18",
            "efecto": "Pierde un turno"
        },  
        {
            "obstaculo/evento": "Cofre de oro",
            "rango": "19-24",
            "efecto": "Avanza 4 casilleros extra"
        },
        {
            "obstaculo/evento": "Kraken",
            "rango": "25-29",
            "efecto": "Dado: impar = pierde, par = retrocede al inicio"
        }
    ]
    print("   ------------------------------------------------------------------------------")
    print(f"   {'Obstaculo/Evento':16} | {'Rango':5} | {'Efecto'}")
    print("   ------------------------------------------------------------------------------")
    for regla in reglas:
        print(f"   {regla['obstaculo/evento']:16} | {regla['rango']:5} | {regla['efecto']}")
    print("   ------------------------------------------------------------------------------")
    print("4. Si escribe 'n' en el momento de su turno, se conciderará como abandonó del juego")

def mensaje(modo, mensaje):
    if modo == "exito":
        return print(f"✅ EXITO, {mensaje}")
    elif modo == "alerta":
        return print(f"❕ ALERTA, {mensaje}")
    elif modo == "error":
        return print(f"❌ ERROR, {mensaje}")

def creaTablero():
    tablero = list()
    for i in range(0,30):
        tablero.append(random.randint(0,1))
    return tablero

def generaID(jugador):
    codigo = len(jugador) + 1
    codigo = str(codigo)
    if len(codigo) == 1:
        codigo = f"00{codigo}"
    elif len(codigo) == 2:
        codigo = f"0{codigo}"
    return codigo

def validaCaracter(modo, mensage, min = 0, max = 0):
    try:
        if modo == "strMin":
            while True:
                valor = input(f"Ingrese su {mensage}: ")
                if min <= len(valor):
                    break
                mensaje("alerta", f"el número de caracteres de {mensage} debe ser mayor a {min}")
        elif modo == "int":
            while True:
                valor = int(input(f"Ingrese su {mensage}: "))
                if min <= valor <= max:
                    break
                mensaje("alerta", f"{valor} esta en el rango de ({min}-{max})")
        elif modo == "confirma":
            while True:
                valor = input(mensage)
                if valor in ['y', 'n']:
                    break
                mensaje("alerta", f"Debe ingresar 'y o 'n")
        return valor
    except ValueError:
        mensaje("error", "Ingrese una opción valida!!!")

def ingresarJugador(jugadores):
    igual = True
    while igual:
        username = validaCaracter("strMin", "nombre de usuario", 2)
        igual = False
        for i in jugadores.values():
            if i["username"] == username:
                igual = True
                break
        if igual:
            mensaje("alerta", "ese nombre de ususario ya esta en uso")
    edad = validaCaracter("int", "edad", 5, 90)
    codigo = generaID(jugadores) 
    jugadores[codigo] = {
        "username" : username,
        "edad" : edad,
    }
    print()
    mensaje("exito", "se creo el usuario")
    print(f"Codigo del jugador: {codigo}")
    print(f"Username del jugador: {username}")
    print(f"Edad del jugador: {edad}\n")

def nuevoJuego():
    tablero = creaTablero()
    jugadores = dict()
    juego = dict()
    mensaje("exito", "se generó un nuevo juego")
    return tablero, jugadores, juego

def actualizaPos(juego, usuario, casillas):
    antiguaPos = juego[usuario]["posicion"]
    condicion = juego[usuario]["condicion"]
    pos = antiguaPos + casillas
    if pos >= 30:
        pos = 30
    if pos <= 0:
        pos = 0
    juego[usuario] = {
        "posicion" : pos,
        "condicion" : condicion,
    }
    print(f"Su posicion actual es la casilla {pos}")
    if pos >= 30:
        actualizaCondicion(juego, usuario, "gana")

def actualizaCondicion(juego, usuario, condicion):
    posicion = juego[usuario]["posicion"]
    juego[usuario] = {
        "posicion" : posicion,
        "condicion" : condicion,
    }

def validaKraken(dado, juego, usuario):
    pos = juego[usuario]["posicion"]
    if dado % 2 == 0:
        print(f"{usuario} retrocede al inicio")
        actualizaPos(juego, usuario, -pos)
    else:
        print(f"{usuario} fue eliminado por el Kraken")
        actualizaCondicion(juego, usuario, "pierde")

def eventosJuego(juego, usuario, tablero, dado):
    actualizaPos(juego, usuario, dado)
    pos = juego[usuario]["posicion"]
    evento = False
    if tablero[pos - 1] == 1:
        evento = True
    if evento:
        if 5 <= pos <= 10:
            print(f"{usuario} se encuentra en una trampa de arena, retrosede 2 espacios")
            actualizaPos(juego, usuario, -2)
        elif 11 <= pos <= 18:
            print(f"{usuario} fue dado por un cañonazo, pierde un turno")
            actualizaCondicion(juego, usuario, "cañonazo")
        elif 19 <= pos <= 24:
            print(f"{usuario} se encontro un cofre del oro, avanza 4 espacios")
            actualizaPos(juego, usuario, 4)
        elif 25 <= pos <= 29:
            print(f"{usuario} se encontró al Kraken")
            print("Debe tirar los dados para saber su destino")
            print("Impar - Muere")
            print("Par - Retrocede al inicio")
            confirmaDado = input(f"Jugador {usuario} tire los dados (y = si , n = no):").lower()
            if confirmaDado == "y":
                dado = random.randint(1,6)
                validaKraken(dado, juego, usuario)
            else:
                actualizaCondicion(juego, usuario, "abandona")

def calculaDuracion(segundos):
    hora = 0
    minutos = 0
    while segundos>=3600:
        hora+=1
        segundos-=3600
    while segundos>=60:
        minutos+=1
        segundos-=60
    return f"{hora} horas, {minutos} minutos y {segundos} segundos"

def actualizaEstadistica(estadistica, juego, usuario, jugadores, inicio):
    final = datetime.now()
    duracion = final - inicio
    if juego[usuario]["condicion"] in ["abandona", "pierde", "gana"]:
        codigo = None
        for i, datos in jugadores.items():
            if datos["username"] == usuario:
                codigo = i
                break
        if codigo is None:
            return  
        condicion = juego[usuario]["condicion"]
        posicion = juego[usuario]["posicion"]
        estadistica[codigo] = {
            "username": usuario,
            "codigo": codigo,
            "posicion": posicion,
            "condicion": condicion,
            "duracion": calculaDuracion(int(duracion.total_seconds()))
        }

def muestraEstadisticas(estadisticas):
    print("ESTADISTICAS DEL JUEGO")
    print("----------------------------------------------------------------------------")
    print(f"{'Codigo':6} | {'Nombre':15} | {'Posicion':8} | {'Resultado':10} | {'Duracion'}")
    print("----------------------------------------------------------------------------")
    for datos in estadisticas.values():
        print(f"{datos['codigo']:6} | {datos['username']:15} | {datos['posicion']:8} | {datos['condicion']:10} | {datos['duracion']}")
    print("----------------------------------------------------------------------------")


def iniciarJuego(tablero, jugadores, juego):
    try:
        if len(jugadores) <= 1:
            mensaje("error", "debe ingresar jugadores antes de jugar")
            return False
        else:
            print("Orden de juego:")
            c = 1
            for i in jugadores.keys():
                print(f"{c}. {jugadores[i]['username']}")
                juego[jugadores[i]["username"]] = {
                            "posicion" : 0,
                            "condicion" : "vivo",
                            "turno" : "si"
                           }
                c+=1
            mantieneJuego = True
            estadisticas = dict()
            inicio = datetime.now()
            for i, num in enumerate(tablero):
                if num == 1:
                    print(f"C{i + 1}-True",end=" ")
                else:
                    print(f"C{i + 1}-False",end=" ")
            print()
            eliminados = list()
            while mantieneJuego:
                for i in juego.keys():
                    if len(eliminados) > 0:
                        if i not in eliminados:
                            actualizaCondicion(juego, i, "gana")
                            mantieneJuego = False
                    if juego[i]["condicion"] == "gana":
                        actualizaEstadistica(estadisticas, juego, i, jugadores, inicio)
                        print(f"EL jugador {i} gana la partida")
                        mantieneJuego = False
                        break
                    if juego[i]["condicion"] == "cañonazo":
                        actualizaCondicion(juego, i, "vivo")
                        continue
                    if i in eliminados:
                        continue
                    confirmaDado = input(f"\nJugador '{i}' tire los dados (y = si , n = no):").lower()
                    if confirmaDado == "y":
                        dado = random.randint(1,6)
                        print(f"{i} avanza {dado} espacios")
                        eventosJuego(juego, i, tablero, dado)
                    else:
                        print(f"El jugador {i} abandona la partida")
                        actualizaCondicion(juego, i, "abandona")
                    if juego[i]["condicion"] == "pierde" or juego[i]["condicion"] == "abandona":
                        actualizaEstadistica(estadisticas, juego, i, jugadores, inicio)
                        eliminados.append(i)
            return estadisticas
    except ValueError:
        mensaje("error", "Ingrese una opción valida!!!")

def menu():
    try:
        tablero = None
        jugadores = None
        juego = None
        estadisticas = None
        opc = 0
        while opc != 6:
            print("\tEL TESORO PIRATA",end="\n")
            print("1. Instrucciones de como jugar")
            print("2. Ingresar jugador")
            print("3. Nuevo juego")
            print("4. Iniciar juego")
            print("5. Ver estadísticas")
            print("6. Salir")
            opc = int(input("Ingrese su opción: "))
            match opc:
                case 1:
                    mostrarReglas()
                case 2:
                    if jugadores is None:  
                        mensaje("error", "Primero debe crear un nuevo juego con la opción 3")
                    else:
                        ingresarJugador(jugadores)
                case 3:
                    tablero, jugadores, juego = nuevoJuego()
                case 4:
                    if jugadores is None or len(jugadores) <2:
                        mensaje("error", "Primero debe ingresar minimo 2 jugadores para empezar con la opción 2")
                    else:
                        estadisticas = iniciarJuego(tablero, jugadores, juego)
                case 5:
                    if estadisticas is None:
                        mensaje("error", "Primero debe jugar para recibir las estadisticas con la opcion 4")
                    else:
                        muestraEstadisticas(estadisticas)
                case 6:
                    print("Saliendo...")
                case other:
                    mensaje("error", "ingrese una opcion válida")
    except ValueError:
        mensaje("error", "Ingrese una opción valida!!!")

menu()