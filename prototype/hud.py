'''
hud handles the UI for the game
'''
from ursina import Ursina, ButtonList, Entity, destroy, Func, camera, color, Text
from prototype.grid import Map


class Hud(Entity):
    '''
    class to collect all the hud elements
    '''
    instance = None
    def __init__(self):
        self.app=Ursina()
        super().__init__()
        self.overlay_active = False
        self.game_active = False
        self.current_map = Map.create_map(5)
        self.maps = {}
        self.maps["world"] = self.current_map
        self.turns = []
        self.lists = {}
        self.overlay_message = ""

    def update(self):
        '''
        standard update loop
        '''
        if not self.game_active: # don't do any updates until the game is active
            return
        game_loss = True
        game_win = True
        for character in self.turns:
            if character.health > 0 and character.team == "player":
                game_loss = False
            elif character.health > 0 and character.team != "player":
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
        '''
        handle game input.
        '''
        print(key)
        if self.overlay_active and key in ('space', 'gamepad a', 'escape', 'left mouse down'):
            self.clear_overlay()


    @property
    def game_map(self):
        '''
        reference to the map we are currently displaying on screen
        '''
        return self.current_map

    @game_map.setter
    def set_map(self, game_map):
        self.current_map = game_map

    def run(self):
        '''
        run the Ursina app associated with this hud object
        '''
        self.app.run()

    def run_then_destroy(self, func, entity):
        '''
        does what it says, call a function
        then destroy the entity passed in
        '''
        func()
        destroy(entity)

    def display_list(self, name, options, function=print):
        '''
        create and display a buttonlist of buttons that call a function 
        then destroy the list when an option is selected
        '''
        button_dict = {}
        self.lists[name] = ButtonList(button_dict,
                                      font='VeraMono.ttf',
                                      button_height=1.5,
                                      popup=0,
                                      clear_selected_on_enable=False)
        for option in options:
            button_dict[option] = Func(self.run_then_destroy,
                                       Func(function, option),
                                       self.lists[name])
        self.lists[name].button_dict = button_dict

    def overlay(self, text):
        '''
        create an overlay screen with the given text
        '''
        self.overlay_active = True
        camera.overlay.animate_color(color.black, duration=.1)
        self.overlay_message = Text(text, parent=camera.ui,world_z=camera.overlay.z-1)
        #invoke(self.clear_overlay, delay=3)

    def clear_overlay(self):
        '''
        removes a previously established overlay
        '''
        camera.overlay.animate_color(color.clear, duration=.25)
        self.overlay_active = False
        destroy(self.overlay_message)

    @classmethod
    def get_ui(cls):
        '''
        gets the hud instance
        '''
        if cls.instance is None:
            cls.instance = Hud()
        return cls.instance
try:
    UI = Hud.get_ui()
except Exception as e:
    print(f"could not get a hud: {e}")
