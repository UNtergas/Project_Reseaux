"""
@author: yacin
"""
# Dans while game_Running:
    
# Ce code permet de retourner la l'attractivité et la 
#prospérité en %

import BuildingBrouillon
import Walker


class gameUpdate:
    if CompteurFps%60==0:
        #update les atributs des batiments
        for i in Buildings.building:
            i.fireRisk=fire_Risks(i.pos,getMinDistanceBetweenWolkersHome(i.pos,"Prefect"))
            i.collapseRisks=collapse_Risks(i.pos,getMinDistanceBetweenWolkersHome(i.pos,"Engineer"))
            i.criminalityRisks=criminality_Risks(i.pos,getMinDistanceBetweenHomes(i.pos,"Prefecture"))
            Attractivity=gameUpdate.attractivity(i.fireRisk, i.collapseRisks)     
        Prosperity=gameUpdate.prosperity(Buildings.building)
        
    def attractivity(fireRisk,collapseRisks,criminalityRisks):
        return (1.5-((fireRisk+collapseRisks+criminalityRisks)/1.5))*100
    
    def prosperity(buildings): 
        sumActractivities=0
        for i in buildings:
            sumActractivities+=gameUpdate.attractivity(i.risk_fire,i.risk_collapse,i.risk_criminality)
        return sumActractivities/len(buildings)

    def getMinDistanceBetweenWolkersHome(homePosition,typeWalker):#renvoie la position du walker le plus proche d'une tente
        listWolkers=Walkers.ListWalker[typeWalker]
        indexMin=0
        for i in range(len(listWolkers)-1): 
            if Manhanttan_Distance(homePosition,listWolkers[i+1].pos)<Distance(homePosition,listWolkers[i].pos):
                indexMin=i+1
        return listWolkers[idexMin].pos
            
    def getMinDistanceBetweenHomes(homePosition,TypeLocation):#renvoi le batiment le plus proche d'une tente
        listTypeLocation=[]
        for i in Buildings.building:
            if i.type==TypeLocation:
               listTypeLocation.append(i)
        indexMin=0
        for i in range(len(listTypeLocation)-1): 
            if Distance(homePosition,listTypeLocation[i+1].pos)<Distance(homePosition,listTypeLocation[i].pos):
                indexMin=i+1
       ### exp: p1 est de la forme p1={x,y]
       def Distance(p1,p2):
           return abs(p2[1]-p1[1])+abs(p2[2]-p1[2])
        
       return listTypeLocation[idexMin].pos
    
    
            