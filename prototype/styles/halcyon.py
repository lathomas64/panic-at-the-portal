'''
module for the halcyon style
'''
from prototype.styles.style import Style
from prototype.actions.purify import PurifyAction
from prototype.hud import UI
#from ursina import Func

class HalcyonStyle(Style):
    '''
    implementation of the Halcyon style 
    '''
    def __init__(self, character):
        super().__init__(character)
        self.range = 2
        self.actions = [PurifyAction(character)]

    def drop_token(self): # prompt to lose a token look at douse
        '''
        Make a prompt to discard a token
        '''
        token_list = [token_type for token_type in self.actor.tokens.keys()
                      if self.actor.get_tokens(token_type) > 0]
        UI.display_list("drop_token", token_list, self.actor.discard_tokens)

    def gain_iron(self):
        '''
        Method to add an iron token to the user
        used for the sake of register hooks being able to identify the function
        as opposed to just using Func
        '''
        self.actor.add_tokens("iron", 1)

    def on_equip(self):
        self.actor.register_hook("start_turn", self.drop_token)
        self.actor.register_hook("discard_token", self.gain_iron)

    def on_unequip(self):
        self.actor.unregister_hook("start_turn", self.drop_token)
        self.actor.unregister_hook("discard_token", self.gain_iron)
