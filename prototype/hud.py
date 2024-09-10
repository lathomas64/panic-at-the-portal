from ursina import *
from grid import Map
from ursina.prefabs.splash_screen import SplashScreen

class Hud(Entity):
    instance = None
    def __init__(self):
        self.app=Ursina()
        super().__init__()
        self.overlay_active = False
        self.game_active = False
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
        if not self.game_active: # don't do any updates until the game is active
            return
        game_loss = True
        game_win = True
        for character in self.turns:
            if character.health > 0 and character.team == "player":
                game_loss = False 
            elif character.health > 0 and character.team != "player": # TODO win condition will be more complicated in future
                game_win = False
        if game_loss:
            self.game_active = False
            self.overlay("You lose!")
            return
        if game_win:
            self.game_active = False
            self.overlay("You win!")
            return

    def input(self, key):
        print(key)
        if self.overlay_active and key in ('space', 'gamepad a', 'escape', 'left mouse down'):
            self.clear_overlay()


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
        SplashScreen("game_over")
        self.overlay("")
    
    def game_win(self):
        print("***\n\nYou win!\n\n***")
        SplashScreen("you_win")
    
    def overlay(self, text):
        self.overlay_active = True
        camera.overlay.animate_color(color.black, duration=.1)
        self.overlay_message = Text(text, parent=camera.ui,world_z=camera.overlay.z-1)
        #invoke(self.clear_overlay, delay=3)

    def clear_overlay(self):
        camera.overlay.animate_color(color.clear, duration=.25)
        self.overlay_active = False
        destroy(self.overlay_message)

    @classmethod 
    def get_ui(cls):
        if cls.instance is None:
            cls.instance = Hud()
        return cls.instance

ui = Hud.get_ui()