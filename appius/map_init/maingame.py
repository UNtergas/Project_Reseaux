import pygame as pg
from game.map import MapGame
SCREENSIZE = WIDTH, HEIGHT = 1200, 760


def main():

    running = True
    playing = True

    pg.init()
    pg.mixer.init()
    screen = pg.display.set_mode(SCREENSIZE)
    # screen = pg.display.set_mode((0, 0), pg.FULLSCREEN)
    clock = pg.time.Clock()

    # implement menu
    # implement game
    game = MapGame(screen, clock)
    while running:
        # menu

        while playing:
            # game loop
            game.run()


if __name__ == "__main__":
    main()
