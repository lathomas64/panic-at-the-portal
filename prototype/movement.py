from action import Action
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from character import Character


class Movement(Action):
    def __init__(self):
        super(Movement, self).__init__()
        self.name = "Movement"
        self.cost = "X"
    
    def available(self, pool=[], tokens={}) -> bool:
        if len(pool) > 0:
            return True 
        else:
            return False 
    
    def act(self, actor: 'Character', die:int):
        actor.add_tokens("speed", die)
    
    def __repr__(self):
        return "X: Gain X speed tokens"

class FreeMovement(Action):
    def __repr__(self) -> str:
        return "Speed Token: Free Movement"
    
    def available(self, pool=[], tokens={}) -> bool:
        if tokens["speed"] > 0:
            return True
        else:
            return False
    def act(self, actor: 'Character', position):
        print("Moving to:", position)
        actor.remove_tokens("speed", 1)