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
        self.posibles_movimientos = []

    def actualizar_posicion(self, tablero_x: int, tablero_y: int, borde_tablero: int, tam_casilla: tuple[int, int]):
        x = borde_tablero * self.escala + tablero_x - self.tam_x // 2 + \
            (tam_casilla * self.escala) // 2 + self.columna * tam_casilla * self.escala
        y = borde_tablero * self.escala + tablero_y - self.tam_y // 2 + \
            (tam_casilla * self.escala) // 2 + self.fila * tam_casilla * self.escala
        self.posicion = (x, y)

    def dibujar(self, pantalla):
        pantalla.blit(self.sprite, self.posicion)

    def movimiento_legal(self, casilla: tuple[int, int], piezas: dict) -> bool:
        fila_final, columna_final = casilla
        return not (casilla in piezas and piezas[casilla].color == self.color) and (0 <= fila_final <= 7 and 0 <= columna_final <= 7)

    def __str__(self):
        return f"{self.tipo} {self.color}"


class Rey(Pieza):
    def __init__(self, color: str, casilla: tuple[int, int], estilo: str, escala: float):
        super().__init__('rey', color, casilla, estilo, escala)

    def movimiento_legal(self, casilla: tuple[int, int], piezas: dict) -> bool:
        nueva_fila, nueva_columna = casilla
        return abs(self.fila - nueva_fila) <= 1 and abs(self.columna - nueva_columna) <= 1 and super().movimiento_legal(casilla, piezas)

    def actualizar_posibles_movimientos(self, piezas: dict):
        posibles_movimientos = []
        for offset_fila in range(-1, 2):
            for offset_columna in range(-1, 2):
                if not (offset_fila == 0 and offset_columna == 0):
                    nueva_casilla = (self.fila + offset_fila, self.columna + offset_columna)
                    if super().movimiento_legal(nueva_casilla, piezas):
                        posibles_movimientos.append(nueva_casilla)


class Reina(Pieza):
    def __init__(self, color: str, casilla: tuple[int, int], estilo: str, escala: float):
        super().__init__('reina', color, casilla, estilo, escala)


class Peon(Pieza):
    def __init__(self, color: str, casilla: tuple[int, int], estilo: str, escala: float):
        super().__init__('peon', color, casilla, estilo, escala)

    def movimiento_legal(self, casilla: tuple[int, int], piezas: dict) -> bool:
        nueva_fila, nueva_columna = casilla

        return (
            nueva_columna == self.columna
            and (
                (self.color == 'blanco' and ((self.fila == 6 and self.fila - nueva_fila == 2) or self.fila - nueva_fila == 1))
                or (self.color == 'negro' and ((self.fila == 1 and nueva_fila - self.fila == 2) or nueva_fila - self.fila == 1))
            )
            and casilla not in piezas
        ) or (
            abs(nueva_columna - self.columna) == 1
            and (
                ((self.color == 'blanco' and (self.fila - nueva_fila == 1)))
                or (self.color == 'negro' and (nueva_fila - self.fila == 1))
            )
            and casilla in piezas
        ) and super().movimiento_legal(casilla, piezas)


class Alfil(Pieza):
    def __init__(self, color: str, casilla: tuple[int, int], estilo: str, escala: float):
        super().__init__('alfil', color, casilla, estilo, escala)


class Caballo(Pieza):
    def __init__(self, color: str, casilla: tuple[int, int], estilo: str, escala: float):
        super().__init__('caballo', color, casilla, estilo, escala)


class Torre(Pieza):
    def __init__(self, color: str, casilla: tuple[int, int], estilo: str, escala: float):
        super().__init__('torre', color, casilla, estilo, escala)

    def movimiento_legal(self, casilla: tuple[int, int], piezas: dict, escala: float) -> bool:
        if not super().movimiento_legal(casilla, piezas, escala):
            return False

        nueva_fila, nueva_columna = casilla
        if self.columna == nueva_columna:
            if nueva_fila > self.fila:
                for fila in range(self.fila + 1, nueva_fila):
                    if (fila, self.columna) in piezas:
                        return False
            else:
                for fila in range(nueva_fila + 1, self.fila):
                    if (fila, self.columna) in piezas:
                        return False
            return True

        elif self.fila == nueva_fila:
            if nueva_columna > self.columna:
                for columna in range(self.columna + 1, nueva_columna):
                    if (self.fila, columna) in piezas:
                        return False
            else:
                for columna in range(nueva_columna + 1, self.columna):
                    if (self.fila, columna) in piezas:
                        return False

            return True

        return False
