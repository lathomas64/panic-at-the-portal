class Stance:
    def __init__(self, actor, style, form):
        self.style = style 
        self.form = form
        self.actor = actor # TODO is this necessary?
    def equip(self):
        self.style.on_equip()
        self.form.on_equip()
    def unequip(self):
        self.style.on_unequip()
        self.form.on_unequip()
    
    @property
    def actions(self):
        if not hasattr(self, "_actions"):
            self._actions = self.style.actions + self.form.actions
        return self._actions