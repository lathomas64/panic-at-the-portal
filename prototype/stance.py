'''
Stance is the form and style combination that a character can
switch between at the start of their turn.
'''
class Stance:
    '''
    Represents a single style form combination
    '''
    def __init__(self, style, form):
        self.style = style
        self.form = form
        self._actions = None
    def equip(self):
        '''
        setup when the actor switches into this stance
        '''
        self.style.on_equip()
        self.form.on_equip()
    def unequip(self):
        '''
        cleanup when the actor switches out of this stance
        '''
        self.style.on_unequip()
        self.form.on_unequip()

    @property
    def actions(self):
        '''
        Stance actions returns the actions of its style + the actions of its form
        '''
        if self._actions is None:
            self._actions = self.style.actions + self.form.actions
        return self._actions
