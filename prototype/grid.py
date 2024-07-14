from ursina import *



class Hex(Entity):
    map = {}
    targeting = None
    current_character = None
    base_color = color.white 
    hover_color = color.gray
    move_cost = -1
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
        self.s = -1 * (q+r)
        scale = .125
        x_offset = (q + r/2) * scale
        y_offset = (r * .75) * scale
        super().__init__(parent=camera.ui,scale=scale,x=x_offset, y=y_offset, model='quad',collider='box', texture=load_texture("hexbordered.png"), kwargs=kwargs)
        self.on_click = self.clicked
        self.tooltip = Tooltip(str((q,r))+"::"+str(abs(q+r))+"::"+str(max(abs(q),abs(r))))

    def empty(self):
        return len(self.children) == 0

    def distance(self, otherHex):
        q = self.q - otherHex.q
        r = self.r - otherHex.r
        return max([abs(q+r), abs(q), abs(r)])
    
    def neighbors(self):
        result = []
        for q in range(self.q-1,self.q+2):
            for r in range(self.r-1,self.r+2):
                if (q,r) == (self.q,self.r):
                    continue # don't count myself as a neighbor
                if (q,r) in Hex.map and abs(q-self.q+r-self.r) <= 1:
                    result.append(Hex.map[(q,r)])
        return result
    
    def update(self):
        if Hex.current_character != None:
            self.move_cost = self.distance(Hex.current_character.parent)
        else:
            self.move_cost = -1
        if(self.hovered):
            self.color = Hex.hover_color
            if Hex.current_character != None:
                self.tooltip.text = str(self.move_cost) + " speed tokens"
            self.tooltip.enabled = True
        else:
            self.color = Hex.base_color
            self.tooltip.enabled = False
        if((Hex.current_character != None) 
           and self.move_cost > 0
           and self.move_cost <= Hex.current_character.get_tokens("speed")):
            self.color = color.green
    
    def clicked(self):
        if Hex.targeting != None:
            Hex.targeting["action"](Hex.targeting["actor"],Hex.targeting["die"], self)
            return
        print("clicked:",self.q,self.r)
        if(self.empty() and (Hex.current_character != None) and self.move_cost <= Hex.current_character.get_tokens("speed")):
            cost = self.distance(Hex.current_character.parent)
            Hex.current_character.parent = self
            Hex.current_character.spend_tokens("speed", cost)

    @classmethod
    def create_map(cls, radius):
        cls.map = {}
        for q in range(-radius, radius+1):
            for r in range(-radius, radius+1):
                if abs(q+r) <=radius:
                    hex = Hex(q,r)
                    cls.map[(q,r)] = hex
        return cls.map

if __name__ == "__main__":
    app = Ursina()
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