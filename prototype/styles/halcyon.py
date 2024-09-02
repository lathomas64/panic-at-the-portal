from styles.style import Style 
from actions.purify import Purify

class Halcyon(Style):
    def __init__(self, character):
        super().__init__(character)
        self.range = 2
    
    def on_equip(self):
        self.actor.register_hook("start_turn", self.drop_token)
        self.actor.register_hook("discard_token", self.gain_iron)
    
    def on_unequip(self):
        self.actor.unregister_hook("start_turn", self.drop_token)
        self.actor.unregister_hook("discard_token", self.gain_iron)
    
    @property
    def actions(self):
        if not hasattr(self, "_actions"):
            self._actions = [Purify(self.actor)]
        return self._actions