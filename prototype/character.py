from action import Action
from die import Die
from grid import Map
from fadingText import FadingText
from ursina import SpriteSheetAnimation, window, color, time
#from ursina.prefabs.health_bar import HealthBar

class Character(SpriteSheetAnimation):
    # actions movement die in speed tokens out

    def __init__(self, sheet="placeholder_character.png", name="default"):
        self.range = 2
        self.action_pool = Die.create_pool(["d4", "d6", "d8", "d10"])
        self.tokens = {}
        self.actions = []
        self.max_health = 6
        self.health = self.max_health
        self.stance = None
        self.team = name
        self.default_animation = "walk_down"

        super().__init__(sheet, scale=.5, fps=4, z=-1, tileset_size=[4,4], animations={
        'idle' : ((0,3), (0,3)),        # makes an animation from (0,0) to (0,0), a single frame
        'walk_up' : ((0,0), (3,0)),     # makes an animation from (0,0) to (3,0), the bottom row
        'walk_right' : ((0,1), (3,1)),
        'walk_left' : ((0,2), (3,2)),
        'walk_down' : ((0,3), (3,3)),
        })
        self.name = name
        self.play_animation('walk_down')
        #self.health_bar = HealthBar(parent=self, x=.5,bar_color=color.lime.tint(-.25), roundness=.5, max_value=self.max_health, value=self.health)

    def take_damage(self, amount):
        self.health -= amount
        #self.health_bar.value = self.health
        FadingText(amount, self, color.red)
        if self.health <= 0:
            #self.parent = None
            #self.enabled = False
            self.color = color.gray
            self.health = 0
            self.play_animation("idle")
        print(self.health,"/",self.max_health)
    
    def heal(self, amount):
        self.health += amount
        self.play_animation(self.default_animation)
        self.color = color.white
        #self.health_bar.value = self.health
        FadingText(amount, self, color.green)
        print(self.health,"/",self.max_health)
    
    def push(self, target, amount):
        print("attempting to push ",target, " ", amount, " hexes")   
        for _ in range(min(amount,0), max(amount,0)):
            qdiff = target.parent.q - self.parent.q 
            rdiff = target.parent.r - self.parent.r
            if amount < 0:
                qdiff = qdiff * -1
                rdiff = rdiff * -1
            destination_q = target.parent.q
            destination_r = target.parent.r
            if (abs(qdiff) == abs(rdiff)) and (qdiff != rdiff):
                if qdiff > 0:
                    destination_q += 1
                else:
                    destination_q -= 1
                if rdiff > 0:
                    destination_r += 1
                else:
                    destination_r -= 1
            elif abs(qdiff) > abs(rdiff):
                #push q            
                if qdiff > 0:
                    destination_q += 1
                else:
                    destination_q -= 1 
            else:
                #push r
                if rdiff > 0:
                    destination_r += 1
                else:
                    destination_r -= 1
            if (destination_q, destination_r) in Map.get_map():
                target.parent = Map.get_map()[destination_q, destination_r]
            #should we have an else?
        #TODO handle ringout if their final destination is outside the map.

    def pull(self, target, amount):
        self.push(target, -1 * amount)

    def get_tokens(self, tokenType: str) -> int:
        if tokenType in self.tokens:
            return self.tokens[tokenType]
        else:
            return 0

    def add_tokens(self, tokenType: str, tokenAmount:int):
        FadingText("+"+str(tokenAmount) + " " + tokenType, self, color.green)
        if tokenType in self.tokens:
            self.tokens[tokenType] += tokenAmount 
        else:
            self.tokens[tokenType] = tokenAmount
    
    def spend_tokens(self, tokenType: str, tokenAmount:int):
        FadingText("-"+str(tokenAmount) + " " + tokenType, self, color.red)
        if tokenType not in self.tokens:
            return
        self.tokens[tokenType] -= tokenAmount
        if self.tokens[tokenType] < 0:
            self.tokens[tokenType] = 0
    
    def has_dice(self):
        for die in self.action_pool:
            if die.used == False:
                return True
        # no unused dice here
        return False

    def take_action(self, action: Action): #this only works for actions that take die
        if Die.selected:
            if action.act(self, Die.selected.value) != False:
                Die.selected.consume()
        else:
            action.act(self, None) #this will get more complicated later with token actions

    def get_actions(self):
        print("get actions...")
        for action in self.actions:
            action.enabled = False 
        #build out top level menu of actions
        self.actions = Action.get_basic_actions()
        if self.stance != None:
            self.actions += self.stance.get_actions()

    def set_actions(self, actions):
        for action in self.actions:
            action.enabled = False 
        self.actions = actions
        self.show_actions()

    def show_actions(self):
        for index in range(len(self.actions)):
            action = self.actions[index]
            # these will have to adjust based on index in future when there are multiple
            action.x = window.top_left.x+.17
            action.y = .3 - .1125 * index
            action.enabled = True

    def start_turn(self):
        # anything else at start of turn
        for die in self.action_pool:
            die.roll()
            die.enabled = True
        self.get_actions()
        self.show_actions()
        self.parent.move_cost = 0
        self.parent.flood_move_cost()
    
    def end_turn(self):
        self.tokens["speed"] = 0 # unless special conditions
        Die.selected = None
        for die in self.action_pool:
            die.enabled = False 
        for action in self.actions:
            action.enabled = False 
        Map.get_map().advance_turn()
    
    def __del__(self):
        print("character deleted...")
    def __str__(self):
        return self.name + "\n" + str(self.health) + "/" + str(self.max_health)


class AICharacter(Character):
    state = None
    wait_time = -1
    wait_function = None
    def idle(self):
        FadingText(self.name + " seems oblivious",self.parent, color.black, 1)
        self.wait_time = 1
        self.wait_function = self.end_turn
        #self.end_turn()
    
    def find_enemies(self):
        return [character for character in Map.get_map().turns if character.team == None or character.team != self.team]
    
    def start_turn(self):
        print("AICharacter start turn...")
        super().start_turn()
        print("enemies:", self.find_enemies())
        if self.state == None:
            self.state = self.idle
        self.wait_time = 1
        self.wait_function = self.state
    
    def end_turn(self):
        self.wait_time = -1
        self.wait_function = None 
        super().end_turn()
    
    def update(self):
        if self.state != self.end_turn and self.health <= 0:
            self.default_state = self.state 
            self.state = self.end_turn
        elif self.state == self.end_turn and self.health > 0:
            self.state = self.default_state
        if Map.get_map().current_character == self:
            if self.wait_time > 0 and self.wait_function != None:
                self.wait_time -= time.dt
                if self.wait_time <= 0:
                    self.wait_function()

if __name__ == "__main__": # this example is probably broken and needs to be rewritten
    oc = Character()
    oc.start_turn()
    while True:
        print("action pool:",oc.action_pool)
        print("tokens:", oc.tokens)
        for index in range(len(oc.actions)):
            print(index, oc.actions[index])
        print("which action will you take?")
        result = input(">")
        if result.isdigit() and int(result) < len(oc.actions):
            chosen_action = oc.actions[int(result)]
            print("Which die do you want to use?", oc.action_pool)
            result = input(">")
            if int(result) in oc.action_pool:
                chosen_action.act(oc, int(result))
            else:
                print("You don't have a die for that amount!")
        else:
            print("invalid action, goodbye!")
            break

    print("character.py ran")