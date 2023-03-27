from Building import Chemins
import random
import pygame
from const import *
from Utils import A_star, polygon_center


class Walker():
    def __init__(self, spawnpoint=(0, 0), goal=None):

        self.range = 0
        # self.building = None
        # self.type = None
        self.map = None
        self.path = []
        self.dir = (0, 0)
        self.pos = spawnpoint
        self.rayonDAction = 0
        self.unemployed = True  # unemployed pour définir la statut d'un walker]
        self.sprite_list = {
            (0, -1): [pygame.transform.rotozoom(pygame.image.load("Walkers/Citizen01/Citizen01_00001.png").convert_alpha(
            ), 0, scaleDelta), pygame.transform.rotozoom(pygame.image.load("Walkers/Citizen01/Citizen01_00009.png").convert_alpha(
            ), 0, scaleDelta), pygame.transform.rotozoom(pygame.image.load("Walkers/Citizen01/Citizen01_00017.png").convert_alpha(
            ), 0, scaleDelta), pygame.transform.rotozoom(pygame.image.load("Walkers/Citizen01/Citizen01_00025.png").convert_alpha(
            ), 0, scaleDelta), pygame.transform.rotozoom(pygame.image.load("Walkers/Citizen01/Citizen01_00033.png").convert_alpha(
            ), 0, scaleDelta), pygame.transform.rotozoom(pygame.image.load("Walkers/Citizen01/Citizen01_00041.png").convert_alpha(
            ), 0, scaleDelta), pygame.transform.rotozoom(pygame.image.load("Walkers/Citizen01/Citizen01_00065.png").convert_alpha(
            ), 0, scaleDelta), pygame.transform.rotozoom(pygame.image.load("Walkers/Citizen01/Citizen01_00073.png").convert_alpha(
            ), 0, scaleDelta), pygame.transform.rotozoom(pygame.image.load("Walkers/Citizen01/Citizen01_00081.png").convert_alpha(
            ), 0, scaleDelta), pygame.transform.rotozoom(pygame.image.load("Walkers/Citizen01/Citizen01_00089.png").convert_alpha(), 0, scaleDelta)],
            (0, 1): [pygame.transform.rotozoom(pygame.image.load("Walkers/Citizen01/Citizen01_00005.png").convert_alpha(
            ), 0, scaleDelta), pygame.transform.rotozoom(pygame.image.load("Walkers/Citizen01/Citizen01_00013.png").convert_alpha(
            ), 0, scaleDelta), pygame.transform.rotozoom(pygame.image.load("Walkers/Citizen01/Citizen01_00021.png").convert_alpha(
            ), 0, scaleDelta), pygame.transform.rotozoom(pygame.image.load("Walkers/Citizen01/Citizen01_00029.png").convert_alpha(
            ), 0, scaleDelta), pygame.transform.rotozoom(pygame.image.load("Walkers/Citizen01/Citizen01_00037.png").convert_alpha(
            ), 0, scaleDelta), pygame.transform.rotozoom(pygame.image.load("Walkers/Citizen01/Citizen01_00045.png").convert_alpha(
            ), 0, scaleDelta), pygame.transform.rotozoom(pygame.image.load("Walkers/Citizen01/Citizen01_00053.png").convert_alpha(
            ), 0, scaleDelta), pygame.transform.rotozoom(pygame.image.load("Walkers/Citizen01/Citizen01_00069.png").convert_alpha(
            ), 0, scaleDelta), pygame.transform.rotozoom(pygame.image.load("Walkers/Citizen01/Citizen01_00077.png").convert_alpha(
            ), 0, scaleDelta), pygame.transform.rotozoom(pygame.image.load("Walkers/Citizen01/Citizen01_00093.png").convert_alpha(), 0, scaleDelta)],
            (-1, 0): [pygame.transform.rotozoom(pygame.image.load("Walkers/Citizen01/Citizen01_00007.png").convert_alpha(
            ), 0, scaleDelta), pygame.transform.rotozoom(pygame.image.load("Walkers/Citizen01/Citizen01_00015.png").convert_alpha(
            ), 0, scaleDelta), pygame.transform.rotozoom(pygame.image.load("Walkers/Citizen01/Citizen01_00023.png").convert_alpha(
            ), 0, scaleDelta), pygame.transform.rotozoom(pygame.image.load("Walkers/Citizen01/Citizen01_00031.png").convert_alpha(
            ), 0, scaleDelta), pygame.transform.rotozoom(pygame.image.load("Walkers/Citizen01/Citizen01_00039.png").convert_alpha(
            ), 0, scaleDelta), pygame.transform.rotozoom(pygame.image.load("Walkers/Citizen01/Citizen01_00047.png").convert_alpha(
            ), 0, scaleDelta), pygame.transform.rotozoom(pygame.image.load("Walkers/Citizen01/Citizen01_00055.png").convert_alpha(
            ), 0, scaleDelta), pygame.transform.rotozoom(pygame.image.load("Walkers/Citizen01/Citizen01_00071.png").convert_alpha(
            ), 0, scaleDelta), pygame.transform.rotozoom(pygame.image.load("Walkers/Citizen01/Citizen01_00079.png").convert_alpha(
            ), 0, scaleDelta), pygame.transform.rotozoom(pygame.image.load("Walkers/Citizen01/Citizen01_00095.png").convert_alpha(), 0, scaleDelta)],
            (1, 0): [pygame.transform.rotozoom(pygame.image.load("Walkers/Citizen01/Citizen01_00003.png").convert_alpha(
            ), 0, scaleDelta), pygame.transform.rotozoom(pygame.image.load("Walkers/Citizen01/Citizen01_00011.png").convert_alpha(
            ), 0, scaleDelta), pygame.transform.rotozoom(pygame.image.load("Walkers/Citizen01/Citizen01_00019.png").convert_alpha(
            ), 0, scaleDelta), pygame.transform.rotozoom(pygame.image.load("Walkers/Citizen01/Citizen01_00027.png").convert_alpha(
            ), 0, scaleDelta), pygame.transform.rotozoom(pygame.image.load("Walkers/Citizen01/Citizen01_00035.png").convert_alpha(
            ), 0, scaleDelta), pygame.transform.rotozoom(pygame.image.load("Walkers/Citizen01/Citizen01_00043.png").convert_alpha(
            ), 0, scaleDelta), pygame.transform.rotozoom(pygame.image.load("Walkers/Citizen01/Citizen01_00051.png").convert_alpha(
            ), 0, scaleDelta), pygame.transform.rotozoom(pygame.image.load("Walkers/Citizen01/Citizen01_00059.png").convert_alpha(
            ), 0, scaleDelta), pygame.transform.rotozoom(pygame.image.load("Walkers/Citizen01/Citizen01_00067.png").convert_alpha(
            ), 0, scaleDelta), pygame.transform.rotozoom(pygame.image.load("Walkers/Citizen01/Citizen01_00091.png").convert_alpha(), 0, scaleDelta)]
        }
        self.sprite = pygame.transform.rotozoom(pygame.image.load("Walkers/Citizen01/Citizen01_00001.png").convert_alpha(
        ), 0, scaleDelta)
        self.dir_path = []
        self.path = [self.pos]
        self.goal = goal
        self.path_index = 0
        self.my_house = None
        self.movement_clock = 0
        self.company = None
        self.target = (0, 0)
        self.coef = (0, 0)
        self.time_index = 0

    def mouv(self, grid, world):
        self.dir = self.getRandomValideDir(grid)
        self.smooth(world)

    def getRandomValideDir(self, grid):
        dirs = [dir for dir in [(0, -1), (1, 0), (0, 1), (-1, 0)]
                if self.isNextPosValide(dir, grid)]
        return random.choice(dirs if (len(dirs) > 0) else [(self.dir[0]*-1, self.dir[1]*-1)])

    def isNextPosValide(self, dir, grid):
        nextPos = (self.pos[0] + dir[0],
                   self.pos[1] + dir[1])

        isNextPosInRange = MAP_SIZE[0] > nextPos[0] >= 0 and\
            MAP_SIZE[1] > nextPos[1] >= 0

        isNextPosAPath = False
        if isNextPosInRange:

            isNextPosAPath = grid[nextPos[0]][nextPos[1]] == True
            # isNextPosAPath = type(grid[nextPos[0]][nextPos[1]]) == Chemins

        isNextPosBackward = dir == (self.dir[0]*-1, self.dir[1]*-1)

        return isNextPosInRange and isNextPosAPath and not isNextPosBackward

    def work():
        # NE PAS MODIFIER
        return

    def draw(self, camera, screen, world):
        cell_relative = world.Building[self.pos[0]][self.pos[1]]
        pos_x = cell_relative.map[0]+self.coef[0] + \
            (2*TILE_SIZE-self.sprite.get_width())*0.5
        pox_y = cell_relative.map[1]+self.coef[1] + \
            (TILE_SIZE-self.sprite.get_height())*0.5
        screen.blit(self.sprite.convert_alpha(),
                    (pos_x+camera.scroll.x, pox_y+camera.scroll.y))

    def path_finding(self, grid):
        if self.goal != None:
            self.path = A_star(
                (self.pos[0], self.pos[1]), (self.goal[0], self.goal[1]), grid)
            self.dir_path = [(0, -1)]+[(self.path[i+1][0] - self.path[i][0], self.path[i+1][1] - self.path[i][1])
                                       for i in range(len(self.path) - 1)]

    def smooth(self, world, end=False):
        # if self.pos == self.target:
        #     self.coef = (0, 0)
        #     self.movement_clock = 0
        # else:
        if end or self.dir == (0, 0):
            self.sprite = self.sprite_list[(1, 0)][round((
                self.movement_clock*10) % 9)]
            self.coef = (0, 0)
        else:
            self.target = (self.pos[0] + self.dir[0],
                           self.pos[1] + self.dir[1])
            if 0 <= self.target[0] < MAP_SIZE[0] and 0 <= self.target[1] < MAP_SIZE[1]:
                debut = polygon_center(
                    world.Building[self.pos[0]][self.pos[1]].iso_poly)
                end = polygon_center(
                    world.Building[self.target[0]][self.target[1]].iso_poly)

                distance = -pygame.math.Vector2(
                    debut[0], debut[1]) + pygame.math.Vector2(end[0], end[1])
                # print(distance*self.movement_clock)
                # if self.movement_clock >= 1:
                #     self.movement_clock = 0
                self.sprite = self.sprite_list[self.dir][round((
                    self.movement_clock*10) % 9)]
                self.coef = distance*self.movement_clock


