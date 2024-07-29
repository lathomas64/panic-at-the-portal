from ursina import *

class Map(Entity):
    hexes = {}
    turns = []
    targeting = None
    current_character = None
    pan_speed = 5
    zoom_speed = 1
    max_zoom = .5
    min_zoom = .05
    instance = None
    def __init__(self, radius, **kwargs):
        super().__init__(parent=camera.ui,scale=.1, z=100,kwargs=kwargs)
        if radius != None:
            for q in range(-radius, radius+1):
                for r in range(-radius, radius+1):
                    if abs(q+r) <=radius:
                        hex = Hex(q,r, parent=self)
                        self[(q,r)] = hex
    
    def __setitem__(self, key, value):
        self.hexes[key] = value

    def __getitem__(self, key):
        return self.hexes[key]
    def __contains__(self, key):
        return key in self.hexes


    def input(self, key):
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
            self.scale = min(self.scale, self.max_zoom)
        if key == "scroll down":
            self.scale -= Vec3(self.zoom_speed * time.dt)
            self.scale = max(self.scale, self.min_zoom)
        if key == "escape":
            print(key, self.targeting, self.current_character)
            if self.targeting == None and self.current_character != None:
                self.current_character.get_actions()
                self.current_character.show_actions()
            else:
                self.targeting = None
    
    def advance_turn(self):
        if self.current_character != None: #skip this if we haven't done a turn yet
            self.turns.remove(self.current_character)
            self.turns.append(self.current_character)
        self.current_character = self.turns[0]
        self.current_character.start_turn()

    @classmethod
    def create_map(cls, radius=None):
        cls.instance = Map(radius)
        return cls.instance
    
    @classmethod
    def get_map(cls):
        return cls.instance


class Hex(Entity):
    map = None
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
        self.obstacle = None
        self.q = q
        self.r = r
        self.s = -1 * (q+r)
        scale = 1
        x_offset = (q + r/2) * scale
        y_offset = (r * .75) * scale
        super().__init__(parent=kwargs["parent"],scale=scale,x=x_offset, y=y_offset, model='quad',collider='box', texture=load_texture("hexbordered.png"), kwargs=kwargs)
        self.map = self.parent
        self.on_click = self.clicked
        self.tooltip = Tooltip(str((q,r))+"::"+str(abs(q+r))+"::"+str(max(abs(q),abs(r))))
        if random.random() < .3:
            self.addRubble()

    def addRubble(self):
        self.obstacle = "rubble"
        self.texture = load_texture("hexrubble.png")
        #self.move_cost = 2 #no move_cost is total calculated in distance
    
    def clearObstacles(self, radius):
        if self.obstacle == None: #exit early so we don't radiate out from hexes without obstacles
            return
        self.obstacle = None 
        self.texture = load_texture("hexbordered.png")
        if radius > 0:
            for neighbor in self.neighbors():
                neighbor.clearObstacles(radius-1)
    
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
        if self.map.current_character != None:
            self.move_cost = self.distance(self.map.current_character.parent)
            if self.map.current_character in self.children:
                self.texture = load_texture("hexcurrent.png")
            elif self.obstacle == "rubble":
                self.texture = load_texture("hexrubble.png")
            else:
                self.texture = load_texture("hexbordered.png")
        else:
            self.move_cost = -1
        if(self.hovered):
            self.color = Hex.hover_color
            if self.children != []:
                self.tooltip.text = str(self.children[0])
            elif self.map.current_character != None:
                self.tooltip.text = str(self.move_cost) + " speed tokens"
            self.tooltip.enabled = True
        elif self.map.targeting != None and "targets" in self.map.targeting and len(self.children) > 0 and self.children[0] in self.map.targeting["targets"]:
            self.color = color.green 
            self.tooltip.enabled = False
        elif self.map.targeting != None and self.distance(self.map.current_character.parent) <= self.map.targeting.get("range", self.map.current_character.range):
            self.color = color.red
            self.tooltip.enabled = False
        elif((self.map.current_character != None) 
           and self.move_cost > 0
           and self.move_cost <= self.map.current_character.get_tokens("speed")):
            self.color = color.blue
            self.tooltip.enabled = False
        else:
            self.color = Hex.base_color
            self.tooltip.enabled = False
    
    def clicked(self):
        if self.map.targeting != None:
            self.map.targeting["action"](self.map.targeting["actor"],self.map.targeting["die"], self)
            return
        print("clicked:",self.q,self.r)
        if(self.empty() and (self.map.current_character != None) and self.move_cost <= self.map.current_character.get_tokens("speed")):
            cost = self.distance(self.map.current_character.parent)
            self.map.current_character.parent = self
            self.map.current_character.spend_tokens("speed", cost)

if __name__ == "__main__":
    app = Ursina()
    my_map = Map.create_map(4)
    app.run()