from ursina import *
#382b2b
class Die(Entity):
    left_margin = .1
    selected = None
    def __init__(self, size: str, static: bool = False):
        self.size = int(size.split("d").pop())
        self.static = static
        self.used = True
        super().__init__(model="quad",collider='box', texture=load_texture(size), parent=camera.ui, scale=.075)
        self.text = Text(text="", parent=self, color=color.white, z=-1, scale=10)
        self.text.x = -1 * (self.text.scale.x * self.text.width) / 2
        self.on_click = self.clicked
        self.enabled = False
    
    def update(self):
        if self.used:
            self.visible = False 
            return
        else:
            self.visible = True
        if self.hovered or Die.selected == self:
            self.texture = load_texture("d"+str(self.size)+"_hover")
        else:
            self.texture = load_texture("d"+str(self.size))
    
    def consume(self):
        Die.selected = None 
        self.used = True 
        self.value = None 
        self.text.text = "x"

    def roll(self):
        if(self.static):
            self.value = self.size
        else:
            self.value = random.randint(1,self.size)
        self.used = False
        self.text.text = str(self.value)
        return self.value

    def clicked(self):
        Die.selected = self
    
    @classmethod
    def create_pool(cls, dice):
        results = []
        index = 0
        for index in range(len(dice)):
            size = dice[index]
            die = Die(size)
            die.x = window.top_left.x + (.5 + Die.left_margin + index + Die.left_margin*index) * .075
            die.y = 6 * die.scale.y
            results.append(die)
        return results



if __name__ == "__main__":
    app = Ursina()

    left_margin = .1

    for index in range(4):
        die = Entity(model="quad", texture=load_texture("d4.png"), parent=camera.ui, scale=.075)
        die.x = window.top_left.x + (.5 + left_margin + index + left_margin*index) * .075
        die.y = 6 * die.scale.y
        die_value = Text(text="4", parent=die, color=color.white, z=-1, scale=10)
        die_value.x = -1 * (die_value.scale.x * die_value.width) / 2

    app.run()