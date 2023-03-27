import pygame
from Utils import get_ratio
import copy


class Minimap:
    def __init__(self, real_width, real_height, mini_width, mini_height, mattrice, pos) -> None:
        self.real_width = real_width
        self.real_height = real_height
        self.mini_width = mini_width
        self.mini_height = mini_height
        self.pos = pos
        self.ratio_width = get_ratio(real_width, mini_width)
        self.ratio_height = get_ratio(real_height, mini_height)
        #
        self.real_x_y_ratio = self.real_width/self.real_height
        self.mini_x_y_ratio = self.mini_width/self.mini_height
        self.x_y_ratio = self.real_x_y_ratio/self.mini_x_y_ratio
        self.array = []
        #
        self.mattrice = mattrice
        self.mini_map = self.creation_surface()
        self.mini_rect = pygame.Rect(
            pos[0], pos[1], self.mini_width, self.mini_height)

        self.mini_camera_rect = None
        self.mini_scroll_x = 0
        self.mini_scroll_y = 0
        #
        self.building = ["water_well", "B_Engineering", "house", "Prefecture"]

    def creation_surface(self):
        mini_map = pygame.Surface((self.real_width, self.real_height))
        for x in self.mattrice:
            for building in x:
                grid = building.iso_poly
                grid = [(x + self.real_width/2, y)
                        for x, y in grid]
                if building.name == "grass":
                    pygame.draw.polygon(mini_map, (153, 255, 51), grid)
                elif building.name == "road":
                    pygame.draw.polygon(mini_map, (153, 76, 0), grid)
                elif building.name in self.building:
                    pygame.draw.polygon(mini_map, (255, 255, 51), grid)

        mini_map = pygame.transform.scale(
            mini_map, (self.real_width*self.ratio_width, self.real_height*self.ratio_height))

        return mini_map

    def update_surface(self, grid, type):
        grid = [((x + self.real_width/2)*self.ratio_width, y*self.ratio_height)
                for x, y in grid]
        color = (255, 255, 255)
        match type:
            case "road":
                color = (153, 76, 0)
            case "building":
                color = (255, 255, 51)
            case "grass":
                color = (153, 255, 51)
        pygame.draw.polygon(self.mini_map, color, grid)

    def update_mode_interactive(self, mousePos, mouseAction, camera):
        print(mousePos)
        if self.mini_rect.collidepoint(mousePos):
            print("isonminin")
            relative_x = (mousePos[0]-self.pos[0])
            relative_y = (mousePos[1]-self.pos[1])
            if mouseAction[0]:
                camera.scroll.x = -(relative_x/self.ratio_width)
                camera.scroll.y = -(relative_y/self.ratio_height)
                camera.scroll.x += camera.width/2
                camera.scroll.y += camera.height/2

    def update_scrolling(self, camera):
        self.mini_camera_rect = pygame.Rect(
            self.pos[0], self.pos[1], camera.width*self.ratio_width, camera.height*self.ratio_height)
        self.mini_scroll_x = -(camera.scroll.x)*self.ratio_width
        self.mini_scroll_y = -(camera.scroll.y)*self.ratio_height
        self.mini_camera_rect.x += self.mini_scroll_x
        self.mini_camera_rect.y += self.mini_scroll_y

    def draw(self, screen,  camera):
        self.update_scrolling(camera)
        screen.blit(self.mini_map, self.pos)
        pygame.draw.rect(screen, (200, 0, 0), self.mini_camera_rect, 1)