import pygame
SCREENSIZE = WIDTH, HEIGHT = 1200, 760


class Game():
    def __init__(self, save):
        pygame.init()
        # self.screen = pygame.display.set_mode(SCREENSIZE)
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

        self.screen_width, self.screen_height = self.screen.get_size()

        self.save = save

        self.actualScene = None
        self.running = True
        self.sceneMap = {}
        self.map = None
        self.tick = 0

    def addScene(self, scene) -> None:
        if scene.id in self.sceneMap.keys():
            raise Exception(
                f"The scene {self.sceneMap[scene.id]} already have id : {scene.id}")

        if self.actualScene == None:
            self.actualScene = scene.id

        self.sceneMap[scene.id] = scene

    def switchScene(self, sceneId):
        if sceneId not in self.sceneMap.keys():
            raise Exception(
                f"No Scene with id {sceneId}"
            )
        self.actualScene = sceneId

    def run(self):
        while self.running:

            # Verifie if the scene selected exist
            if self.actualScene not in self.sceneMap.keys():
                raise Exception(
                    f"Invalid Scene ID ({self.actualScene}) valid : [{self.sceneMap.keys()}]")

            # Change the scene to the selected scene
            scene = self.sceneMap[self.actualScene]

            # Initialise the scene
            scene.create(self)

            # Run the scene
            while self.running and self.actualScene == scene.id:

                scene.handleEvents()
                scene.run()
                self.tick += 1
            # End the scene
            scene.destroy()
            #
        pygame.display.quit()
        pygame.quit()
        exit()

    def end(self):
        self.running = False
