import pygame
from const import font1


class Button:

    def __init__(self,  x, y, width, height, action):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.action = action
        self.color = (109, 109, 109)
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.rect.topleft = (self.x, self.y)
        self.hover = False

    def MouseonButton(self, posMouse):
        if (posMouse[0] > (self.x - self.width/2) and posMouse[0] < (self.x + self.width/2)):
            if (posMouse[1] > (self.y - self.height/2) and posMouse[1] < (self.y + self.height/2)):
                self.color = (180, 180, 180)
                pygame.event.post(pygame.event.Event(
                    pygame.USEREVENT, {"action": self.action}))
                return True

    def IsHoverOn(self, mouse_pos):
        self.hover = self.rect.collidepoint(mouse_pos)
        return self.hover

    def Clicked(self, mouse_action):
        if self.IsHoverOn:
            if mouse_action[0]:
                return True
            else:
                return False


class Button_img(Button):
    def __init__(self, x, y, action,  image, image_click=None):
        self.image = pygame.image.load(image).convert()
        if image_click is not None:
            self.image_click = pygame.image.load(image_click).convert()
        else:
            self.image_click = None
        super().__init__(x, y, self.image.get_width(), self.image.get_height(), action)
        self.rect = self.image.get_rect(center=(self.x, self.y))

    def show(self, screen):
        if self.hover and self.image_click is not None:
            screen.blit(pygame.transform.scale(
                self.image_click, (self.image.get_width(), self.image.get_height())), self.rect)
        else:
            screen.blit(pygame.transform.scale(
                self.image, (self.image.get_width(), self.image.get_height())), self.rect)


class Button_text(Button):

    def __init__(self, x, y, width, height, action, text, font=font1):
        self.text = text
        self.name = text
        self.font = font
        self.width = width
        self.height = height
        self.text_render = font.render(self.text, 1, (0, 0, 0))
        super().__init__(x, y, width, height, action)

    def show(self, screen, background=True):
        if background:
            pygame.draw.rect(screen, self.color, ((
                self.x-self.width/2), (self.y-self.height/2), self.width, self.height))
        screen.blit(self.text_render, (self.x-self.text_render.get_width() /
                    2, self.y-self.text_render.get_height()/2))