class Engineer(Walker):
    def __init__(self, save):
        Walker.__init__(self, save)
        self.type = "Engineer"
        self.unemployed = False

    def work(self, Buildings):
        assert (type(Buildings) == Buildings)
        r = self.rayonDAction
        for i in range(self.pos[0]-r, self.pos[0]+r):
            for j in range(self.pos[1]-r, self.pos[1]+r):
                for b in Buildings.listBuilding.keys():                 # a refaire
                    for k in Buildings.listBuilding[b]:
                        if ((i, j) == k.grid) and (k.risk_collapse > 0):
                            k._set_risk_collapse(0)


class Prefect(Walker):
    def __init__(self, spawnpoint=(0, 0), goal=None):
        super().__init__(spawnpoint, goal)
        self.type = "Prefect"
        self.travailleur = 0
        self.unemployed = False
        self.headquarter = None
        self.missionaire = None
        self.returning = False
        self.rayonDAction = 2
        self.sprite_list = {(0, -1): [pygame.transform.rotozoom(pygame.image.load("Walkers/Prefect/citizen02_00615.png").convert_alpha(
        ), 0, scaleDelta), pygame.transform.rotozoom(pygame.image.load("Walkers/Prefect/citizen02_00623.png").convert_alpha(
        ), 0, scaleDelta), pygame.transform.rotozoom(pygame.image.load("Walkers/Prefect/citizen02_00631.png").convert_alpha(
        ), 0, scaleDelta), pygame.transform.rotozoom(pygame.image.load("Walkers/Prefect/citizen02_00639.png").convert_alpha(
        ), 0, scaleDelta), pygame.transform.rotozoom(pygame.image.load("Walkers/Prefect/citizen02_00647.png").convert_alpha(
        ), 0, scaleDelta), pygame.transform.rotozoom(pygame.image.load("Walkers/Prefect/citizen02_00655.png").convert_alpha(
        ), 0, scaleDelta), pygame.transform.rotozoom(pygame.image.load("Walkers/Prefect/citizen02_00663.png").convert_alpha(
        ), 0, scaleDelta), pygame.transform.rotozoom(pygame.image.load("Walkers/Prefect/citizen02_00679.png").convert_alpha(
        ), 0, scaleDelta), pygame.transform.rotozoom(pygame.image.load("Walkers/Prefect/citizen02_00695.png").convert_alpha(
        ), 0, scaleDelta), pygame.transform.rotozoom(pygame.image.load("Walkers/Prefect/citizen02_00703.png").convert_alpha(), 0, scaleDelta)],
            (0, 1): [pygame.transform.rotozoom(pygame.image.load("Walkers/Prefect/citizen02_00619.png").convert_alpha(
            ), 0, scaleDelta), pygame.transform.rotozoom(pygame.image.load("Walkers/Prefect/citizen02_00627.png").convert_alpha(
            ), 0, scaleDelta), pygame.transform.rotozoom(pygame.image.load("Walkers/Prefect/citizen02_00635.png").convert_alpha(
            ), 0, scaleDelta), pygame.transform.rotozoom(pygame.image.load("Walkers/Prefect/citizen02_00643.png").convert_alpha(
            ), 0, scaleDelta), pygame.transform.rotozoom(pygame.image.load("Walkers/Prefect/citizen02_00651.png").convert_alpha(
            ), 0, scaleDelta), pygame.transform.rotozoom(pygame.image.load("Walkers/Prefect/citizen02_00659.png").convert_alpha(
            ), 0, scaleDelta), pygame.transform.rotozoom(pygame.image.load("Walkers/Prefect/citizen02_00667.png").convert_alpha(
            ), 0, scaleDelta), pygame.transform.rotozoom(pygame.image.load("Walkers/Prefect/citizen02_00683.png").convert_alpha(
            ), 0, scaleDelta), pygame.transform.rotozoom(pygame.image.load("Walkers/Prefect/citizen02_00699.png").convert_alpha(
            ), 0, scaleDelta), pygame.transform.rotozoom(pygame.image.load("Walkers/Prefect/citizen02_00707.png").convert_alpha(), 0, scaleDelta)],
            (-1, 0): [pygame.transform.rotozoom(pygame.image.load("Walkers/Prefect/citizen02_00621.png").convert_alpha(
            ), 0, scaleDelta), pygame.transform.rotozoom(pygame.image.load("Walkers/Prefect/citizen02_00629.png").convert_alpha(
            ), 0, scaleDelta), pygame.transform.rotozoom(pygame.image.load("Walkers/Prefect/citizen02_00637.png").convert_alpha(
            ), 0, scaleDelta), pygame.transform.rotozoom(pygame.image.load("Walkers/Prefect/citizen02_00645.png").convert_alpha(
            ), 0, scaleDelta), pygame.transform.rotozoom(pygame.image.load("Walkers/Prefect/citizen02_00653.png").convert_alpha(
            ), 0, scaleDelta), pygame.transform.rotozoom(pygame.image.load("Walkers/Prefect/citizen02_00661.png").convert_alpha(
            ), 0, scaleDelta), pygame.transform.rotozoom(pygame.image.load("Walkers/Prefect/citizen02_00677.png").convert_alpha(
            ), 0, scaleDelta), pygame.transform.rotozoom(pygame.image.load("Walkers/Prefect/citizen02_00685.png").convert_alpha(
            ), 0, scaleDelta), pygame.transform.rotozoom(pygame.image.load("Walkers/Prefect/citizen02_00693.png").convert_alpha(
            ), 0, scaleDelta), pygame.transform.rotozoom(pygame.image.load("Walkers/Prefect/citizen02_00709.png").convert_alpha(), 0, scaleDelta)],
            (1, 0): [pygame.transform.rotozoom(pygame.image.load("Walkers/Prefect/citizen02_00617.png").convert_alpha(
            ), 0, scaleDelta), pygame.transform.rotozoom(pygame.image.load("Walkers/Prefect/citizen02_00625.png").convert_alpha(
            ), 0, scaleDelta), pygame.transform.rotozoom(pygame.image.load("Walkers/Prefect/citizen02_00633.png").convert_alpha(
            ), 0, scaleDelta), pygame.transform.rotozoom(pygame.image.load("Walkers/Prefect/citizen02_00641.png").convert_alpha(
            ), 0, scaleDelta), pygame.transform.rotozoom(pygame.image.load("Walkers/Prefect/citizen02_00649.png").convert_alpha(
            ), 0, scaleDelta), pygame.transform.rotozoom(pygame.image.load("Walkers/Prefect/citizen02_00665.png").convert_alpha(
            ), 0, scaleDelta), pygame.transform.rotozoom(pygame.image.load("Walkers/Prefect/citizen02_00673.png").convert_alpha(
            ), 0, scaleDelta), pygame.transform.rotozoom(pygame.image.load("Walkers/Prefect/citizen02_00681.png").convert_alpha(
            ), 0, scaleDelta), pygame.transform.rotozoom(pygame.image.load("Walkers/Prefect/citizen02_00697.png").convert_alpha(
            ), 0, scaleDelta), pygame.transform.rotozoom(pygame.image.load("Walkers/Prefect/citizen02_00705.png").convert_alpha(), 0, scaleDelta)],
            "action": [pygame.transform.rotozoom(pygame.image.load("Walkers/Prefect/citizen02_00907.png").convert_alpha(
            ), 0, scaleDelta), pygame.transform.rotozoom(pygame.image.load("Walkers/Prefect/citizen02_00900.png").convert_alpha(
            ), 0, scaleDelta), pygame.transform.rotozoom(pygame.image.load("Walkers/Prefect/citizen02_00884.png").convert_alpha(
            ), 0, scaleDelta)]}
        self.sprite = pygame.transform.rotozoom(pygame.image.load("Walkers/Prefect/citizen02_00615.png").convert_alpha(
        ), 0, scaleDelta)

    def work(self, listBuilding):
        r = self.rayonDAction
        # assert (type(Buildings) == Buildings)
        for i in range(self.pos[0]-r, self.pos[0]+r):  # a refaire
            for j in range(self.pos[1]-r, self.pos[1]+r):
                for b in listBuilding:
                    if ((i, j) == b.grid) and (b.risk_fire > 0):
                        b._set_riskfire(0)


