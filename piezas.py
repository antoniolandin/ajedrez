import pygame


class Pieza:
    traducir_pieza = {
        "peon": "pawn",
        "torre": "rook",
        "alfil": "bishop",
        "caballo": "knight",
        "rey": "king",
        "reina": "queen"
    }

    traducir_color = {
        "negro": "black",
        "blanco": "white"
    }

    def __init__(self, pieza: str, color: str, casilla: tuple[int, int], estilo: str, escala: float):
        ruta = f"assets/chess{estilo}/{Pieza.traducir_color[color]}_{Pieza.traducir_pieza[pieza]}.png"
        self.tipo = pieza
        self.sprite = pygame.transform.scale_by(pygame.image.load(ruta), escala).convert_alpha()
        self.tam_x, self.tam_y = self.sprite.get_size()
        self.selecionada = False
        self.color = color
        self.escala = escala
        self.fila, self.columna = casilla
        self.movida = False

    def actualizar_posicion(self, tablero):
        x = tablero.borde * tablero.escala + tablero.x - self.tam_x // 2 + \
            (tablero.tam_casilla * tablero.escala) // 2 + self.columna * tablero.tam_casilla * tablero.escala
        y = tablero.borde * tablero.escala + tablero.y - self.tam_y // 2 + \
            (tablero.tam_casilla * self.escala) // 2 + self.fila * tablero.tam_casilla * tablero.escala
        self.posicion = (x, y)

    def mover(self, tablero, movimiento: tuple[int, int]):
        self.fila, self.columna = movimiento
        self.actualizar_posicion(tablero)

        if not self.movida:
            self.movida = True

    def dibujar(self, pantalla):
        pantalla.blit(self.sprite, self.posicion)

    def posibles_movimientos(self, tablero):
        posibles_movimientos = []
        for fila in range(tablero.num_filas):
            for columna in range(tablero.num_columnas):
                casilla = (fila, columna)
                if not self.casilla_ocupada(tablero, casilla):
                    posibles_movimientos.append(casilla)

        return posibles_movimientos

    def movimiento_legal(self, tablero, movimiento: tuple[int, int]):
        return movimiento in self.posibles_movimientos(tablero)

    def casilla_ocupada(self, tablero, casilla: tuple[int, int]):
        return casilla in tablero.piezas and tablero.piezas[casilla].color == self.color

    def __str__(self):
        return f"{self.tipo} {self.color}"


class Rey(Pieza):
    def __init__(self, color: str, casilla: tuple[int, int], estilo: str, escala: float):
        super().__init__('rey', color, casilla, estilo, escala)

    def posibles_movimientos(self, tablero):
        posibles_movimientos = []
        for fila in range(self.fila - 1, self.fila + 2):
            for columna in range(self.columna - 1, self.columna + 2):
                if 0 <= fila < tablero.num_filas and 0 <= columna < tablero.num_columnas:
                    casilla = (fila, columna)
                    if (fila != self.fila or columna != self.columna) and not self.casilla_ocupada(tablero, casilla):
                        posibles_movimientos.append(casilla)

        return posibles_movimientos


class Reina(Pieza):
    def __init__(self, color: str, casilla: tuple[int, int], estilo: str, escala: float):
        super().__init__('reina', color, casilla, estilo, escala)


class Peon(Pieza):
    def __init__(self, color: str, casilla: tuple[int, int], estilo: str, escala: float):
        super().__init__('peon', color, casilla, estilo, escala)

    def posibles_movimientos(self, tablero):
        posibles_movimientos = []
        if self.color == 'blanco':
            if self.fila - 1 >= 0:
                for columna in (self.columna - 1, self.columna + 1):
                    if 0 <= columna <= tablero.num_columnas:
                        casilla = (self.fila - 1, columna)
                        if casilla in tablero.piezas and tablero.piezas[casilla].color != self.color:
                            posibles_movimientos.append(casilla)

                if (self.fila - 1, self.columna) not in tablero.piezas:
                    posibles_movimientos.append((self.fila - 1, self.columna))

                if not self.movida and self.fila - 2 >= 0 and (self.fila - 2, self.columna) not in tablero.piezas:
                    posibles_movimientos.append((self.fila - 2, self.columna))

        elif self.color == 'negro':
            if self.fila + 1 < tablero.num_filas:
                for columna in (self.columna - 1, self.columna + 1):
                    if 0 <= columna <= tablero.num_columnas:
                        casilla = (self.fila + 1, columna)
                        if casilla in tablero.piezas and tablero.piezas[casilla].color != self.color:
                            posibles_movimientos.append(casilla)

                if (self.fila + 1, self.columna) not in tablero.piezas:
                    posibles_movimientos.append((self.fila + 1, self.columna))

                if not self.movida and self.fila + 2 >= 0 and (self.fila + 2, self.columna) not in tablero.piezas:
                    posibles_movimientos.append((self.fila + 2, self.columna))

        return posibles_movimientos


class Alfil(Pieza):
    def __init__(self, color: str, casilla: tuple[int, int], estilo: str, escala: float):
        super().__init__('alfil', color, casilla, estilo, escala)


class Caballo(Pieza):
    def __init__(self, color: str, casilla: tuple[int, int], estilo: str, escala: float):
        super().__init__('caballo', color, casilla, estilo, escala)


class Torre(Pieza):
    def __init__(self, color: str, casilla: tuple[int, int], estilo: str, escala: float):
        super().__init__('torre', color, casilla, estilo, escala)

    def posibles_movimientos(self, tablero):
        posibles_movimientos = []

        for indice, rangos in enumerate((
                (range(self.fila + 1, tablero.num_filas), range(self.fila - 1, -1, -1)),
                (range(self.columna + 1, tablero.num_columnas), range(self.columna - 1, -1, -1))
        )):
            for rango in rangos:
                for i in rango:
                    if indice == 0:
                        casilla = (i, self.columna)
                    elif indice == 1:
                        casilla = (self.fila, i)

                    if casilla not in tablero.piezas or (casilla in tablero.piezas and tablero.piezas[casilla].color != self.color):
                        posibles_movimientos.append(casilla)

                    if (casilla in tablero.piezas):
                        break

        return posibles_movimientos
