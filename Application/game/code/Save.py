import os
import pathlib
import json
from StackFunc import FunctionQueue
from const import MAP_SIZE
from Building import *
from Walker import *
from GameIO import IO
import socket
from StackFunc import FunctionQueue

class Save():
    def __init__(self, name, socket: socket.socket):
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
        self.road_system = [
            [False] * MAP_SIZE[0] for _ in range(MAP_SIZE[1])]

        self.IO = IO(socket=socket)
        self.function_queue= FunctionQueue()

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
        for temp_build in map:
            (x, y) = temp_build['pos']
            name = temp_build['name']
            self.map.Building[x][y] = type_of_tile((x, y), name)
            match name:
                case "Prefecture":
                    pass
                case "Tent":
                    citizen = Citizen((x, y))
                    citizen.my_house = self.map.Building[x][y]
                    self.walkers.listWalker["Citizen"].append(citizen)
                    self.map.Building[x][y].habitant = citizen
                    self.map.Building[x][y].risk_fire = temp_build['risk']
                    if temp_build['time_under_effect'] != 0:
                        self.map.Building[x][y].onFire = True
                        self.map.Building[x][y].time_under_effect = temp_build['time']
                case "Road":
                    self.road_system[x][y] = True
                case "House":
                    self.road_system[x][y] = 'X'
                case _:
                    self.road_system[x][y] = 'S'
        for pft in Prefects:
            pos = pft['pos']
            hqt = pft['headquarter']
            prefect = Prefect(pos)
            prefect.goal = pft['goal']
            if pft['missionaire'] != "":
                prefect.missionaire = self.map.Building[pft['missionaire']
                                                        [0]][pft['missionaire'][1]]
            prefect.headquarter = self.map.Building[hqt[0]][hqt[1]]
            self.map.Building[hqt[0]][hqt[1]].personnage = prefect
            self.walkers.listWalker["Prefect"].append(prefect)
        for img in Immigrants:
            pos = img['pos']
            goal = img['goal']
            immigrant = Walker(pos)
            immigrant.goal = goal
            immigrant.my_house = self.map.Building[goal[0]][goal[1]]
            self.map.Building[goal[0]][goal[1]].available = False
            immigrant.path_finding(self.road_system)
            immigrant.path_index = 0
            self.walkers.listWalker["Immigrant"].append(immigrant)

    def save(self):
        map = []
        prefect = []
        immigrant = []
        for x in range(MAP_SIZE[0]):
            for y in range(MAP_SIZE[1]):
                name = self.map.Building[x][y].name
                if name != "grass":
                    if name == "road":
                        map.append(
                            {
                                'pos': [x, y],
                                'name': 'road'
                            }
                        )
                    else:
                        risk_fire = self.map.Building[x][y].risk_fire
                        time_under_effect = self.map.Building[x][y].time_under_effect
                        map.append(
                            {
                                'pos': [x, y],
                                'name': name,
                                "risk": risk_fire,
                                "time": time_under_effect
                            }
                        )
        self.IO.ipc.sendToNetwork("!Done")

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
        self.IO.ipc.sendToNetwork('!Done')

    def getSavesNames():
        return ["chicken", "moscow", "save"]

    def getJsonInstance(self):
        map = []
        prefect = []
        immigrant = []
        for x in range(MAP_SIZE[0]):
            for y in range(MAP_SIZE[1]):
                name = self.map.Building[x][y].name
                if name != "grass":
                    if name == "road":
                        map.append(
                            {
                                'pos': [x, y],
                                'name': 'road'
                            }
                        )
                    else:
                        risk_fire = self.map.Building[x][y].risk_fire
                        time_under_effect = self.map.Building[x][y].time_under_effect
                        map.append(
                            {
                                'pos': [x, y],
                                'name': name,
                                "risk": risk_fire,
                                "time": time_under_effect
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
                        "goal": img.goal,
                    }
                )
                i += 1
        save = {
            "name": self.name,
            "map": map,
            "Prefect": prefect,
            "Immigrant": immigrant,
            "PO": self.PO
        }

        return json.dumps(save)
