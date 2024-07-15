from ursina import Text, destroy, Entity, time

class FadingText(Entity):
    def __init__(self, text, parent, color, time=.5):
        super().__init__(parent=parent)
        self.text = Text(text, parent=self, scale=20,color=color, z=-5)
        destroy(self, delay=time)
    
    def update(self):
        self.y += 2 * time.dt