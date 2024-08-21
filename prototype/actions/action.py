from ursina import Button, window, color, Tooltip
from grid import Map
from die import Die

class Action(Button):
    basic_actions = []
    def __init__(self, cost, name, description, available = None, act = None):
        super().__init__(scale=(.3,.1), x = window.top_left.x+.170, y=3, text=str(self))
        self.cost = cost
        self.name = name 
        self.description = description 
        if available:
            self.available = available 
        if act:
            self.act = act
        self.tooltip = Tooltip(self.description)
        self.enabled = False
    
    def available(self,actor):
        return actor.has_dice() and Die.selected != None
    
    def update(self):
        self.text = self.cost + ": " + self.name
        if self.available(Map.get_map().current_character):
            #self.enabled = True 
            self.disabled = False
            self.on_click = self.on_click = lambda : self.act(Map.get_map().current_character, Die.selected)
            self.color = color.black
            pass
        else:
            #self.enabled = False
            self.disabled = True
            self.on_click = lambda : None
            self.color = color.gray
            pass