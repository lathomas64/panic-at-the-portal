'''
module for temporary text messages displayed on the screen
'''
from ursina import Text, destroy, Entity, time, color

class FadingText(Entity):
    '''
    temporary text message in a space
    '''
    def __init__(self, text, parent, text_color, delay=5):
        super().__init__(parent=parent)
        self.y = 0
        self.text = Text(text, parent=self, scale=20,color=text_color, z=-5)
        self.outline = Text(text, parent=self, scale=20,color=color.black, z=-4.9)
        destroy(self, delay=delay)

    def update(self):
        '''
        ursina update loop, text floats up until its over
        '''
        self.y += 2 * time.dt
