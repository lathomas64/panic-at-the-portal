'''
Handles individual Hexes and 
The whole Map of them too
'''
from ursina import Entity, camera, time, random, load_texture, Vec3, color, Tooltip

class Map(Entity):
    '''
    The grid of hexagons forming the board for this game
    '''
    targeting = None
    current_character = None
    pan_speed = 5
    zoom_speed = 1
    max_zoom = .5
    min_zoom = .05
    current_map = None
    def __init__(self, radius, **kwargs):
        super().__init__(parent=camera.ui,z=100,kwargs=kwargs)
        self.x = 0
        self.y = 0
        self.scale = .1
        self.hexes = {}
        self.turns = []
        if radius is not None:
            for q in range(-radius, radius+1):
                for r in range(-radius, radius+1):
                    if abs(q+r) <=radius:
                        self.add(q,r)

    def __setitem__(self, key, value):
        self.hexes[key] = value

    def __getitem__(self, key):
        return self.hexes[key]
    def __contains__(self, key):
        return key in self.hexes

    def add(self, q, r):
        '''
        create a hex and add it to the map at the given coordinates
        '''
        hex_space = Hex(q,r,parent=self)
        hex_space.move_cost = -1
        self[(q,r)] = hex_space

    def explore(self):
        '''
        explore hexes around the current character
        '''
        current_hex = self.current_character.parent
        for value in current_hex.directions.values():
            q = current_hex.q + value[0]
            r = current_hex.r + value[1]
            self.explore_hex(q,r)
        current_hex.flood_move_cost()

    def explore_hex(self, q,r):
        '''
        if there is no hex at the given coordinates
        create one and add it to the map
        '''
        if (q,r) not in self:
            self.add(q,r)
            self[q,r].rotation = (90,90,90)

    def input(self, key):
        '''
        standard ursina input
        scroll the map, zoom, or cancel targeting
        '''
        if key in ("a","a hold"):
            self.x += self.pan_speed * time.dt
        elif key in ("d","d hold"):
            self.x -= self.pan_speed * time.dt
        elif key in ("w","w hold"):
            self.y -= self.pan_speed * time.dt
        elif key in ("s","s hold"):
            self.y += self.pan_speed * time.dt
        elif key == "scroll up":
            self.scale += Vec3(self.zoom_speed * time.dt)
            self.scale = min(self.scale, self.max_zoom)
        elif key == "scroll down":
            self.scale -= Vec3(self.zoom_speed * time.dt)
            self.scale = max(self.scale, self.min_zoom)
        elif key == "escape":
            print(key, self.targeting, self.current_character)
            if self.targeting is None and self.current_character is not None:
                self.current_character.get_actions()
                self.current_character.show_actions()
            else:
                self.targeting = None

    def advance_turn(self):
        '''
        handle moving to the next turn in turn order
        '''
        self.targeting = None #stop gap end any targeting we were trying to do
        if self.current_character is not None: #skip this if we haven't done a turn yet
            self.turns.remove(self.current_character)
            self.turns.append(self.current_character)
        self.current_character = self.turns[0]
        self.current_character.start_turn()

    @classmethod
    def create_map(cls, radius=None):
        '''
        class method to create a new map
        0,0 will be the center and it will extend
        out radius hexes in each direction
        '''
        return Map(radius)


