import pygame
import itertools


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
                if not self.movimiento_legal_base(tablero, casilla):
                    posibles_movimientos.append(casilla)

        return posibles_movimientos

    def movimiento_legal(self, tablero, movimiento: tuple[int, int]):
        return movimiento in self.posibles_movimientos(tablero)

    def movimiento_legal_base(self, tablero, casilla: tuple[int, int]):
        return (
            (self.fila != casilla[0] or self.columna != casilla[1])
            and (0 <= casilla[0] < tablero.num_filas and 0 <= casilla[1] < tablero.num_columnas)
            and not (casilla in tablero.piezas and tablero.piezas[casilla].color == self.color)
        )

    def movimiento_diagonal(self, tablero):
        posibles_movimientos = []

        for combinacion in itertools.product((1, -1), repeat=2):
            offset_fila, offset_columna = combinacion
            fila, columna = self.fila + offset_fila, self.columna + offset_columna
            while (0 <= fila < tablero.num_filas and 0 <= columna < tablero.num_columnas):
                casilla = (fila, columna)

                if self.movimiento_legal_base(tablero, casilla):
                    posibles_movimientos.append(casilla)

                if (casilla in tablero.piezas):
                    break

                fila = fila + offset_fila
                columna = columna + offset_columna

        return posibles_movimientos

    def movimiento_recto(self, tablero):
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

                    if self.movimiento_legal_base(tablero, casilla):
                        posibles_movimientos.append(casilla)

                    if (casilla in tablero.piezas):
                        break

        return posibles_movimientos

    def __str__(self):
        return f"{self.tipo} {self.color}".title()


class Rey(Pieza):
    def __init__(self, color: str, casilla: tuple[int, int], estilo: str, escala: float):
        super().__init__('rey', color, casilla, estilo, escala)

    def posibles_movimientos(self, tablero):
        posibles_movimientos = []
        for fila in range(self.fila - 1, self.fila + 2):
            for columna in range(self.columna - 1, self.columna + 2):
                casilla = (fila, columna)
                if self.movimiento_legal_base(tablero, casilla):
                    posibles_movimientos.append(casilla)

        return posibles_movimientos


class Reina(Pieza):
    def __init__(self, color: str, casilla: tuple[int, int], estilo: str, escala: float):
        super().__init__('reina', color, casilla, estilo, escala)

    def posibles_movimientos(self, tablero):
        return self.movimiento_diagonal(tablero) + self.movimiento_recto(tablero)


class Peon(Pieza):
    def __init__(self, color: str, casilla: tuple[int, int], estilo: str, escala: float):
        super().__init__('peon', color, casilla, estilo, escala)

    def posibles_movimientos(self, tablero):
        def aux(self, tablero, i):
            posibles_movimientos = []

            # movimiento diagonal
            for columna in (self.columna - 1, self.columna + 1):
                casilla = (self.fila + i, columna)
                if self.movimiento_legal_base(tablero, casilla) and casilla in tablero.piezas:
                    posibles_movimientos.append(casilla)

            # movimiento recto
            casilla = (self.fila + i, self.columna)
            if casilla not in tablero.piezas and self.movimiento_legal_base(tablero, casilla):
                posibles_movimientos.append(casilla)

            # doble salto
            if not self.movida:
                casilla = (self.fila + i * 2, self.columna)
                if self.movimiento_legal_base(tablero, casilla) and casilla not in tablero.piezas:
                    posibles_movimientos.append((self.fila + i * 2, self.columna))

            return posibles_movimientos

        if self.color == 'blanco':
            return aux(self, tablero, -1)
        elif self.color == 'negro':
            return aux(self, tablero, 1)


class Alfil(Pieza):
    def __init__(self, color: str, casilla: tuple[int, int], estilo: str, escala: float):
        super().__init__('alfil', color, casilla, estilo, escala)

    def posibles_movimientos(self, tablero):
        return self.movimiento_diagonal(tablero)


class Caballo(Pieza):
    def __init__(self, color: str, casilla: tuple[int, int], estilo: str, escala: float):
        super().__init__('caballo', color, casilla, estilo, escala)

    def posibles_movimientos(self, tablero):
        posibles_movimientos = []

        for i in (-1, 1):
            for j in (-2, 2):
                for casilla in ((self.fila + j, self.columna + i), (self.fila + i, self.columna + j)):
                    if self.movimiento_legal_base(tablero, casilla):
                        posibles_movimientos.append(casilla)

        return posibles_movimientos


class Torre(Pieza):
    def __init__(self, color: str, casilla: tuple[int, int], estilo: str, escala: float):
        super().__init__('torre', color, casilla, estilo, escala)

    def posibles_movimientos(self, tablero):
        return self.movimiento_recto(tablero)
