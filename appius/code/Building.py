
from const import *
from Utils import cartCoToIsoCo


def type_of_tile(grid, name):
    x, y = grid
    match name:
        case "house":
            return Housing((x, y))
        case "hammer":
            return B_Engineering((x, y))
        case "sword":
            return Prefecture((x, y))
        case "water":
            return Water_well((x, y))
        case "rumble":
            return Rumble((x, y))


class Building:
    def __init__(self, pos):
        self.grid = pos
        self.grid_x, self.grid_y = pos
        self.rect = [
            (self.grid_x*TILE_SIZE, self.grid_y*TILE_SIZE),
            (self.grid_x*TILE_SIZE+TILE_SIZE, self.grid_y*TILE_SIZE),
            (self.grid_x*TILE_SIZE+TILE_SIZE, self.grid_y*TILE_SIZE+TILE_SIZE),
            (self.grid_x*TILE_SIZE, self.grid_y*TILE_SIZE+TILE_SIZE)
        ]
        self.iso_poly = [cartCoToIsoCo(x, y) for x, y in self.rect]
        min_x = min([x for x, y in self.iso_poly])
        min_y = min([y for x, y in self.iso_poly])
        self.map = [min_x, min_y]
        self.name = None  # {Tent,Temples,Prefecture,Well-water..}
        self.size = 1

        self.risk_collapse = 0  # 0:pas de risk
        self.risk_fire = 0
        self.canRemove = True
        self.canFire = False
        self.canCollapse = False
        self.onFire = False
        self.time_under_effect = 0
        # cant do nothing now, remove asap
        self.useless = False

        self.capacity = 0
        self.number_workers = 0
        self.price_building = 0
        self.currentNB = 0
        self.service = False
        self.needs = []

        self.collision = True

        self.tileImage = None
        self.imageOffset = 0

    # def position(self):
    #     return

    def _get_riskfeu(self):
        return self.riskfeu

    def _get_riskcollapse(self):
        return self.riskcollapse

    def _set_riskfire(self, n):
        self.risk_fire = n

    def _set_risk_criminality(self, n):
        self.risk_criminality = n

    def _set_risk_collapse(self, n):
        self.risk_collapse = n

    def _construct_me(self, world, offset, road_system):

        world.Building[self.grid_x].remove(
            world.Building[self.grid_x][self.grid_y])
        self.map[0] += offset
        world.Building[self.grid_x].insert(self.grid_y,
                                           self)
        if type(self) == Housing:
            road_system[self.grid_x][self.grid_y] = 'S'
        else:
            road_system[self.grid_x][self.grid_y] = 'X'
        if type(self) != Chemins:
            world.listBuilding.append(self)

    def _destroy_me(self, world, offset, road_system, H_R):
        if self in world.listBuilding:
            world.listBuilding.remove(self)
        world.Building[self.grid_x].remove(
            self)
        world.Building[self.grid_x].insert(self.grid_y,
                                           Grass((self.grid_x, self.grid_y)))
        road_system[self.grid_x][self.grid_y] = False
        world.Building[self.grid_x][self.grid_y].map[0] += offset

    def close_to_road(self, world):
        x, y = self.grid
        _surrounding = [(x-2, y-2), (x-2, y-1), (x-2, y), (x-2, y+1), (x-2, y+2), (x-1, y-2), (x-1, y-1), (x-1, y), (x-1, y+1), (x-1, y+2), (x, y-2), (x, y-1),
                        (x, y+1), (x, y+2), (x+1, y-2), (x+1, y-1), (x+1, y), (x+1, y+1), (x+1, y+2), (x+2, y-2), (x+2, y-1), (x+2, y), (x+2, y+1), (x+2, y+2)]
        _surrounding = [(x, y) for (x, y) in _surrounding if 0 <=
                        x < MAP_SIZE[0] and 0 <= y < MAP_SIZE[1]]
        for cell in _surrounding:
            if type(world.Building[cell[0]][cell[1]]) == Chemins:
                return cell
            else:
                continue
        return False

    def close_to_prefect(self, world):
        x, y = self.grid
        _surrounding = [(x-1, y-1), (x-1, y), (x-1, y+1),
                        (x, y-1), (x, y+1),
                        (x+1, y-1), (x+1, y), (x+1, y+1)]
        _surrounding = [(x, y) for (x, y) in _surrounding if 0 <=
                        x < MAP_SIZE[0] and 0 <= y < MAP_SIZE[1]]
        for cell in _surrounding:
            if type(world.Building[cell[0]][cell[1]]) == Prefecture:
                return cell
            else:
                continue
        return False


