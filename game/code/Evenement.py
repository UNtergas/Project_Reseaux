import pygame
from const import FIRE_THRESHOLD, COLLAPSE_THESHOLD, BURNING_TIME, MAP_SIZE
from Building import Housing, Tent, Prefecture, Tent_niv_2, Water_well
from Walker import Walker, Prefect
from Utils import manhattan_distance
import random


class Evenement:

    def __init__(self) -> None:
        self.timer = pygame.time.get_ticks()
        self.game_speed = 1
        self.day = 0.05

        self.day_pass = 0
        self.month = self.day_pass / 5
        self.year = self.month / 12
        self.movement = 0
        self.pop = 0

    def calendar_update(self):
        self.day_pass += self.day*self.game_speed

    def change_game_speed(self, speed):
        self.game_speed = speed

    def change_building_timer(self, listonFire):
        for building in listonFire:
            if building.onFire:
                building.time_under_effect += self.day*0.5*self.game_speed

    def change_risk_fire(self, world):
        for building in world.listBuilding:
            if building.close_to_prefect(world):
                building._set_riskfire(1)
            if building.canFire:
                # print(f"risk{building.risk_fire}")
                building.risk_fire += self.day*0.5*self.game_speed

    def set_on_fire(self, listBuilding):
        for building in listBuilding:
            # print(f"risk{building.onFire,building.canRemove}")
            if building.risk_fire >= FIRE_THRESHOLD and building.canFire:
                # print("setOnfire")
                building.onFire = True
                building.useless = True
                building.canRemove = False
                building.canFire = False

    def done_burning(self, listonFire):
        # print(listonFire)
        for building in listonFire:
            # print(f"risk{building.onFire},timer{building.time_under_effect}")

            if building.time_under_effect >= BURNING_TIME:
                # print("done buring")
                building.canRemove = True
                building.onFire = False

    def vacane_slot(self, world, H_R, road_system, offset):

        for building in world.listBuilding:
            if type(building) == Housing:
                if building.close_to_road(world):
                    if building.available:
                        if H_R.listWalker["Immigrant"] != None:
                            for walker in H_R.listWalker["Immigrant"]:
                                if not walker.my_house:
                                    walker.goal = building.grid
                                    walker.my_house = building
                                    walker.path_finding(road_system)
                                    walker.path_index = 0
                                    building.available = False
                                    break
                                else:
                                    continue
                            spawning = Walker((20, 39))
                            spawning.goal = building.grid
                            spawning.path_finding(road_system)
                            spawning.path_index = 0
                            spawning.my_house = building
                            H_R.listWalker["Immigrant"].append(spawning)
                            building.available = False

        for walker in H_R.listWalker["Immigrant"]:
            if walker.my_house not in world.listBuilding:
                walker.goal = (20, 0)
                if walker.my_house != None:
                    walker.path_finding(road_system)
                    walker.path_index = 0
                    walker.my_house = None
            arrived = self.walker_move(walker, world)
            if arrived:
                if walker.my_house != None:
                    self.building_sign_to_house(
                        walker, world.Building, world.listBuilding, offset, road_system)
                    H_R.pop += 1
                    H_R.listWalker["Citizen"].append(walker)
                H_R.listWalker["Immigrant"].remove(walker)

    def building_sign_to_house(self, walker, Building, listBuilding, offset, road_system):
        x, y = walker.pos
        if Building[x][y] in listBuilding:
            listBuilding.remove(Building[x][y])
        Building[x].remove(Building[x][y])
        Building[x].insert(y, Tent((x, y)))
        road_system[x][y] = 'X'
        Building[x][y].map[0] += offset
        Building[x][y].habitant = walker
        listBuilding.append(Building[x][y])

    def walker_move(self, walker, world):
        if walker.path != None:
            if walker.path_index >= len(walker.path) or walker.path_index >= len(walker.dir_path):
                return True

            new_pos = walker.path[int(walker.path_index)]
            new_dir = walker.dir_path[int(walker.path_index)]
            walker.pos = new_pos
            walker.dir = new_dir
            # walker.target = next_pos
            if walker.path_index >= len(walker.path)-1 or walker.path_index >= len(walker.dir_path)-1:
                # print("end it")
                walker.smooth(world, True)
            else:
                walker.smooth(world)
            walker.path_index += self.day*self.game_speed
            walker.movement_clock = abs(int(walker.path_index) -
                                        walker.path_index)

        return False

    def employing_prefect(self, world, H_R):
        for building in world.listBuilding:
            if type(building) == Prefecture:
                if building.personnage == None:
                    unemployed = [
                        a for a in H_R.listWalker["Citizen"] if a.unemployed == True]
                    if len(unemployed) > 4:
                        count = 0
                        for _ in unemployed:
                            if count >= 4:
                                break
                            _.unemployed = False
                            _.company = building
                            building.list_employer.append(_)
                            count += 1

                    spawnpoint = building.close_to_road(world)
                    if not spawnpoint:
                        if building.personnage != None:
                            H_R.listWalker["Prefect"].remove(prefect)
                            building.personnage = None
                        print("prefect too far from road")
                    else:
                        if len(building.list_employer) >= 4:
                            prefect = Prefect(spawnpoint)
                            prefect.headquarter = building
                            prefect.returning = False
                            prefect.missionaire = None
                            building.personnage = prefect
                            H_R.listWalker["Prefect"].append(prefect)

        for prefect in H_R.listWalker["Prefect"]:
            if prefect.headquarter not in world.listBuilding or not prefect.headquarter.close_to_road(world) or len(prefect.headquarter.list_employer) < 4:
                prefect.headquarter.personnage = None
                prefect.headquarter = None
                H_R.listWalker["Prefect"].remove(prefect)

    def Patrol(self, H_R, road_system, world):
        for prefect in H_R.listWalker["Prefect"]:
            if prefect.missionaire == None and prefect.returning == False:
                prefect.time_index += self.day*self.game_speed
                prefect.movement_clock = abs(int(prefect.time_index) -
                                             prefect.time_index)
                prefect.mouv(road_system, world)
                # print(int(prefect.movement_clock))
                if int(prefect.time_index) >= 1:
                    prefect.pos = (prefect.pos[0] + prefect.dir[0],
                                   prefect.pos[1] + prefect.dir[1])
                    prefect.time_index = 0
            prefect.work(world.listBuilding)

    def Find_Fire(self, H_R, world, road_system):
        for onFire in world.listonFire:
            x, y = onFire.grid
            surround = [(x+1, y), (x, y-1), (x-1, y), (x, y+1)]
            surround = [(x, y) for (x, y) in surround if 0 <=
                        x < MAP_SIZE[0] and 0 <= y < MAP_SIZE[1]]
            surround = [(x, y) for (x, y) in surround if road_system[x]
                        [y] != 'X' and road_system[x]
                        [y] != 'S']
            if surround != []:
                for prefect in H_R.listWalker["Prefect"]:
                    if not prefect.missionaire:
                        prefect.missionaire = onFire
                        prefect.returning = False
                        prefect.goal = random.choice(surround)
                        prefect.path_finding(road_system)
                        prefect.path_index = 0
        for prefect in H_R.listWalker["Prefect"]:
            if prefect.missionaire != None:
                if prefect.missionaire not in world.listonFire:
                    if road_system[prefect.pos[0]][prefect.pos[1]] != True and not prefect.returning:
                        road = self.find_road_in_map(road_system)
                        if not road:
                            prefect.goal = (20, 0)
                        else:
                            prefect.goal = min(road, key=lambda point: manhattan_distance(
                                point, prefect.headquarter.grid))
                        prefect.path_finding(road_system)
                        prefect.path_index = 0
                        prefect.returning = True
                    prefect.missionaire = None
            elif road_system[prefect.pos[0]][prefect.pos[1]] != True and prefect.returning == False:
                road = self.find_road_in_map(road_system)
                if not road:
                    prefect.goal = (20, 0)
                else:
                    prefect.goal = min(road, key=lambda point: manhattan_distance(
                        point, prefect.headquarter.grid))
                prefect.path_finding(road_system)
                prefect.path_index = 0
                prefect.returning = True
            arrived = self.walker_move(prefect, world)
            if arrived:
                if prefect.missionaire != None:
                    prefect.sprite = prefect.sprite_list["action"][round(
                        prefect.missionaire.time_under_effect) % 3]
                    prefect.missionaire.time_under_effect += BURNING_TIME*0.005 * self.game_speed
                if prefect.missionaire == None:
                    prefect.returning = False

    def find_road_in_map(self, road_system):
        pile = []
        for x in range(MAP_SIZE[0]):
            for y in range(MAP_SIZE[1]):
                if road_system[x][y] == True:
                    pile.append((x, y))
        return pile

    def water_affection(self, world):
        for water in world.listBuilding:

            if type(water) == Water_well:
                x, y = water.grid
                surrounding = [(x-2, y-2), (x-2, y-1), (x-2, y), (x-2, y+1), (x-2, y+2), (x-1, y-2), (x-1, y-1), (x-1, y), (x-1, y+1), (x-1, y+2), (x, y-2), (x, y-1),
                               (x, y+1), (x, y+2), (x+1, y-2), (x+1, y-1), (x+1, y), (x+1, y+1), (x+1, y+2), (x+2, y-2), (x+2, y-1), (x+2, y), (x+2, y+1), (x+2, y+2)]
                surrounding = [(x, y) for (x, y) in surrounding if 0 <=
                               x < MAP_SIZE[0] and 0 <= y < MAP_SIZE[1] and (type(world.Building[x][y]) == Tent or type(world.Building[x][y]) == Tent_niv_2)]

                for a in surrounding:
                    x, y = a
                    # if type(world.Building[x][y]) == Tent or type(world.Building[x][y]) == Tent_niv_2:
                    if world.Building[x][y].water_source == None:
                        world.Building[x][y].water_source = water
                        water.distribute.append(world.Building[x][y])

    def house_evolution_devolution(self, world):
        for building in world.listBuilding:
            if type(building) == Tent:
                if building.water_source != None:
                    building._evoluer(world)
            if type(building) == Tent_niv_2:
                if building.water_source == None:
                    building._devoluer(world)

    def update(self, world, H_R, road_system, offset):
        # print(world.listBuilding)
        # print(H_R.pop)
        self.calendar_update()
        self.employing_prefect(world, H_R)
        self.water_affection(world)
        self.house_evolution_devolution(world)
        self.change_risk_fire(world)
        self.set_on_fire(world.listBuilding)
        self.change_building_timer(world.listonFire)
        self.done_burning(world.listonFire)
        self.vacane_slot(world, H_R, road_system, offset)
        self.Find_Fire(H_R, world, road_system)
        self.Patrol(H_R, road_system, world)
