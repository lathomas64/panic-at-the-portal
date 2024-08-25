from ursina import *
from grid import Map


class Hud(Entity):
    instance = None
    def __init__(self):
        self.app=Ursina()
        self.current_map = Map.create_map(5)
        self.maps = {}
        self.maps["world"] = self.current_map
    
    @property
    def map(self):
        return self.current_map
    
    @map.setter
    def set_map(self, map):
        self.current_map = map

    def run(self):
        self.app.run()
    @classmethod 
    def get_ui(cls):
        if cls.instance is None:
            cls.instance = Hud()
        ui = cls.instance
        return cls.instance

ui = Hud.get_ui()