from Game import Game
from Scenes import Scene_PreMenu, Scene_menu, Scene_game, Scene_newgame, Scene_load, Scene_multi, Scene_multicreate, Scene_multijoin

if __name__ == '__main__':
    g = Game("")

    g.addScene(Scene_PreMenu.SCENE)
    g.addScene(Scene_menu.SCENE)
    g.addScene(Scene_newgame.SCENE)
    g.addScene(Scene_game.SCENE)
    g.addScene(Scene_load.SCENE)
    g.addScene(Scene_multi.SCENE)
    g.addScene(Scene_multijoin.SCENE)
    g.addScene(Scene_multicreate.SCENE)

    g.run()
