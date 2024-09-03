from ursina import *
from grid import Map


class Hud(Entity):
    instance = None
    def __init__(self):
        self.app=Ursina()
        self.current_map = Map.create_map(5)
        self.maps = {}
        self.maps["world"] = self.current_map
        self.action_dict = {}
        self.turns = []
        self.lists = {}
    
    def display_actions(self):
        self.action_list = ButtonList(self.action_dict,
                        font='VeraMono.ttf',
                        button_height=1.5,
                        popup=0,
                        clear_selected_on_enable=True)
    
    def update(self):
        print("does update in hud get called ever???")
        game_loss = True
        game_win = True
        for character in self.turns:
            if character.health > 0 and character.team == "player":
                game_loss = False 
            elif character.health > 0 and character.team != "player": # TODO win condition will be more complicated in future
                game_win = False
        if game_loss:
            self.game_over()
        if game_win:
            self.game_win()

    def input(self, key):
        print(key)


    @property
    def map(self):
        return self.current_map
    
    @map.setter
    def set_map(self, map):
        self.current_map = map

    def run(self):
        self.app.run()
    
    def run_then_destroy(self, func, entity):
        func()
        destroy(entity)
    
    def display_list(self, name, options, function=print):
        button_dict = {}
        self.lists[name] = ButtonList(button_dict, font='VeraMono.ttf', button_height=1.5, popup=0, clear_selected_on_enable=False)
        for option in options:
            button_dict[option] = Func(self.run_then_destroy, Func(function, option), self.lists[name])
        self.lists[name].button_dict = button_dict
    
    def game_over(self):
        print("***\n\nGame Over!\n\n***")
    
    def game_win(self):
        print("***\n\nYou win!\n\n***")
    
    @classmethod 
    def get_ui(cls):
        if cls.instance is None:
            cls.instance = Hud()
        return cls.instance

ui = Hud.get_ui()