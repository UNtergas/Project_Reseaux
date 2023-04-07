import pygame
from const import *
from Save import *


class InputBox:
    def __init__(self,  x, y, width, height, action, font=font2, text=''):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.rect = pygame.Rect(
            ((self.x-self.width/2), (self.y-self.height/2), self.width, self.height))
        self.text = text
        self.color = pygame.Color(109, 109, 109)
        self.font = font
        self.txt_render = self.font.render(text, True, self.color)
        self.active = False
        self.action = action
        self.count = 0

    def OverBox(self, event):
        if self.rect.collidepoint(event.pos):
            self.active = not self.active
        else:
            self.active = False

        if self.active:
            self.color = (145, 145, 145)
        else:
            self.color = pygame.Color(109, 109, 109)

    def write(self, event):
        if self.active:
            if event.key == pygame.K_RETURN:
                self.action()
            elif event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
                print(self.count)
                self.count -= 1
            else:
                if self.count < 15:
                    self.text += event.unicode
                    self.count += 1
                    print(self.count)
            self.txt_render = self.font.render(self.text, True, (0, 0, 0))

    def show(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
        screen.blit(self.txt_render, (self.rect.x, self.rect.y))
