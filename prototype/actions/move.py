from actions.action import Action
from die import Die

class MoveAction(Action):
    def __init__(self):
        super().__init__("X", 
               "Movement", 
               "Gain X speed tokens")
    
    def available(self,actor):
        return actor.has_dice() and Die.selected != None

    def act(self,actor, die):
        actor.add_tokens("speed", die.value)
        die.consume()