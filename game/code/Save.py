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
        self.spawnpoint = (20, 0)
        self.walkers = Walkers()
        self.pop = 0
        self.PO = 3000
        self.date = 0
        self.desirability = 0
        self.religions = {}
        self.name = name
        self.size = 0

    def print(self):
        map = []
        walker = []
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

        if self.walkers.listWalker['Prefect'] is not None:
            for prefect in self.walkers.listWalker['Prefect']:
                pos = prefect.pos
                walker.append(
                    {
                        'pos': pos
                    }
                )
        save = {
            "map": map,
            "walker": walker
        }
        with open("saves/save.json", "w") as savefile:
            json.dump(save, savefile)
