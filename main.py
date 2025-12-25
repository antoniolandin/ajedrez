import pygame
from tablero import Tablero
from piezas import Pieza
from temporizador import Temporizador
import copy

BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
LARGO, ALTO = 1280, 960
COLORS = ''
ESCALA = 3

pygame.init()
pygame.display.set_caption("Ajedrez")

pantalla = pygame.display.set_mode((LARGO, ALTO))

fondo = pygame.transform.scale(pygame.image.load(f"assets/chess{COLORS}/bg.png"), (LARGO, ALTO)).convert()
tam_x, tam_y = pygame.image.load(f"assets/chess{COLORS}/board.png").get_size()
x = LARGO // 2 - tam_x * ESCALA // 2
y = ALTO // 2 - tam_y * ESCALA // 2
tablero = Tablero(x, y, escala=ESCALA)
casilla_seleccionada = None
sonido_mover_pieza = pygame.mixer.Sound('assets/audio/move.ogg')
sonido_jacke = pygame.mixer.Sound('assets/audio/jacke.ogg')
jugadores = ('blanco', 'negro')
num_movimientos = 0
color_turno = jugadores[num_movimientos % 2]
fuente_victoria = pygame.Font(None, LARGO // 10)
ganador = None

evento_tiempo = pygame.USEREVENT + 1
pygame.time.set_timer(evento_tiempo, 1000)
temporizadores = [10 * 60, 10 * 60]
fuente_temporizador = pygame.Font(None, LARGO // 20)
temporizadores = [
    Temporizador(10 * 60, tablero.x, tablero.y + tablero.tam_y, fuente_temporizador, BLANCO),
    Temporizador(10 * 60, tablero.x, tablero.y, fuente_temporizador, BLANCO)
]
temporizadores[1].y = tablero.y - temporizadores[1].tam_y


def detectar_jacke(color: str, piezas: dict, num_filas: int, num_columnas: int):
    rey = encontrar_rey(color, piezas)
    if not rey:
        return False

    for pieza in piezas.values():
        if pieza != rey and (rey.fila, rey.columna) in pieza.posibles_movimientos(piezas, num_filas, num_columnas):
            return True

    return False


def encontrar_rey(color: str, piezas: dict):
    for pieza in piezas.values():
        if pieza.tipo == 'rey' and pieza.color == color:
            return pieza

    return None


def detectar_jacke_mate(color: str, piezas: dict[tuple[int, int], Pieza], num_filas: int, num_columnas: int):
    for pos_pieza in piezas.keys():
        pieza = piezas[pos_pieza]
        if pieza.color == color:
            posibles_movimientos = pieza.posibles_movimientos(piezas, num_filas, num_columnas)

            # ver si se va el jacke al mover
            for movimiento in posibles_movimientos:
                temp_piezas = copy.deepcopy(piezas)
                temp_pieza = temp_piezas[pos_pieza]
                temp_pieza.fila, temp_pieza.columna = movimiento[0], movimiento[1]
                del temp_piezas[pos_pieza]
                temp_piezas[movimiento] = temp_pieza

                if not detectar_jacke(color, temp_piezas, num_filas, num_columnas):
                    return False

    return True


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
                if not ganador:
                    raton_columna = (raton_x - tablero.borde - tablero.x) // tablero.tam_casilla
                    raton_fila = (raton_y - tablero.borde - tablero.y) // tablero.tam_casilla

                    color_turno = jugadores[num_movimientos % 2]

                    if 0 <= raton_fila <= tablero.num_filas - 1 and 0 <= raton_columna <= tablero.num_columnas - 1:
                        if (
                            not casilla_seleccionada
                            and (raton_fila, raton_columna) in tablero.piezas
                            and tablero.piezas[(raton_fila, raton_columna)].color == color_turno
                        ):
                            casilla_seleccionada = (raton_fila, raton_columna)
                            tablero.piezas[casilla_seleccionada].seleccionada = True
        elif evento.type == pygame.MOUSEBUTTONUP:
            if evento.button == pygame.BUTTON_LEFT:
                if not ganador:
                    if casilla_seleccionada:
                        pieza_seleccionada = tablero.piezas[casilla_seleccionada]
                        pieza_seleccionada.seleccionada = False

                        raton_columna = (raton_x - tablero.borde - tablero.x) // tablero.tam_casilla
                        raton_fila = (raton_y - tablero.borde - tablero.y) // tablero.tam_casilla

                        movimiento = (raton_fila, raton_columna)
                        color_turno = jugadores[num_movimientos % 2]

                        if (
                            pieza_seleccionada.color == color_turno
                            and pieza_seleccionada.movimiento_legal(tablero.piezas, tablero.num_filas, tablero.num_columnas, movimiento)
                        ):
                            temp_piezas = copy.deepcopy(tablero.piezas)
                            pieza_temp = temp_piezas[casilla_seleccionada]
                            pieza_temp.fila, pieza_temp.columna = raton_fila, raton_columna
                            del temp_piezas[casilla_seleccionada]
                            temp_piezas[movimiento] = pieza_temp

                            # si hay jacke, invalidar movimiento
                            if not detectar_jacke(color_turno, temp_piezas, tablero.num_filas, tablero.num_columnas):
                                tablero.mover_pieza(casilla_seleccionada, movimiento)
                                sonido_mover_pieza.play()
                                num_movimientos += 1

                                # si le haces jacke al otro rey, reproducir sonido
                                color_turno = jugadores[num_movimientos % 2]
                                if detectar_jacke(color_turno, tablero.piezas, tablero.num_filas, tablero.num_columnas):
                                    # comprobar si es jacke mate
                                    if detectar_jacke_mate(color_turno, tablero.piezas, tablero.num_filas, tablero.num_columnas):
                                        ganador = jugadores[(num_movimientos + 1) % 2]
                                    else:
                                        sonido_jacke.play()
                        casilla_seleccionada = None

        elif evento.type == evento_tiempo:
            pygame.time.set_timer(evento_tiempo, 1000)
            temporizadores[num_movimientos % 2].tiempo_restante -= 1
            temporizadores[num_movimientos % 2].actualizar()

    pantalla.fill(BLANCO)
    pantalla.blit(fondo, (0, 0))
    tablero.dibujar(pantalla)

    if ganador:
        texto_superficie = fuente_victoria.render(f"Gana el jugador {ganador}", True, NEGRO)
        tam_x, tam_y = texto_superficie.get_size()
        x = LARGO // 2 - tam_x // 2
        y = ALTO // 2 - tam_y // 2
        pygame.draw.rect(pantalla, BLANCO, (x, y, tam_x, tam_y))
        pantalla.blit(texto_superficie, (x, y))

    for temporizador in temporizadores:
        temporizador.dibujar(pantalla)

    pygame.display.flip()
