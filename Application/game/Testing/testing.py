# import pygame as pg
# import sys
# SCREEN = WIDTH, HEIGH = 300, 300

# pg.init()
# run = True
# display = pg.display.set_mode(SCREEN)


# def eventhandling():
#     for event in pg.event.get():
#         if event.type == pg.QUIT:
#             pg.quit()
#             sys.exit()


# while run:
#     eventhandling()
lista = []
for x in range(5):
    lista.append([])
    for y in range(5):
        lista[x].append(y)
lista[2].remove(2)
lista[2].insert(2, 9)
print(lista)