class Hex(Entity):
    '''
    a single space in our map
    '''
    map = None
    base_color = color.white
    hover_color = color.gray
    move_cost = -1

    def __init__(self, q,r, **kwargs):
        self.obstacle = None
        self.q = q
        self.r = r
        self.s = -1 * (q+r)
        scale = 1
        x_offset = (q + r/2) * scale
        y_offset = (r * .75) * scale
        self.directions = {
        "northeast":(0,1),
        "east" : (1,0),
        "southeast" : (1,-1),
        "northwest" : (-1,1),
        "west" : (-1,0),
        "southwest" : (0,-1)
        }
        super().__init__(scale=scale,x=x_offset, y=y_offset, model='quad',collider='box', **kwargs)
        self.texture = load_texture("hexbordered.png")
        self.map = self.parent
        self.on_click = self.clicked
        self.tooltip = Tooltip(str((q,r))+"::"+str(abs(q+r))+"::"+str(max(abs(q),abs(r))))
        self.color = color.white
        if random.random() < .3:
            #self.addRubble()
            self.add_obstacle(random.choice(["rubble", "edge", "wall", "fog"]))

    def add_obstacle(self, obstacle_type):
        '''
        add an obstacle of the given type to this hex
        handles updating its texture
        '''
        self.obstacle = obstacle_type
        self.texture = load_texture(f"hex{obstacle_type}.png")

    def clear_obstacles(self, radius):
        '''
        clear obstacles from this hex
        and surrounding ones out to a radius
        does not radiate from hexes with no obstacle
        '''
        if self.obstacle is None: #exit early so we don't radiate out from hexes without obstacles
            return
        self.obstacle = None
        self.texture = load_texture("hexbordered.png")
        if radius > 0:
            for neighbor in self.neighbors():
                neighbor.clearObstacles(radius-1)

    def empty(self):
        '''
        Are there any characters on this hex?
        '''
        return len(self.children) == 0

    def distance(self, other_hex):
        '''
        calculate distance between 2 hexes
        as the crow flies
        this method does not account for path or terrain
        '''
        q = self.q - other_hex.q
        r = self.r - other_hex.r
        return max([abs(q+r), abs(q), abs(r)])

    def neighbors(self):
        '''
        get a list of the hexes boarding this hex
        '''
        neighbor_coords = [(self.q + d[0], self.r + d[1]) for d in self.directions.values()]
        return [self.map[(q, r)] for q, r in neighbor_coords if (q, r) in self.map]

    def update(self):
        '''
        standard Ursina entity loop
        makes sure we have the right texture
        tooltip and color
        blue if we can be moved to
        red if we can be targeted
        green if we are being targeted
        white otherwise
        '''
        if self.rotation != (0,0,0):
            self.rotation -= (10,10,10)
            return
        if self.map.current_character is not None:
            #self.move_cost = self.distance(self.map.current_character.parent)
            if self.map.current_character in self.children:
                self.texture = load_texture("hexcurrent.png")
            elif self.obstacle is not None:
                self.texture = load_texture(f"hex{self.obstacle}.png")
            else:
                self.texture = load_texture("hexbordered.png")
        else:
            self.move_cost = -1
        if self.hovered:
            self.color = Hex.hover_color
            if self.children != []:
                self.tooltip.text = str(self.children[0])
            elif self.map.current_character is not None and self.move_cost != -1:
                self.tooltip.text = str(self.move_cost) + " speed tokens"
            else:
                self.tooltip.text = "unreachable"
            self.tooltip.enabled = True
        elif (self.map.targeting is not None
              and "targets" in self.map.targeting
              and len(self.children) > 0
              and self.children[0] in self.map.targeting["targets"]):
            self.color = color.green
            self.tooltip.enabled = False
        elif (self.map.targeting is not None
        and self.distance(self.map.current_character.parent)
        <= self.map.targeting.get("range", self.map.current_character.range)):
            self.color = color.red
            self.tooltip.enabled = False
        elif((self.map.current_character is not None)
           and self.move_cost > 0
           and self.move_cost <= self.map.current_character.get_tokens("speed")):
            self.color = color.blue
            self.tooltip.enabled = False
        else:
            self.color = Hex.base_color
            self.tooltip.enabled = False

    def clicked(self):
        '''
        process what should happen when a hex is clicked
        '''
        print(self.children)
        if self.map.targeting is not None:
            self.map.targeting["action"](self.map.targeting["actor"],
                                         self.map.targeting["die"],
                                         self)
            return
        if self.move_cost == -1:
            return
        print("clicked:",self.q,self.r)
        if(self.empty()
           and (self.map.current_character is not None)
           and self.move_cost <= self.map.current_character.get_tokens("speed")):
            self.map.current_character.parent = self
            self.map.current_character.spend_tokens("speed", self.move_cost)
            for hex_space in self.map.hexes.values():
                hex_space.move_cost = -1
            self.move_cost = 0
            self.flood_move_cost()

    def passable(self):
        '''
        is it possible to pass through this hex
        '''
        if not self.empty():
            return False
        if self.obstacle == "wall":
            return False
        return True

    def flood_move_cost(self):
        '''
        recursively figure out distance to hex and neighbors.
        '''
        blank_neighbors = [neighbor for neighbor in self.neighbors()
                           if neighbor.move_cost == -1 and neighbor.passable()]
        if len(blank_neighbors) == 0:
            return
        for neighbor in self.neighbors():
            if neighbor.move_cost == -1:
                neighbor.flood_move_cost_helper(self.move_cost)
        for neighbor in blank_neighbors:
            neighbor.flood_move_cost()

    def flood_move_cost_helper(self, previous_cost):
        '''
        figure out the length of the shortest path to this hex
        '''
        path_costs = [neighbor.move_cost for neighbor in self.neighbors()
                      if neighbor.move_cost != -1 and neighbor.passable()]
        path_cost = previous_cost
        if len(path_costs) >= 0:
            path_cost = min(path_costs+[previous_cost])

        if self.obstacle == "rubble":
            self.move_cost = path_cost + 2
        else:
            self.move_cost = path_cost +1
