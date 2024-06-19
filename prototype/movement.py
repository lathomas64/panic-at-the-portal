from prototype.action import Action
from prototype.character import Character


class Movement(Action):
    def __init__(self):
        super(Movement, self).__init__()
    
    def available(self, pool=[], tokens={}) -> bool:
        if len(pool) > 0:
            return True 
        else:
            return False 
    
    def act(self, actor: , die:int):
        pass