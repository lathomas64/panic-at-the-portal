from ursina import Text, destroy, Entity, time, color

class FadingText(Entity):
    def __init__(self, text, parent, text_color, time=5):
        super().__init__(parent=parent)
        self.text = Text(text, parent=self, scale=20,color=text_color, z=-5)
        self.outline = Text(text, parent=self, scale=20,color=color.black, z=-4.9)
        destroy(self, delay=time)
    
    def update(self):
        self.y += 2 * time.dt