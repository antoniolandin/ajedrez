import pygame
from piezas import Rey, Reina, Caballo, Torre, Alfil, Peon, Pieza


class Tablero:
    def __init__(self, x: int, y: int, escala: float, estilo="", tam_casilla=22, borde=2):
        self.piezas = {}
        self.sprite = pygame.transform.scale_by(pygame.image.load(f"assets/chess{estilo}/board.png"), escala).convert()
        self.x, self.y = x, y
        self.estilo = estilo
        self.tam_casilla = tam_casilla
        self.escala = escala
        self.borde = borde
        self.reiniciar_tablero()

    def añadir_pieza(self, tipo_pieza: str, color: str, posicion: tuple[int, int]):
        assert tipo_pieza in Pieza.traducir_pieza.keys()

        if tipo_pieza == 'rey':
            self.piezas[posicion] = Rey(color, posicion, self.estilo, self.escala)
        elif tipo_pieza == 'reina':
            self.piezas[posicion] = Reina(color, posicion, self.estilo, self.escala)
        elif tipo_pieza == 'alfil':
            self.piezas[posicion] = Alfil(color, posicion, self.estilo, self.escala)
        elif tipo_pieza == 'caballo':
            self.piezas[posicion] = Caballo(color, posicion, self.estilo, self.escala)
        elif tipo_pieza == 'torre':
            self.piezas[posicion] = Torre(color, posicion, self.estilo, self.escala)
        elif tipo_pieza == 'peon':
            self.piezas[posicion] = Peon(color, posicion, self.estilo, self.escala)

        self.piezas[posicion].actualizar_posicion(self.x, self.y, self.borde, self.tam_casilla)

    def reiniciar_tablero(self):
        self.piezas = {}

        for i in range(8):
            self.añadir_pieza('peon', 'negro', (1, i))
            self.añadir_pieza('peon', 'blanco', (6, i))

        for index, pieza in enumerate(['torre', 'caballo', 'alfil']):
            for i in range(2):
                self.añadir_pieza(pieza, 'negro', (0, index + i * (7 - index * 2)))
                self.añadir_pieza(pieza, 'blanco', (7, index + i * (7 - index * 2)))

        self.añadir_pieza('reina', 'negro', (0, 3))
        self.añadir_pieza('rey', 'negro', (0, 4))
        self.añadir_pieza('reina', 'blanco', (7, 3))
        self.añadir_pieza('rey', 'blanco', (7, 4))

    def mover_pieza(self, casilla_inicial: tuple[int, int], casilla_final: tuple[int, int]):
        fila_final, columna_final = casilla_final
        pieza: Pieza = self.piezas[casilla_inicial]
        if pieza.movimiento_legal(casilla_final, self.piezas):
            pieza.fila, pieza.columna = casilla_final
            pieza.actualizar_posicion(self.x, self.y, self.borde, self.tam_casilla)

            del self.piezas[casilla_inicial]
            self.piezas[casilla_final] = pieza

    def dibujar(self, pantalla):
        pantalla.blit(self.sprite, (self.x, self.y))
        for pieza in self.piezas.values():
            if not pieza.selecionada:
                pieza.dibujar(pantalla)
            else:
                raton_x, raton_y = pygame.mouse.get_pos()
                pantalla.blit(pieza.sprite, (raton_x - pieza.tam_x // 2, raton_y - pieza.tam_y // 2))
