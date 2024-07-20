from ursina import *

class Map(Entity):
    hexes = {}
    pan_speed = 5
    zoom_speed = 1
    def __init__(self, **kwargs):
        super().__init__(parent=camera.ui,scale=.1, z=100,kwargs=kwargs)
    
    def __setitem__(self, key, value):
        self.hexes[key] = value

    def __getitem__(self, key):
        return self.hexes[key]
    def __contains__(self, key):
        return key in self.hexes


    def input(self, key):
        print(key)
        print(self.x,self.y,self.scale)
        if key == "a" or key == "a hold":
            self.x += self.pan_speed * time.dt
        if key == "d" or key == "d hold":
            self.x -= self.pan_speed * time.dt
        if key == "w" or key == "w hold":
            self.y -= self.pan_speed * time.dt
        if key == "s" or key == "s hold":
            self.y += self.pan_speed * time.dt
        if key == "scroll up":
            self.scale += Vec3(self.zoom_speed * time.dt)
        if key == "scroll down":
            self.scale -= Vec3(self.zoom_speed * time.dt)

class Hex(Entity):
    map = None
    targeting = None
    current_character = None
    turns = []
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
        scale = 1
        x_offset = (q + r/2) * scale
        y_offset = (r * .75) * scale
        super().__init__(parent=Hex.map,scale=scale,x=x_offset, y=y_offset, model='quad',collider='box', texture=load_texture("hexbordered.png"), kwargs=kwargs)
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
            if self.children != []:
                self.tooltip.text = str(self.children[0])
            elif Hex.current_character != None:
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
        cls.map = Map(parent=camera.ui)
        for q in range(-radius, radius+1):
            for r in range(-radius, radius+1):
                if abs(q+r) <=radius:
                    hex = Hex(q,r)
                    cls.map[(q,r)] = hex
        return cls.map
    
    @classmethod
    def advance_turn(cls):
        if cls.current_character != None: #skip this if we haven't done a turn yet
            cls.turns.remove(cls.current_character)
            cls.turns.append(cls.current_character)
        cls.current_character = cls.turns[0]
        cls.current_character.start_turn()



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