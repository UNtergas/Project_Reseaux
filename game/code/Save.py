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
        for x in range(MAP_SIZE[0]):
            self.map.Building.append([])
            for y in range(MAP_SIZE[1]):
                self.map.Building[x].append(Grass((x, y)))
        self.map.Building[20] = [Chemins((20, x))for x in range(40)]
        self.load()
        self.spawnpoint = (20, 0)
        self.walkers = Walkers()
        self.pop = 0
        self.PO = 3000
        self.date = 0
        self.desirability = 0
        self.religions = {}
        self.name = name
        self.size = 0

    def load(self):
        with open("saves/save.json", "r") as loadfile:
            load = json.load(loadfile)
        map = load["map"]
        # walkers = load["walker"]
        for x in range(MAP_SIZE[0]):
            for y in range(MAP_SIZE[1]):
                temp_build = map[x*MAP_SIZE[0] + y]
                name = temp_build['name']
                self.map.Building[x][y] = type_of_tile((x, y), name)
                self.map.Building[x][y].risk = temp_build['risk']
                if temp_build['time_under_effect'] != 0:
                    self.map.Building[x][y].onFire = True
                self.map.Building[x][y].time_under_effect = temp_build['time_under_effect']

    def print(self):
        map = []
        citizen = []
        prefect = []
        imigrant = []
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
            for ctz in self.walkers.listWalker['Citizen']:
                citizen.append(ctz.path)
            for pft in self.walkers.listWalker['Prefect']:
                prefect.append(
                    {
                        'pos': pft.pos,
                        'path': pft.path,
                        'goal': pft.goal,
                        'missionaire': pft.missionaire.grid,
                        'headquarter': pft.headquarter.grid
                    }
                )
            for img in self.walkers.listWalker['Immigrant']:
                print(img.__dict__)
        save = {
            "name": self.name,
            "map": map,
            "walker": prefect,
            "PO": self.PO
        }
        with open("saves/save.json", "w") as savefile:
            json.dump(save, savefile)
