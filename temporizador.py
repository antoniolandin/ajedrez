import pygame


class Temporizador():
    def __init__(self, tiempo_inicial: int, x: int, y: int, fuente: pygame.Font, color: tuple[int, int, int]):
        self.tiempo_restante = tiempo_inicial
        self.x = x
        self.y = y
        self.fuente = fuente
        self.mensaje = ""
        self.sprite = None
        self.color = color
        self.actualizar()

    def actualizar(self):
        tiempo = self.tiempo_restante
        horas = tiempo // 3600
        tiempo %= 3600
        minutos = tiempo // 60
        tiempo %= 60
        segundos = tiempo

        self.mensaje = f"{horas}h {minutos}m {segundos}s"
        self.sprite = self.fuente.render(self.mensaje, True, self.color)
        self.tam_x, self.tam_y = self.sprite.get_size()

    def dibujar(self, pantalla: pygame.Surface):
        pantalla.blit(self.sprite, (self.x, self.y))
