from prototype.forms.form import Form
from prototype.die import Die
from prototype.actions.amplify import AmplifyAction
from prototype.actions.shockwave import ShockwaveAction

class BlasterForm(Form):
    def __init__(self, character):
        super().__init__(character)
        self.action_pool = Die.create_pool(["d8", "d8", "d8"])
    
    def on_equip(self):
        pass # TODO how do we do the extra targets ability?

    def on_unequip(self):
        pass
    
    @property
    def actions(self):
        if not hasattr(self, "_actions"):
            self._actions = [AmplifyAction(self.actor), ShockwaveAction(self.actor)]