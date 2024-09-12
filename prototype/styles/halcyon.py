from prototype.styles.style import Style 
from prototype.actions.purify import PurifyAction
from prototype.hud import UI
from ursina import Func

class HalcyonStyle(Style):
    def __init__(self, character):
        super().__init__(character)
        self.range = 2
    
    def drop_token(self): # prompt to lose a token look at douse
        token_list = [token_type for token_type in self.actor.tokens.keys() if self.actor.get_tokens(token_type) > 0]
        UI.display_list("drop_token", token_list, self.actor.discard_tokens)
    
    def gain_iron(self):
        self.actor.add_tokens("iron", 1) # gain an iron token 

    def on_equip(self):
        self.actor.register_hook("start_turn", self.drop_token)
        self.actor.register_hook("discard_token", self.gain_iron)
    
    def on_unequip(self):
        self.actor.unregister_hook("start_turn", self.drop_token)
        self.actor.unregister_hook("discard_token", self.gain_iron)
    
    @property
    def actions(self):
        if not hasattr(self, "_actions"):
            self._actions = [PurifyAction(self.actor)]
        return self._actions