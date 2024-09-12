'''
base module for all actions
'''
import abc
from ursina import Button, window, color, Tooltip
from prototype.die import Die
from prototype.actions.actor import Actor
from prototype.grid import Hex
from prototype.hud import UI


class Action(Button):
    '''
    Superclass for actions
    '''
    basic_actions = []
    def __init__(self, cost: str, name: str, description: str, actor: Actor,
                 action_range: int=None):
        super().__init__(scale=(.3,.1), x = window.top_left.x+.170, y=3)
        self.cost = cost
        self.name = name
        self.text = self.cost + ": " + self.name
        self.description = description
        self.tooltip = Tooltip(self.description)
        self.actor = actor
        self.range = action_range if action_range is not None else actor.range
        self.on_click = self.clicked
        self.parse_min_die()

    def parse_min_die(self):
        '''
        evaluate from cost what the smallest die value
        we can use for this action is
        '''
        try:
            self.min_die = int(self.cost.split("+")[0])
        except ValueError: #only case so far for this is X
            self.min_die = 1

    @abc.abstractmethod
    def confirm_targets(self, actor: Actor, die: Die, target_hex: Hex):
        '''
        implement this to specify what should happen after a target is chosen
        for this action
        '''
        raise NotImplementedError("Need to specify what to do after we have targets")

    def act(self, die: Die):
        '''
        What to do when this action is chosen
        default is to move to selecting a target
        '''
        UI.game_map.targeting = {"actor":self.actor,
                                 "action":self.confirm_targets,
                                 "die":die, "range":self.range,
                                 "targets":[]}

    def is_available(self) -> bool:
        '''
        how we determine if this action is, well actionable
        '''
        return (self.actor.has_dice()
                and Die.selected is not None
                and Die.selected.value >= self.min_die)

    def action_finished(self, die):
        '''
        cleanup function for after an action is complete
        '''
        UI.game_map.targeting = None
        die.consume()

    def clicked(self):
        '''
        what fires when an action is clicked
        '''
        if self.is_available():
            self.act(Die.selected)

    def update(self):
        '''
        Ursina update loop, 
        switch visual state if we are available
        and its our actor's turn
        '''
        if self.is_available() and self.actor.is_active_turn():
            #self.enabled = True
            self.disabled = False
            self.color = color.black
        else:
            #self.enabled = False
            self.disabled = True
            self.color = color.gray
