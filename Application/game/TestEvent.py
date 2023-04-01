import pygame as pg
import sys

pg.init()
screen = pg.display.set_mode((300, 300))
screen.fill((255, 255, 255))


class TE:
    def __init__(self, action=None, *args):
        self.num = 10
        self.args = []
        self.action = action
        for _ in args:
            self.args.append(_)

    def setAction(self, action, *args):
        self.action = action
        self.args = []
        for _ in args:
            self.args.append(_)

    def do(self):
        self.action(*self.args)


def plus(_num):
    _num += 1


def test(event, a=1):
    if event[pg.K_UP]:
        print(event[pg.K_UP])
        a += 1
        print(a)


while 1:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()
    test(pg.key.get_pressed())