class Tent (Building):
    def __init__(self, pos):
        super().__init__(pos)
        self.canFire = True
        self.tileImage = pygame.image.load(
            "fonction_render/house/Housng1a_00002.png").convert_alpha()
        self.tileImage = pygame.transform.rotozoom(
            self.tileImage, 0, scaleDelta)
        self.imageOffset = self.tileImage.get_height()-TILE_SIZE
        self.name = 'Tent'
        self.price_building = 0
        self.statut = {"Panneau": 1, "Construction": 0, "Tent": 0,
                       "T_feu": 0, "T_collapse": 0}  # statut du batiment
        self.habitant = None
        self.water_source = None

    def update_NB(self):
        self.currentNB += 1

    def up_date_statut(self):  # a faire
        self.statut
        return None

    def _destroy_me(self, world, offset, road_system, H_R):
        if self.habitant in H_R.listWalker["Citizen"]:
            if not self.habitant.unemployed:
                self.habitant.company.list_employer.remove(self.habitant)
            H_R.listWalker["Citizen"].remove(self.habitant)
        H_R.calcul_pop()
        self.habitant = None
        super()._destroy_me(world, offset, road_system, H_R)

    def _evoluer(self, world):
        if self not in world.listonFire:
            temp = self.habitant
            if self in world.listBuilding:
                world.listBuilding.remove(self)
            pos = world.Building[self.grid_x][self.grid_y].map[0]
            well = self.water_source
            well.distribute.remove(self)
            world.Building[self.grid_x].remove(
                self)
            world.Building[self.grid_x].insert(self.grid_y,
                                               Tent_niv_2((self.grid_x, self.grid_y)))
            world.Building[self.grid_x][self.grid_y].map[0] = pos
            world.Building[self.grid_x][self.grid_y].habitant = temp
            world.Building[self.grid_x][self.grid_y].water_source = well
            well.distribute.append(world.Building[self.grid_x][self.grid_y])
            self.habitant.my_house = world.Building[self.grid_x][self.grid_y]
            world.listBuilding.append(world.Building[self.grid_x][self.grid_y])


class Tent_niv_2(Tent):
    def __init__(self, pos):
        super().__init__(pos)
        self.tileImage = pygame.image.load(
            "fonction_render/house/Housng1a_00019.png").convert_alpha()
        self.tileImage = pygame.transform.rotozoom(
            self.tileImage, 0, scaleDelta)
        self.imageOffset = self.tileImage.get_height()-TILE_SIZE

    def _devoluer(self, world):
        if self not in world.listonFire:
            temp = self.habitant
            if self in world.listBuilding:
                world.listBuilding.remove(self)
            pos = world.Building[self.grid_x][self.grid_y].map[0]
            world.Building[self.grid_x].remove(
                self)
            world.Building[self.grid_x].insert(self.grid_y,
                                               Tent((self.grid_x, self.grid_y)))
            world.Building[self.grid_x][self.grid_y].map[0] = pos
            world.Building[self.grid_x][self.grid_y].habitant = temp
            self.habitant.my_house = world.Building[self.grid_x][self.grid_y]
            world.listBuilding.append(world.Building[self.grid_x][self.grid_y])


class Prefecture(Building):
    def __init__(self, pos):
        super().__init__(pos)
        self.tileImage = pygame.image.load(
            "fonction_render/house/Security_00001.png").convert_alpha()
        self.tileImage = pygame.transform.rotozoom(
            self.tileImage, 0, scaleDelta)
        self.imageOffset = self.tileImage.get_height()-TILE_SIZE
        self.flag = pygame.image.load(
            "fonction_render/house/Security_00004.png").convert_alpha()
        self.flag = pygame.transform.rotozoom(
            self.flag, 0, scaleDelta)

        self.name = 'Prefecture'
        self.price_building = 30
        self.personnage = None
        self.statut = {"Prefecture": 1, "P_feu": 0, "P_collapse": 0}
        self.list_employer = []

    def is_employed(self):
        return self.personnage != None

    def show_flag(self, screen, camera):
        pos_x = self.map[0]+camera.scroll.x + \
            (self.tileImage.get_height()+self.flag.get_height())*0.35
        pos_y = self.map[1]+camera.scroll.y - \
            (self.tileImage.get_width()+self.flag.get_width())*0.22

        screen.blit(
            self.flag, (pos_x, pos_y))

    def up_date_statut():
        return None

    def _destroy_me(self, world, offset, road_system, H_R):
        for employer in self.list_employer:
            if employer in H_R.listWalker["Citizen"]:
                employer.unemployed = True
        super()._destroy_me(world, offset, road_system, H_R)


