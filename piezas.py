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
        self.seleccionada = False
        self.color = color
        self.fila, self.columna = casilla
        self.movida = False

    def actualizar_posicion(self, tablero):
        x = tablero.borde + tablero.x - self.tam_x // 2 + \
            tablero.tam_casilla // 2 + self.columna * tablero.tam_casilla
        y = tablero.borde + tablero.y - self.tam_y // 2 + \
            tablero.tam_casilla // 2 + self.fila * tablero.tam_casilla
        self.posicion = (x, y)

    def mover(self, tablero, movimiento: tuple[int, int]):
        self.fila, self.columna = movimiento
        self.actualizar_posicion(tablero)

        if not self.movida:
            self.movida = True

    def dibujar(self, pantalla):
        pantalla.blit(self.sprite, self.posicion)

    def posibles_movimientos(self, piezas, num_filas: int, num_columnas: int):
        posibles_movimientos = []
        for fila in range(num_filas):
            for columna in range(num_columnas):
                casilla = (fila, columna)
                if not self.movimiento_legal_base(piezas, num_filas, num_columnas, casilla):
                    posibles_movimientos.append(casilla)

        return posibles_movimientos

    def movimiento_legal(self, piezas, num_filas: int, num_columnas: int, movimiento: tuple[int, int]):
        return movimiento in self.posibles_movimientos(piezas, num_filas, num_columnas)

    def movimiento_legal_base(self, piezas, num_filas: int, num_columnas: int, casilla: tuple[int, int]):
        return (
            (self.fila != casilla[0] or self.columna != casilla[1])
            and (0 <= casilla[0] < num_filas and 0 <= casilla[1] < num_columnas)
            and not (casilla in piezas and piezas[casilla].color == self.color)
        )

    def movimiento_diagonal(self, piezas, num_filas, num_columnas):
        posibles_movimientos = []

        for combinacion in itertools.product((1, -1), repeat=2):
            offset_fila, offset_columna = combinacion
            fila, columna = self.fila + offset_fila, self.columna + offset_columna
            while (0 <= fila < num_filas and 0 <= columna < num_columnas):
                casilla = (fila, columna)

                if self.movimiento_legal_base(piezas, num_filas, num_columnas, casilla):
                    posibles_movimientos.append(casilla)

                if (casilla in piezas):
                    break

                fila = fila + offset_fila
                columna = columna + offset_columna

        return posibles_movimientos

    def movimiento_recto(self, piezas, num_filas, num_columnas):
        posibles_movimientos = []

        for indice, rangos in enumerate((
                (range(self.fila + 1, num_filas), range(self.fila - 1, -1, -1)),
                (range(self.columna + 1, num_columnas), range(self.columna - 1, -1, -1))
        )):
            for rango in rangos:
                for i in rango:
                    if indice == 0:
                        casilla = (i, self.columna)
                    elif indice == 1:
                        casilla = (self.fila, i)

                    if self.movimiento_legal_base(piezas, num_filas, num_columnas, casilla):
                        posibles_movimientos.append(casilla)

                    if (casilla in piezas):
                        break

        return posibles_movimientos

    def __str__(self):
        return f"{self.tipo} {self.color}".title()


class Rey(Pieza):
    def __init__(self, color: str, casilla: tuple[int, int], estilo: str, escala: float):
        super().__init__('rey', color, casilla, estilo, escala)

    def posibles_movimientos(self, piezas, num_filas, num_columnas):
        posibles_movimientos = []
        for fila in range(self.fila - 1, self.fila + 2):
            for columna in range(self.columna - 1, self.columna + 2):
                casilla = (fila, columna)
                if self.movimiento_legal_base(piezas, num_filas, num_columnas, casilla):
                    posibles_movimientos.append(casilla)

        if not self.movida:
            if (self.fila, num_columnas - 1) in piezas:
                pieza = piezas[(self.fila, num_columnas - 1)]
                if pieza.tipo == 'torre' and not pieza.movida:
                    vacia = True
                    for columna in range(self.columna + 1, pieza.columna):
                        if (self.fila, columna) in piezas:
                            vacia = False
                    if vacia:
                        posibles_movimientos.append((self.fila, pieza.columna - 1))
            if (self.fila, 0) in piezas:
                pieza = piezas[(self.fila, 0)]
                if pieza.tipo == 'torre' and not pieza.movida:
                    vacia = True
                    for columna in range(1, self.columna):
                        if (self.fila, columna) in piezas:
                            vacia = False
                    if vacia:
                        posibles_movimientos.append((self.fila, 2))

        return posibles_movimientos


class Reina(Pieza):
    def __init__(self, color: str, casilla: tuple[int, int], estilo: str, escala: float):
        super().__init__('reina', color, casilla, estilo, escala)

    def posibles_movimientos(self, piezas, num_filas, num_columnas):
        return self.movimiento_diagonal(piezas, num_filas, num_columnas) + self.movimiento_recto(piezas, num_filas, num_columnas)


class Peon(Pieza):
    def __init__(self, color: str, casilla: tuple[int, int], estilo: str, escala):
        super().__init__('peon', color, casilla, estilo, escala)

    def posibles_movimientos(self, piezas, num_filas, num_columnas):
        def aux(self, piezas, num_filas, num_columnas, i):
            posibles_movimientos = []

            # movimiento diagonal
            for columna in (self.columna - 1, self.columna + 1):
                casilla = (self.fila + i, columna)
                if self.movimiento_legal_base(piezas, num_filas, num_columnas, casilla) and casilla in piezas:
                    posibles_movimientos.append(casilla)

            # movimiento recto
            casilla = (self.fila + i, self.columna)
            if casilla not in piezas and self.movimiento_legal_base(piezas, num_filas, num_columnas, casilla):
                posibles_movimientos.append(casilla)

            # doble salto
            if not self.movida:
                casilla_1 = (self.fila + i, self.columna)
                casilla_2 = (self.fila + i * 2, self.columna)
                if (
                    self.movimiento_legal_base(piezas, num_filas, num_columnas, casilla)
                    and casilla_1 not in piezas
                    and casilla_2 not in piezas
                ):
                    posibles_movimientos.append(casilla_2)

            return posibles_movimientos

        if self.color == 'blanco':
            return aux(self, piezas, num_filas, num_columnas, -1)
        elif self.color == 'negro':
            return aux(self, piezas, num_filas, num_columnas, 1)


class Alfil(Pieza):
    def __init__(self, color: str, casilla: tuple[int, int], estilo: str, escala: float):
        super().__init__('alfil', color, casilla, estilo, escala)

    def posibles_movimientos(self, piezas, num_filas, num_columnas):
        return self.movimiento_diagonal(piezas, num_filas, num_columnas)


class Caballo(Pieza):
    def __init__(self, color: str, casilla: tuple[int, int], estilo: str, escala: float):
        super().__init__('caballo', color, casilla, estilo, escala)

    def posibles_movimientos(self, piezas, num_filas, num_columnas):
        posibles_movimientos = []

        for i in (-1, 1):
            for j in (-2, 2):
                for casilla in ((self.fila + j, self.columna + i), (self.fila + i, self.columna + j)):
                    if self.movimiento_legal_base(piezas, num_filas, num_columnas, casilla):
                        posibles_movimientos.append(casilla)

        return posibles_movimientos


class Torre(Pieza):
    def __init__(self, color: str, casilla: tuple[int, int], estilo: str, escala: float):
        super().__init__('torre', color, casilla, estilo, escala)

    def posibles_movimientos(self, piezas, num_filas, num_columnas):
        return self.movimiento_recto(piezas, num_filas, num_columnas)