class Citizen(Walker):
    def __init__(self, spawnpoint=(0, 0), goal=None):
        super().__init__(spawnpoint, goal)
        self.type = "Citizen"

    def work(self, Buildings):
        assert (type(Buildings) == Buildings)
        r = self.rayonDAction
        for i in range(self.pos[0]-r, self.pos[0]+r):
            for j in range(self.pos[1]-r, self.pos[1]+r):
                for b in Buildings.listBuilding:
                    if (b.type == 'Tent'):
                        if ((i, j) == b.grid) and (b.currentNB < b.capacity):
                            b.updateNB()
                            break


class Walkers():
    # une sorte de base de donnée pour les Walkers
    # sauvegarde des Walkers dans un dict selon leurs types
    # sauvegarde des citizen dans une liste
    def __init__(self):
        self.listWalker = {"Citizen": [], "Prefect": [],
                           "Engineer": [], "Immigrant": []}
        self.pop = 0
        self.possible_prefect = 0
        self.possible_engi = 0

    def _get_possible_prefect(self):
        return self.pop*4 - len(self.listWalker["Prefect"])

    def _get_possible_engi(self):
        return self.pop*4 - len(self.listWalker["Engineer"])

    def _get_pop(self):
        return self.pop

    def _set_pop(self, p):
        self.pop = p

    def calcul_pop(self):
        self.pop = len(self.listWalker["Citizen"])+len(
            self.listWalker["Prefect"])+len(self.listWalker["Engineer"])

    def unemployment_rate(self):
        l = self.listWalker["Citizen"]
        self.calcul_pop
        assert self.pop > 0, "la population est nulle"
        nb = 0
        for i in l:
            if (i.unemployed):
                nb += 1
        return nb/self._get_pop(self)

    # Gestion des citizens
    def ajout_Citizen(self, C):
        assert (type(C) == Citizen)
        self.listWalker["Citizen"].append(C)

    def supp_Citizen(self, C):
        assert (type(C) == Citizen)
        self.listWalker["Citizen"].remove(C)

    # Gestion de Prefet
    def ajout_Prefet(self, P):
        assert (type(P) == Prefect)
        self.listWalker["Prefect"].append(P)

    def supp_Prefet(self, P):
        assert (type(P) == Prefect)
        self.listWalker["Prefect"].remove(P)

    # Gestion de Engineer
    def ajout_Engineer(self, E):
        assert (type(E) == Engineer)
        self.listWalker["Engineer"].append(E)

    def supp_Engineer(self, E):
        assert (type(E) == Engineer)
        self.listWalker["Engineer"].remove(E)