class Water_well(Building):  # puit
    def __init__(self, pos):
        super().__init__(pos)

        self.tileImage = pygame.image.load(
            "fonction_render/house/Utilitya_00001.png")
        self.tileImage = pygame.transform.rotozoom(
            self.tileImage, 0, scaleDelta)
        self.imageOffset = self.tileImage.get_height()-TILE_SIZE
        self.price_building = 5
        self.name = 'water_well'
        self.distribute = []

    def _destroy_me(self, world, offset, road_system, H_R):
        if self.distribute != []:
            for _ in self.distribute:
                # self.distribute.remove(_)
                _.water_source = None
        super()._destroy_me(world, offset, road_system, H_R)


class Senat(Building):
    def __init__(self, pos):
        super.__init__(self, pos)
        self.name = 'Senat'
        self.statut = {"Senat": 1, "S_feu": 0, "S_collapse": 0}
        self.umployment = 0
        self.culture_level = 0
        self.Peace_level = 0
        self.attractivity = 0
        self.population = 0
        self.price_building = 400

    def calcul_culture_level(self):
        return

    def calcul_Peace_level(self):
        return

    def calcul_attractuvity(self):
        return

    def calcul_populaton(self):
        return

    def up_date_statut():
        return None


class B_Engineering(Building):
    def __init__(self, pos):
        super().__init__(pos)

        self.tileImage = pygame.image.load(
            "fonction_render/house/transport_00056.png").convert_alpha()
        self.tileImage = pygame.transform.rotozoom(
            self.tileImage, 0, scaleDelta)
        self.imageOffset = self.tileImage.get_height()-TILE_SIZE
        self.name = 'B_Engineering'
        self.statut = {"B": 1, "B_feu": 0, "B_collapse": 0}
        self.price_building = 30
        self.canFire = True


''''sousclasse pour les temples'''


class Temples(Building):
    def __init__(self, pos):
        super.__init__(self, pos)
        self.name = 'Temples'
        self.nb_temples = 0
        self.price_building = 50

    def rate_satisfaction():        # a faire seulement le nombre des temples et le taille de la mapp

        return


class Ceres(Temples):
    def __init__(self, pos):
        super.__init__(self, pos)
        self.religion = 'Ceres'

    def rate_satisfaction():
        return


class Mars(Temples):
    def __init__(self, pos):
        super.__init__(self, pos)
        self.religion = 'Mars'

    def rate_satisfaction():
        return


class Mercury(Temples):
    def __init__(self, pos):
        super.__init__(self, pos)
        self.religion = 'Mercury'

    def rate_satisfaction():
        return


class Neptune (Temples):
    def __init__(self, pos):
        super.__init__(self, pos)
        self.religion = 'Neptune'

    def rate_satisfaction():
        return


class Venus(Temples):
    def __init__(self, pos):
        super.__init(self, pos)
        self.religon = 'Venus'

    def rate_satisfaction():
        return


# class Buildings:
#     def __init__(self):
#         ''' Une simple liste vide '''
#         self.listBuilding = []

#     def ajouter(self, B):
#         self.Building.append(B)

#     def retirer(self, B):
#         self.Building.remove(B)

#     def __iter__(self):                        #
#         return iter(self.Building)


class Grass(Building):
    def __init__(self, pos):
        super().__init__(pos)
        self.name = "grass"
        self.imageoffset = 0
        self.price_building = 2
        self.collision = False

        self.tileImage = pygame.image.load(
            "newland/Land1a_00285.png").convert_alpha()

        self.tileImage = pygame.transform.rotozoom(
            self.tileImage, 0, scaleDelta)


