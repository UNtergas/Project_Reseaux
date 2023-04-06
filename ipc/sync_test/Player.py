import pygame


class Player:
    def __init__(self, screen_width, screen_height, color) -> None:
        self.rect_width = 50
        self.rect_height = 50
        self.rect_color = color
        self.rect_position = [screen_width/2, screen_height/2]
        self.image = pygame.image.load('phuoc.jpg')
        self.image = pygame.transform.scale(
            self.image, (50, 50))

    def draw(self, screen):

        rect = pygame.Rect(
            self.rect_position[0], self.rect_position[1], self.rect_width, self.rect_height)
        pygame.draw.rect(screen, self.rect_color, rect)

    def phuoc_ve(self, screen):
        # print(self.rect_position[0], self.rect_position[1])
        screen.blit(self.image, (self.rect_position[0], self.rect_position[1]))

    def movement(self, dir):
        if dir == 'left':
            self.rect_position[0] -= 15
        elif dir == 'right':
            self.rect_position[0] += 15
        elif dir == 'up':
            self.rect_position[1] -= 15
        elif dir == 'down':
            self.rect_position[1] += 15
