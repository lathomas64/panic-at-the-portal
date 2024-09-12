'''
Central hub of die rolls for panic
'''
from ursina import Entity, load_texture, camera, color, Text, random, window
#382b2b
class Die(Entity):
    '''
    A single die rolled for being used for actions
    may be a die or a static number
    '''
    left_margin = .1
    selected = None
    def __init__(self, size: str, static: bool = False):
        self.size = int(size.split("d").pop())
        self.static = static
        self.used = True
        super().__init__(model="quad",collider='box',
                         parent=camera.ui, scale=.075)
        self.text = Text(text="", parent=self, color=color.white, z=-1, scale=10)
        self.text.x = -1 * (self.text.scale.x * self.text.width) / 2
        self.on_click = self.clicked
        self.enabled = False
        self.visible = True
        self.texture=load_texture(size)
        self.value = None

    def update(self):
        '''
        Ursina entity update loop
        checks what texture we should have
        and if we should be visible
        '''
        if self.used:
            self.visible = False
            return
        self.visible = True
        if self.hovered or Die.selected == self:
            self.texture = load_texture("d"+str(self.size)+"_hover")
        else:
            self.texture = load_texture("d"+str(self.size))

    def consume(self):
        '''
        consume this die
        set it as used, unselected, and invisible
        also remove its value
        '''
        Die.selected = None
        self.used = True
        self.value = None
        self.text.text = "x"

    def roll(self):
        '''
        roll this die
        get a random value and
        consider it unused
        '''
        if self.static:
            self.value = self.size
        else:
            self.value = random.randint(1,self.size)
        self.used = False
        self.text.text = str(self.value)
        return self.value

    def clicked(self):
        '''
        operations to happen when a die is clicked
        '''
        Die.selected = self

    @classmethod
    def create_pool(cls, dice):
        '''
        given a list of sizes create a dice pool
        '''
        results = []
        index = 0
        for index, size in enumerate(dice):
            die = Die(size)
            die.x = window.top_left.x
            die.x += (.5 + Die.left_margin + index + Die.left_margin*index) * .075
            die.y = 6 * die.scale.y
            results.append(die)
        return results