class Chemins(Building):
    def __init__(self, pos):
        super().__init__(pos)
        self.name = "road"
        self.imageoffset = 0
        self.price_building = 4
        self.collision = True
        self.north = False
        self.south = False
        self.west = False
        self.east = False

        self.tileImage = {"N": pygame.transform.rotozoom(pygame.image.load("Chemins/N.png").convert_alpha(), 0, scaleDelta), "S": pygame.transform.rotozoom(pygame.image.load("Chemins/S.png").convert_alpha(), 0, scaleDelta), "E": pygame.transform.rotozoom(pygame.image.load("Chemins/E.png").convert_alpha(), 0, scaleDelta), "W": pygame.transform.rotozoom(pygame.image.load("Chemins/W.png").convert_alpha(), 0, scaleDelta),
                          "N&E": pygame.transform.rotozoom(pygame.image.load("Chemins/N&E.png").convert_alpha(), 0, scaleDelta), "S&E": pygame.transform.rotozoom(pygame.image.load("Chemins/S&E.png").convert_alpha(), 0, scaleDelta), "W&N": pygame.transform.rotozoom(pygame.image.load("Chemins/W&N.png").convert_alpha(), 0, scaleDelta), "W&S": pygame.transform.rotozoom(pygame.image.load("Chemins/W&S.png").convert_alpha(), 0, scaleDelta),
                          "N_S_E": pygame.transform.rotozoom(pygame.image.load("Chemins/N_S_E.png").convert_alpha(), 0, scaleDelta), "N_W_S": pygame.transform.rotozoom(pygame.image.load("Chemins/N_W_S.png").convert_alpha(), 0, scaleDelta), "W_N_E": pygame.transform.rotozoom(pygame.image.load("Chemins/W_N_E.png").convert_alpha(), 0, scaleDelta), "W_S_E": pygame.transform.rotozoom(pygame.image.load("Chemins/W_S_E.png").convert_alpha(), 0, scaleDelta),
                          "S-N": pygame.transform.rotozoom(pygame.image.load("Chemins/S-N.png").convert_alpha(), 0, scaleDelta), "W-E": pygame.transform.rotozoom(pygame.image.load("Chemins/W-E.png").convert_alpha(), 0, scaleDelta),
                          "ALL": pygame.transform.rotozoom(pygame.image.load("Chemins/ALL.png").convert_alpha(), 0, scaleDelta)
                          }


# test


# class Component_of_House(Building):
#     def __init__(self, pos, component):
#         super().__init__(pos)
#         self.name = component
#         self.component = component
#         self.imageoffset = 0
#         self.price_building = 0
#         self.collision = True

#         self.tileImage = pygame.image.load(
#             "fonction_render/house/Housng1a_00045.png").convert_alpha()
#         self.tileImage = pygame.transform.rotozoom(
#             self.tileImage, 0, scaleDelta)

#     def _get_my_component(self):
#         return self.component


class BigHousing(Building):
    def __init__(self, pos):
        super().__init__(pos)
        self.name = "bighouse"

        self.price_building = 10
        self.collision = True
        self.surrond = None

        self.tileImage = pygame.image.load(
            "fonction_render/house/Housng1a_00005.png").convert_alpha()
        self.tileImage = pygame.transform.rotozoom(
            self.tileImage, 0, scaleDelta)
        self.imageOffset_y = self.tileImage.get_height()-TILE_SIZE*1.5
        self.imageOffset_x = self.tileImage.get_width()-TILE_SIZE*4
        self.canFire = True
        self.size = 2

    def _contruct_big_house(self, world, offset):

        relative_1 = BigHousing((self.grid_x, self.grid_y-1))
        relative_2 = BigHousing((self.grid_x+1, self.grid_y-1))
        relative_3 = BigHousing((self.grid_x+1, self.grid_y))
        relative_1.tileImage = None
        relative_2.tileImage = None
        relative_3.tileImage = None

        self.surrond = [self, relative_1, relative_2, relative_3]
        relative_1.surrond = self.surrond
        relative_2.surrond = self.surrond
        relative_3.surrond = self.surrond
        self._construct_me(world, offset)
        relative_1._construct_me(world, offset)
        relative_2._construct_me(world, offset)
        relative_3._construct_me(world, offset)

    def _destroy_big_house(self, world, offset, H_R):
        for sur in self.surrond:
            sur._destroy_me(world, offset, H_R)


class Housing(Building):
    def __init__(self, pos):
        super().__init__(pos)
        self.name = "house"
        self.imageoffset = 0
        self.price_building = 10
        self.collision = True
        self.available = True

        self.tileImage = pygame.image.load(
            "fonction_render/house/Housng1a_00045.png").convert_alpha()
        self.tileImage = pygame.transform.rotozoom(
            self.tileImage, 0, scaleDelta)


class Rumble(Building):
    def __init__(self, pos):
        super().__init__(pos)
        self.name = "trash"
        self.imageoffset = 0
        self.price_building = 0
        self.collision = True
        self.canCollapse = False
        self.canFire = False
        self.canRemove = True
        self.risk_fire = 0
        self.risk_collapse = 0
        self.useless = True

        self.tileImage = RUMBLE_OF_BUILDING

        # self.tileImage = pygame.transform.rotozoom(
        #     self.tileImage, 0, scaleDelta)

# class for test


class Buildings:
    def __init__(self):
        ''' Une simple liste vide '''
        self.Building = []
        self.listBuilding = []
        self.listonFire = []

    def __iter__(self):
        return iter(self.Building)

    def ajouter(self, Building):  # ajouter
        self.list.append(Building)

    def retirer(self, Buiding):
        self.list.remove(Buiding)
