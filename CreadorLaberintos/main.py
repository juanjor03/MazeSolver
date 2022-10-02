
# Se importa pygame, os y settings.py
from sprites import *
import csv
import sys

font_name = pg.font.match_font('arial')
def draw_text(surface, text, size, x, y, color):
    font = pg.font.Font(font_name, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.center = (x, y)
    surface.blit(text_surface, text_rect)


N_TILES = 5
csv_name = ''
maze = ""

class Button:
    def __init__(self, game, text, x, y, color, size, t_size):
        self.game = game
        self.image = pg.Surface(size)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        self.image.fill(color)
        self.text = text
        self.t_size = t_size
        self.color = color

    def show_text(self):
        draw_text(self.game.screen, self.text, self.t_size, self.rect.centerx, self.rect.centery, WHITE)

    def show(self):
        self.game.screen.fill(self.color, self.rect)

class Game:
    def __init__(self):
        # Inicializacion de pygame
        pg.init()
        pg.mixer.init()

        # Inicializacion de ventana
        self.screen = pg.display.set_mode(SCREEN_SIZE, pg.RESIZABLE)
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.running = True

    def load_data(self):
        self.map_data = list()
        with open(os.path.join(os.path.dirname(__file__), csv_name), 'rt') as f:
            reader = csv.reader(f)
            for row in reader:
                if row:
                    self.map_data.append(row)

    def new(self):
        self.all_sprites = pg.sprite.Group()
        self.walls = pg.sprite.Group()

        print(int((SCREEN_WIDTH/TILESIZE - N_TILES) / 2))

        for row, tiles in enumerate(self.map_data):
            print(tiles)
            for col, tile in enumerate(tiles):
                if tile == 'c' and row == 0:
                    self.player = Player(self, int((SCREEN_WIDTH/TILESIZE - N_TILES) / 2) + col, int((SCREEN_HEIGHT/TILESIZE - N_TILES) / 2), TILESIZE)
                    self.all_sprites.add(self.player)
                if tile == 'w':
                    wall = Wall(self, int((SCREEN_WIDTH/TILESIZE - N_TILES) / 2) + col, int((SCREEN_HEIGHT/TILESIZE - N_TILES) / 2) + row, TILESIZE)
                    self.all_sprites.add(wall)
                    self.walls.add(wall)

    def run(self):
        # Bucle del juego
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()

    def quit(self):
        # Saliendo del juego
        pg.quit()

    def update(self):
        # Actualizando todos los sprites
        self.all_sprites.update()

    def draw_grid(self):
        if N_TILES != 500:
            # Lineas verticales
            for i in range(int(TILESIZE*(SCREEN_WIDTH/TILESIZE - N_TILES) / 2),  int(SCREEN_WIDTH-TILESIZE*(SCREEN_WIDTH/TILESIZE - N_TILES) / 2 + 1), TILESIZE):
                pg.draw.line(self.screen, LIGHTGREY, (i, TILESIZE*(SCREEN_HEIGHT/TILESIZE - N_TILES) / 2), (i, SCREEN_HEIGHT-TILESIZE*(SCREEN_HEIGHT/TILESIZE - N_TILES) / 2))
            # Lineas horizontales
            for j in range(int(TILESIZE*(SCREEN_HEIGHT/TILESIZE - N_TILES) / 2), int(SCREEN_HEIGHT - TILESIZE*(SCREEN_HEIGHT/TILESIZE - N_TILES) / 2 + 1), TILESIZE):
                pg.draw.line(self.screen, LIGHTGREY, (TILESIZE*(SCREEN_WIDTH/TILESIZE - N_TILES) / 2, j), (SCREEN_WIDTH-TILESIZE*(SCREEN_WIDTH/TILESIZE - N_TILES) / 2, j))


    def draw(self):
        # Dando color a la pantalla y dibujando todos los sprites
        self.screen.fill(GREY)
        self.draw_grid()
        self.all_sprites.draw(self.screen)
        draw_text(self.screen, maze, 50, SCREEN_WIDTH / 2, 80, WHITE)
        # Actualizamos los cambios
        pg.display.flip()

    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False

            if event.type == pg.KEYDOWN:
                if event.key == pg.K_LEFT:
                    self.player.move(dx=-1,dy=0)
                if event.key == pg.K_RIGHT:
                    self.player.move(dx=1,dy=0)
                if event.key == pg.K_UP:
                    self.player.move(dx=0,dy=-1)
                if event.key == pg.K_DOWN:
                    self.player.move(dx=0,dy=1)

    def draw_buttons(self):
        for button in self.buttons:
            button.show()
            button.show_text()

    def show_start_screen(self):
        self.showing_menu = True
        self.buttons = []
        button1 = Button(self, "Maze 5x5", SCREEN_WIDTH / 2, SCREEN_HEIGHT*0.4, BLUE, (400, 60), 25)
        self.buttons.append(button1)
        button2 = Button(self, "Maze 10x10", SCREEN_WIDTH / 2, SCREEN_HEIGHT*0.5, BLUE, (400, 60), 25)
        self.buttons.append(button2)
        button3 = Button(self, "Maze 50x50", SCREEN_WIDTH / 2, SCREEN_HEIGHT*0.6, BLUE, (400, 60), 25)
        self.buttons.append(button3)
        button4 = Button(self, "Maze 100x100", SCREEN_WIDTH / 2, SCREEN_HEIGHT * 0.7, BLUE, (400, 60), 25)
        self.buttons.append(button4)
        button5 = Button(self, "Maze 400x400", SCREEN_WIDTH / 2, SCREEN_HEIGHT * 0.8, BLUE, (400, 60), 25)
        self.buttons.append(button5)
        while self.showing_menu:
            self.clock.tick(FPS)
            self.screen.fill(BLACK)

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
                if event.type == pg.MOUSEBUTTONDOWN:
                    mpos = pg.mouse.get_pos()
                    if button1.rect.collidepoint(mpos):
                        global TILESIZE
                        TILESIZE = 100
                        global csv_name
                        csv_name = 'maze_5x5.csv'
                        global maze
                        maze = csv_name[:-4].replace("_", " ").replace("m", "M")
                        self.showing_menu = False

                    elif button2.rect.collidepoint(mpos):
                        TILESIZE = 50
                        global N_TILES
                        N_TILES = 10
                        csv_name = 'maze_10x10.csv'
                        maze = csv_name[:-4].replace("_", " ").replace("m", "M")
                        self.showing_menu = False

                    elif button3.rect.collidepoint(mpos):
                        TILESIZE = 10
                        N_TILES = 50
                        csv_name = 'maze_50x50.csv'
                        maze = csv_name[:-4].replace("_", " ").replace("m", "M")
                        self.showing_menu = False

                    elif button4.rect.collidepoint(mpos):
                        TILESIZE = 5
                        N_TILES = 100
                        csv_name = 'maze_100x100.csv'
                        maze = csv_name[:-4].replace("_", " ").replace("m", "M")
                        self.showing_menu = False

                    elif button5.rect.collidepoint(mpos):
                        TILESIZE = 2
                        N_TILES = 400
                        csv_name = 'maze_400x400.csv'
                        maze = ""
                        self.showing_menu = False

            self.draw_buttons()
            draw_text(self.screen, "Maze Solver", 80, SCREEN_WIDTH / 2, 80, GREEN)

            pg.display.flip()

    def show_go_screen(self):
        pass


g = Game()
g.show_start_screen()
g.load_data()
while g.running:
    g.new()
    g.run()
    g.show_go_screen()

