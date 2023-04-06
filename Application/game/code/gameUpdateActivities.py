"""
@author: yacin
"""
# Dans while game_Running:

# Ce code permet de retourner la l'attractivité et la
# prospérité en %
import numpy as np
import Building
import Walker
import sysv_ipc

KEY = 190234
PY_TO_C = 2

previousTypeMap = np.empty((40, 40), dtype=object)


class gameUpdate:
    ####################################### STEP 2###################################################
    # Si c'est la première fois que le jeu est en cours, previousTypeMap existe.
    # Si c'est le cas, il détecte les changement et vérifie si il y a des conflict avec conflict().

    # if previousTypeMap != TypeMap:
    #   if (conflict(TypeMap)):
    #       previousTypeMap = TypeMap
    #   else:
    #       TypeMap = previousTypeMap
    ###############################################################################################

    if CompteurFps % 60 == 0:

        # STEP 1 (temporaire): Envoi des changement sans problème de conflit
        if previousTypeMap != TypeMap:
            # envoie des informations par ipc
            message_queue = sysv_ipc.MessageQueue(KEY, sysv_ipc.IPC_CREAT)
            message_queue.send(TypeMap.encode(), type=PY_TO_C)

        # update les atributs des batiments
        for i in Buildings.building:
            i.fireRisk = fire_Risks(
                i.pos, getMinDistanceBetweenWolkersHome(i.pos, "Prefect"))
            i.collapseRisks = collapse_Risks(
                i.pos, getMinDistanceBetweenWolkersHome(i.pos, "Engineer"))
            i.criminalityRisks = criminality_Risks(
                i.pos, getMinDistanceBetweenHomes(i.pos, "Prefecture"))
            Attractivity = gameUpdate.attractivity(i.fireRisk, i.collapseRisks)
        Prosperity = gameUpdate.prosperity(Buildings.building)

    def attractivity(fireRisk, collapseRisks, criminalityRisks):
        return (1.5-((fireRisk+collapseRisks+criminalityRisks)/1.5))*100

    def prosperity(buildings):
        sumActractivities = 0
        for i in buildings:
            sumActractivities += gameUpdate.attractivity(
                i.risk_fire, i.risk_collapse, i.risk_criminality)
        return sumActractivities/len(buildings)

    # renvoie la position du walker le plus proche d'une tente
    def getMinDistanceBetweenWolkersHome(homePosition, typeWalker):
        listWolkers = Walkers.ListWalker[typeWalker]
        indexMin = 0
        for i in range(len(listWolkers)-1):
            if Manhanttan_Distance(homePosition, listWolkers[i+1].pos) < Distance(homePosition, listWolkers[i].pos):
                indexMin = i+1
        return listWolkers[idexMin].pos

    # renvoi le batiment le plus proche d'une tente
    def getMinDistanceBetweenHomes(homePosition, TypeLocation):
        listTypeLocation = []
        for i in Buildings.building:
            if i.type == TypeLocation:
                listTypeLocation.append(i)
        indexMin = 0
        for i in range(len(listTypeLocation)-1):
            if Distance(homePosition, listTypeLocation[i+1].pos) < Distance(homePosition, listTypeLocation[i].pos):
                indexMin = i+1
       # exp: p1 est de la forme p1={x,y]

        def Distance(p1, p2):
            return abs(p2[1]-p1[1])+abs(p2[2]-p1[2])

        return listTypeLocation[idexMin].pos


class Posix_Op:
    def __init__(self):
        self.message_queue = sysv_ipc.MessageQueue(KEY, sysv_ipc.IPC_CREAT)
        self.message = None

    def send_message(self, message):
        self.message_queue.send(message.encode(), type=PY_TO_C)
