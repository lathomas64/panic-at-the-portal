from actions.action import Action

class MoveAction(Action):
    def __init__(self):
        super().__init__("X", 
               "Movement", 
               "Gain X speed tokens")

    def act(self,actor, die):
        actor.add_tokens("speed", die.value)
        die.consume()