from ursina import Button, window
from grid import Hex 

class Action(Button):
    def __init__(self):
        super().__init__(scale=(.3,.1), x = window.top_left.x+.170, y=.3, text=str(self))
        self.on_click = lambda : Hex.current_character.take_action(self)

    def available(self, pool=[], tokens={}) -> bool:
        return False
    def act(self, actor, die):
        raise NotImplemented
    
    def update(self):
        self.text = self.cost + ": " + self.name
    
    def __repr__(self):
        return "Generic action - no one should see this"