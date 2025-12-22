import pygame
from piezas import Pieza, Rey, Reina, Alfil, Caballo, Torre, Peon


class Tablero:
    def __init__(self, x: int, y: int, escala: float, estilo="", borde=2, num_filas=8, num_columnas=8):
        self.piezas = {}
        self.sprite = pygame.transform.scale_by(pygame.image.load(f"assets/chess{estilo}/board.png"), escala).convert()
        self.tam_casilla = (self.sprite.get_size()[0] - borde * 2) // (num_filas * escala)
        self.x, self.y = x, y
        self.estilo = estilo
        self.escala = escala
        self.borde = borde
        self.num_filas = num_filas
        self.num_columnas = num_columnas

        self.reiniciar_tablero()

    def añadir_pieza(self, tipo_pieza: str, color: str, posicion: tuple[int, int]):
        assert tipo_pieza in Pieza.traducir_pieza.keys()
        assert 0 <= posicion[0] < self.num_filas and 0 <= posicion[1] < self.num_columnas

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

        self.piezas[posicion].actualizar_posicion(self)

    def reiniciar_tablero(self):
        self.piezas = {}

        for i in range(self.num_columnas):
            self.añadir_pieza('peon', 'negro', (1, i))
            self.añadir_pieza('peon', 'blanco', (self.num_filas - 2, i))

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
        if pieza.movimiento_legal(self, casilla_final):
            pieza.mover(self, casilla_final)

            del self.piezas[casilla_inicial]
            self.piezas[casilla_final] = pieza

    def dibujar_circulos_pieza(self, pieza: Pieza, pantalla: pygame.Surface):
        for casilla in pieza.posibles_movimientos(self):
            fila, columna = casilla
            cx = self.borde * self.escala + self.x + columna * self.tam_casilla * self.escala + self.tam_casilla * self.escala // 2
            cy = self.borde * self.escala + self.y + fila * self.tam_casilla * self.escala + self.tam_casilla * self.escala // 2

            color = (150, 150, 150, 150)

            if casilla in self.piezas:
                radio = self.tam_casilla * self.escala // 2
                diametro = radio * 2
                superficie_circulo = pygame.Surface((diametro, diametro), pygame.SRCALPHA)
                borde_donut = int(self.tam_casilla * 0.2)
                pygame.draw.aacircle(superficie_circulo, color, (radio, radio), radio, borde_donut)
            else:
                radio = self.tam_casilla * self.escala // 4
                diametro = radio * 2
                superficie_circulo = pygame.Surface((diametro, diametro), pygame.SRCALPHA)
                pygame.draw.aacircle(superficie_circulo, color, (radio, radio), radio)
            pantalla.blit(superficie_circulo, (cx - radio, cy - radio))

    def dibujar(self, pantalla: pygame.Surface):
        pantalla.blit(self.sprite, (self.x, self.y))
        pieza_seleccionada: Pieza = None
        for pieza in self.piezas.values():
            if not pieza.selecionada:
                pieza.dibujar(pantalla)
            else:
                pieza_seleccionada = pieza

        if pieza_seleccionada:
            self.dibujar_circulos_pieza(pieza_seleccionada, pantalla)

            raton_x, raton_y = pygame.mouse.get_pos()
            pantalla.blit(pieza_seleccionada.sprite, (raton_x - pieza.tam_x // 2, raton_y - pieza.tam_y // 2))
