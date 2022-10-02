
import pygame as pg

# Inicializacion
pg.init()
pg.mixer.init()

# Dimensiones pantalla
SCREEN_SIZE = (700, 500)

# Colores
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# Otras constantes
FPS = 60

# Inicializacion de ventana
screen = pg.display.set_mode(SCREEN_SIZE)
pg.display.set_caption("Game 1")
clock = pg.time.Clock()

running = True
while running:
    # Correr el juego a la velocidad esperada
    clock.tick(FPS)

    # Revision de eventos
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

    # Lógica y actualizacion
    pass

    # Dibujar
    screen.fill(BLACK)

    # Actualiza la pantalla completa
    pg.display.flip()

pg.quit()

