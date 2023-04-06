# pygame setup
import pygame
import pygame as pg

pg.init()
screen = pg.display.set_mode([600, 400])
pg.display.set_caption("Example code for the cursors module")

surface1 = pygame.Surface((100, 100))
surface1.fill((0, 0, 255))

# Create a surface with a green background, and set its transparency to 50%
surface2 = pygame.Surface((100, 100))
surface2.fill((0, 255, 0))
surface2.set_alpha(128)

# Draw the surfaces to the screen
screen.blit(surface1, (0, 0))
screen.blit(surface2, (0, 0))
system = pg.cursors.Cursor(pg.SYSTEM_CURSOR_NO)

# create bitmap cursors
bitmap_1 = pg.cursors.Cursor(*pg.cursors.arrow)
bitmap_2 = pg.cursors.Cursor(
    (24, 24), (0, 0), *pg.cursors.compile(pg.cursors.thickarrow_strings)
)
image = pg.cursors.Cursor((20, 20), pg.image.load(
    "cursor/hammer.png").convert_alpha())
normal = pg.cursors.Cursor(pg.SYSTEM_CURSOR_ARROW)
# create a color cursor
surf = pg.Surface((40, 40))  # you could also load an image
surf.fill((120, 50, 50))        # and use that as your surface
color = pg.cursors.Cursor((20, 20), surf)

cursors = [system, bitmap_1, bitmap_2, color, image, normal]
cursor_index = 0

pg.mouse.set_cursor(cursors[cursor_index])

clock = pg.time.Clock()
going = True
while going:
    clock.tick(60)
    pg.display.flip()

    for event in pg.event.get():
        if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
            going = False

        # if the mouse is clicked it will switch to a new cursor
        if event.type == pg.MOUSEBUTTONDOWN:
            cursor_index += 1
            cursor_index %= len(cursors)
            pg.mouse.set_cursor(cursors[cursor_index])

pg.quit()
