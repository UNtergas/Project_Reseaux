import pygame


class Camera:

    def __init__(self, width, height, boundary):

        self.width = width
        self.height = height

        self.keys = {
            pygame.K_UP: False,
            pygame.K_LEFT: False,
            pygame.K_DOWN: False,
            pygame.K_RIGHT: False,
        }
        self.boundary = boundary
        self.mousePos = (0, 0)
        self.scroll = pygame.Vector2(0, 0)
        self.scroll.x = -self.boundary[0]*0.4
        self.scroll.y = -self.boundary[1]*0.004
        self.mousseMouvSpeed = 20
        self.keyboardMouvSpeed = 20

    def movement_arrow(self):
        # print(f"scroll:{self.scroll.x,self.scroll.y}")

        if self.scroll.x > self.boundary[0]*0.05:
            self.scroll.x = self.boundary[0]*0.05
        elif self.scroll.x < -self.boundary[0]*0.775:
            self.scroll.x = -self.boundary[0]*0.775
        elif self.scroll.y > self.boundary[1]*0.08:
            self.scroll.y = self.boundary[1]*0.08
        elif self.scroll.y < -self.boundary[1]*0.75:
            self.scroll.y = -self.boundary[1]*0.75
        self.scroll.x += (self.keys[pygame.K_LEFT] -
                          self.keys[pygame.K_RIGHT])*self.keyboardMouvSpeed
        self.scroll.y += (self.keys[pygame.K_UP] -
                          self.keys[pygame.K_DOWN])*self.keyboardMouvSpeed

    def movement_mouse(self):

        # x movement# map boundary
        if self.scroll.x > self.boundary[0]*0.05:
            self.scroll.x = self.boundary[0]*0.05
        elif self.scroll.x < -self.boundary[0]*0.775:
            self.scroll.x = -self.boundary[0]*0.775
        elif self.scroll.y > self.boundary[1]*0.08:
            self.scroll.y = self.boundary[1]*0.08
        elif self.scroll.y < -self.boundary[1]*0.75:
            self.scroll.y = -self.boundary[1]*0.75

        # x movement
        if self.mousePos[0] > self.width * 0.97:
            self.scroll.x += -self.mousseMouvSpeed
        elif self.mousePos[0] < self.width * 0.03:
            self.scroll.x += self.mousseMouvSpeed
        # y movement
        if self.mousePos[1] > self.height * 0.97:
            self.scroll.y += -self.mousseMouvSpeed
        elif self.mousePos[1] < self.height * 0.03:
            self.scroll.y += self.mousseMouvSpeed
