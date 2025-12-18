import pygame
from tablero import Tablero

pygame.init()
pygame.display.set_caption("Ajedrez")

BLANCO = (255, 255, 255)
LARGO, ALTO = 640, 480
TAM_CASILLA = 22
COLORS = ''

pantalla = pygame.display.set_mode((LARGO, ALTO))

fondo = pygame.transform.scale(pygame.image.load(f"assets/chess{COLORS}/bg.png"), (LARGO, ALTO)).convert()
tam_x, tam_y = pygame.image.load(f"assets/chess{COLORS}/board.png").get_size()
escala = 2
x = LARGO // 2 - (tam_x // 2) * escala
y = ALTO // 2 - (tam_y // 2) * escala
tablero = Tablero(x, y, escala=2)
casilla_seleccionada = None

while True:
    raton_x, raton_y = pygame.mouse.get_pos()

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            exit()
        elif evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_q:
                pygame.quit()
                exit()
        elif evento.type == pygame.MOUSEBUTTONDOWN:
            if evento.button == pygame.BUTTON_LEFT:
                raton_columna = (raton_x - tablero.borde * tablero.escala - tablero.x) // (tablero.tam_casilla * tablero.escala)
                raton_fila = (raton_y - tablero.borde * tablero.escala - tablero.y) // (tablero.tam_casilla * tablero.escala)

                if 0 <= raton_fila <= 7 and 0 <= raton_columna <= 7:
                    if not casilla_seleccionada and (raton_fila, raton_columna) in tablero.piezas:
                        casilla_seleccionada = (raton_fila, raton_columna)
                        tablero.piezas[casilla_seleccionada].selecionada = True
        elif evento.type == pygame.MOUSEBUTTONUP:
            if evento.button == pygame.BUTTON_LEFT:
                if casilla_seleccionada:
                    tablero.piezas[casilla_seleccionada].selecionada = False

                    raton_columna = (raton_x - tablero.borde * tablero.escala - tablero.x) // (tablero.tam_casilla * tablero.escala)
                    raton_fila = (raton_y - tablero.borde * tablero.escala - tablero.y) // (tablero.tam_casilla * tablero.escala)

                    tablero.mover_pieza(casilla_seleccionada, (raton_fila, raton_columna))
                    casilla_seleccionada = None

    pantalla.fill(BLANCO)
    pantalla.blit(fondo, (0, 0))
    tablero.dibujar(pantalla)
    pygame.display.flip()
