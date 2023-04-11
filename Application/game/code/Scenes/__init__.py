class Scene:
    def __init__(self, scene_id, scene_name, createFunc=None, runFunc=None, handleEventsFunc=None):
        self.scene_id = scene_id
        self.scene_name = scene_name
        self.createFunc = createFunc
        self.runFunc = runFunc
        self.handleEventsFunc = handleEventsFunc
        self.children = [] # Créer une liste vide d'enfants

    def add_child(self, child):
        self.children.append(child)
