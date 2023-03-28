import os
import pathlib
import json

from const import MAP_SIZE
from Building import *
from Walker import *


class Save():
    def __init__(self, name):
        # NOTE : Carte temporaire
        self.map = Buildings()
        self.init()
        # self.load()
        self.spawnpoint = (20, 0)
        self.walkers = Walkers()
        self.pop = 0
        self.PO = 3000
        self.date = 0
        self.desirability = 0
        self.religions = {}
        self.name = name
        self.size = 0

    def init(self):
        for x in range(MAP_SIZE[0]):
            self.map.Building.append([])
            for y in range(MAP_SIZE[1]):
                self.map.Building[x].append(Grass((x, y)))
        self.map.Building[20] = [Chemins((20, x))for x in range(40)]

    def load(self, file):
        with open("saves/" + file + ".json", "r") as loadfile:
            load = json.load(loadfile)
        map = load["map"]
        Prefects = load["Prefect"]
        Immigrants = load["Immigrant"]
        for x in range(MAP_SIZE[0]):
            for y in range(MAP_SIZE[1]):
                temp_build = map[x*MAP_SIZE[0] + y]
                name = temp_build['name']
                self.map.Building[x][y] = type_of_tile((x, y), name)
                self.map.Building[x][y].risk = temp_build['risk']
                if temp_build['time_under_effect'] != 0:
                    self.map.Building[x][y].onFire = True
                self.map.Building[x][y].time_under_effect = temp_build['time_under_effect']
                if name == "Tent":
                    citizen = Citizen((x, y))
                    citizen.my_house = self.map.Building[x][y]
                    self.walkers.listWalker["Citizen"].append(citizen)
                    self.map.Building[x][y].habitant = citizen
        for pft in Prefects:
            pos = pft['pos']
            prefect = Prefect(pos)
            prefect.goal = pft['goal']
            if pft['missionaire'] != "":
                prefect.missionaire = self.map.Building[pft['missionaire']
                                                        [0]][pft['missionaire'][1]]
            prefect.headquarter = self.map.Building[pos[0]][pos[1]]
            self.walkers.listWalker["Prefect"].append(prefect)
        for img in Immigrants:
            pos = img['pos']
            goal = img['goal']
            immigrant = Walker(pos)
            immigrant.goal = goal
            immigrant.my_house = self.map.Building[goal[0]][goal[1]]
            immigrant.path = img['path']
            self.walkers.listWalker["Immigrant"].append(immigrant)

    def save(self):
        map = []
        prefect = []
        immigrant = []
        for x in range(MAP_SIZE[0]):
            for y in range(MAP_SIZE[1]):
                name = self.map.Building[x][y].name
                risk_fire = self.map.Building[x][y].risk_fire
                time_under_effect = self.map.Building[x][y].time_under_effect
                map.append(
                    {
                        'name': name,
                        "risk": risk_fire,
                        "time_under_effect": time_under_effect
                    }
                )

        if self.walkers.listWalker is not None:
            for pft in self.walkers.listWalker['Prefect']:
                prefect.append(
                    {
                        'pos': pft.pos,
                        'goal': pft.goal,
                        'missionaire': "" if pft.missionaire is None else pft.missionaire.grid,
                        'headquarter': pft.headquarter.grid
                    }
                )
            for img in self.walkers.listWalker['Immigrant']:
                immigrant.append(
                    {
                        "pos": img.pos,
                        "path": img.path,
                        "goal": img.goal,
                    }
                )
        save = {
            "name": self.name,
            "map": map,
            "Prefect": prefect,
            "Immigrant": immigrant,
            "PO": self.PO
        }
        with open("saves/save.json", "w") as savefile:
            json.dump(save, savefile)

    def getSavesNames():
        return ["chicken", "moscow", "save"]
