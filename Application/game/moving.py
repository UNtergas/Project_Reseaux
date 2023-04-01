import pygame

pygame.init()
window = pygame.display.set_mode((300, 300))
clock = pygame.time.Clock()
rect = pygame.Rect(0, 0, 20, 20)
rect.center = window.get_rect().center
vel = 5
bound = [window.get_width(), window.get_height()]
possible_x = True
run = True
while run:
    print(clock.get_fps())
    # print(f"screen{bound[0]},{bound[1]}\n")
    # print(f"{rect.centerx},{rect.centery}")

    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            pass
            # print(pygame.key.name(event.key))

    keys = pygame.key.get_pressed()

    if rect.centerx > bound[0]:
        rect.centerx = bound[0]
    elif rect.centerx < 0:
        rect.centerx = 0
    elif rect.centery > bound[1]:
        rect.centery = bound[1]
    elif rect.centery < 0:
        rect.centery = 0
    rect.x += (keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]) * vel
    rect.y += (keys[pygame.K_DOWN] - keys[pygame.K_UP]) * vel

    # rect.centerx = rect.centerx % window.get_width()
    # rect.centery = rect.centery % window.get_height()

    window.fill(0)
    pygame.draw.rect(window, (255, 0, 0), rect)
    pygame.display.flip()

pygame.quit()
exit()
