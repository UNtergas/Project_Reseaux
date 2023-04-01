import os
import pathlib
import pickle

from const import MAP_SIZE
from Building import *


class Save():
    def __init__(self, name):
        # NOTE : Carte temporaire
        self.map = Buildings()
        for x in range(MAP_SIZE[0]):
            self.map.Building.append([])
            for y in range(MAP_SIZE[1]):
                self.map.Building[x].append(Grass((x, y)))

        # ajout chemins
        X = 20
        for k in range(X):
            self.map.Building[k].remove(Grass((X, k)))
            self.map.Building[k].append(Chemins((X, k)))

        self.walkers = []
        self.pop = 0
        self.PO = 0
        self.date = 0
        self.desirability = 0
        self.religions = {}
        self.name = name
        self.size = 0

    def serialize(self):
        path = pathlib.PurePath(os.path.dirname(
            os.path.abspath(__file__)), "../saves")
        with open(pathlib.Path(path, f"{self.name}.save"), "wb") as f:
            pickle.dump(self, f)

    @staticmethod
    def deserialize(path: str) -> object:
        with open(path, "rb") as f:
            return pickle.load(f)

    @staticmethod
    def getSavesNames():
        path = pathlib.PurePath(os.path.dirname(
            os.path.abspath(__file__)), "../saves")

        return [
            fileName.split(".")[0]
            for fileName in os.listdir(path)
            if fileName.endswith(".save")]
