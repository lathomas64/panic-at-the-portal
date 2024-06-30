from ursina import *

app = Ursina()

class Hex(Entity):
    map = {}
    current_character = None
    base_color = color.white 
    hover_color = color.gray
    directions = {
        "northeast":(0,1),
        "east" : (1,0),
        "southeast" : (1,-1),
        "northwest" : (-1,1),
        "west" : (-1,0),
        "southwest" : (0,-1)
    }

    def __init__(self, q,r, **kwargs):
        self.q = q
        self.r = r
        x_offset = q  + r/2
        y_offset = r * .75
        print(kwargs)
        super().__init__(x=x_offset, y=y_offset, model='quad',collider='box', texture=load_texture("hexbordered.png"), kwargs=kwargs)
        self.on_click = self.clicked
        self.tooltip = Tooltip(str((q,r))+"::"+str(abs(q+r))+"::"+str(max(abs(q),abs(r))))

    def distance(self, otherHex):
        q = self.q - otherHex.q
        r = self.r - otherHex.r
        return max([abs(q+r), abs(q), abs(r)])
    def update(self):
        if(self.hovered):
            self.color = Hex.hover_color
            self.tooltip.text = str(self.distance(Hex.current_character.parent)) + " speed tokens"
            self.tooltip.enabled = True
        else:
            self.color = Hex.base_color
            self.tooltip.enabled = False
        if(self.distance(Hex.current_character.parent) <= 2):
            self.color = color.green
    def clicked(self):
        print("clicked:",self.q,self.r)
        Hex.hover_color = color.random_color()
        Hex.current_character.parent = self
    @classmethod
    def create_map(cls, radius):
        cls.map = {}
        for q in range(-radius, radius+1):
            for r in range(-radius, radius+1):
                if abs(q+r) <=radius:
                    hex = Hex(q,r)
                    cls.map[(q,r)] = hex
        return cls.map

my_map = Hex.create_map(4)
player = SpriteSheetAnimation("placeholder_character.png", scale=.5, fps=4, z=-1, tileset_size=[4,4], animations={
    'idle' : ((0,3), (0,3)),        # makes an animation from (0,0) to (0,0), a single frame
    'walk_up' : ((0,0), (3,0)),     # makes an animation from (0,0) to (3,0), the bottom row
    'walk_right' : ((0,1), (3,1)),
    'walk_left' : ((0,2), (3,2)),
    'walk_down' : ((0,3), (3,3)),
    })

player.play_animation('walk_down')
player.parent = Hex.map[(0,0)]
Hex.current_character = player

app.run()