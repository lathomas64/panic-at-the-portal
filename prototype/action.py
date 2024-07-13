from ursina import Button, window, color
from grid import Hex 
from die import Die

class Action(Button):
    basic_actions = []
    def __init__(self, cost, name, description, available, act):
        super().__init__(scale=(.3,.1), x = window.top_left.x+.170, y=.3, text=str(self))
        self.on_click = lambda : Hex.current_character.take_action(self)
        self.cost = cost
        self.name = name 
        self.description = description 
        self.available = available 
        self.act = act

    def available(self, pool=[], tokens={}) -> bool:
        print("action available called.")
        return False
    def act(self, actor, die):
        raise NotImplemented
    
    def update(self):
        self.text = self.cost + ": " + self.name
        if (Die.selected != None) and self.available(Hex.current_character):
            #self.enabled = True 
            self.disabled = False
            self.on_click = self.on_click = lambda : Hex.current_character.take_action(self)
            self.color = color.black
            pass
        else:
            #self.enabled = False
            self.disabled = True
            self.on_click = None
            self.color = color.gray
            pass
    
    def __repr__(self):
        return "Generic action - no one should see this"
    
    @classmethod 
    def get_basic_actions(cls):
        if cls.basic_actions != []:
            return cls.basic_actions 
        move = Action("X", 
               "Movement", 
               "Gain X speed tokens", 
               lambda actor: actor.has_dice(),
               lambda actor, amount: actor.add_tokens("speed", amount))
        cls.basic_actions = [move]
        return cls.basic_actions