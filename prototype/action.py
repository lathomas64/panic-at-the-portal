from ursina import Button, window, color, Tooltip
from grid import Hex 
from die import Die

class Action(Button):
    basic_actions = []
    def __init__(self, cost, name, description, available, act):
        super().__init__(scale=(.3,.1), x = window.top_left.x+.170, y=3, text=str(self))
        self.on_click = lambda : Hex.current_character.take_action(self)
        self.cost = cost
        self.name = name 
        self.description = description 
        self.available = available 
        self.act = act
        self.tooltip = Tooltip(self.description)
    
    def update(self):
        self.text = self.cost + ": " + self.name
        if self.available(Hex.current_character):
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
    
    @classmethod 
    def get_basic_actions(cls):
        if cls.basic_actions != []:
            return cls.basic_actions 
        move = Action("X", 
               "Movement", 
               "Gain X speed tokens", 
               lambda actor: actor.has_dice() and Die.selected != None,
               lambda actor, amount: actor.add_tokens("speed", amount))
        def unimplemented():
            raise NotImplementedError("This action not yet implemented")
        damage = Action("1+",
                        "Damage",
                        """
                        Deal 1 damage to one enemy in your range
                            3+: Deal 2 damage instead.
                            5+: Deal 3 damage instead, and push them 1 space away.
                            7+: Deal 4 damage instead, and push them 1 more space.
                            9+: Deal 5 damage instead, and push them 1 more space.
                        """,
                        lambda actor: actor.has_dice() and Die.selected != None,
                        lambda actor, die: unimplemented())
        #TODO once we have a turn queue this should go to the next player's turn
        end = Action("",
                     "End Turn",
                     "End your turn",
                     lambda actor: True,
                     lambda actor, die: actor.start_turn())
        cls.basic_actions = [move, damage, end]
        return cls.basic_actions