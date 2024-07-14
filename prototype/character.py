import random
from action import Action
from die import Die
from grid import Hex
from ursina import SpriteSheetAnimation, window

class Character(SpriteSheetAnimation):
    # actions movement die in speed tokens out

    def __init__(self, sheet="placeholder_character.png"):
        self.action_pool = Die.create_pool(["d4", "d6", "d8", "d10"])
        self.tokens = {}
        self.actions = Action.get_basic_actions()
        self.max_health = 6
        self.health = self.max_health

        super().__init__(sheet, scale=.5, fps=4, z=-1, tileset_size=[4,4], animations={
        'idle' : ((0,3), (0,3)),        # makes an animation from (0,0) to (0,0), a single frame
        'walk_up' : ((0,0), (3,0)),     # makes an animation from (0,0) to (3,0), the bottom row
        'walk_right' : ((0,1), (3,1)),
        'walk_left' : ((0,2), (3,2)),
        'walk_down' : ((0,3), (3,3)),
        })
        self.play_animation('walk_down')

    def take_damage(self, amount):
        self.health -= amount 
        print(self.health,"/",self.max_health)
    
    def heal(self, amount):
        self.health += amount
        print(self.health,"/",self.max_health)
    
    def push(self, target, amount):
        qdiff = target.parent.q - self.parent.q 
        rdiff = target.parent.r - self.parent.r
        print(qdiff)
        print(rdiff)
        destination_coords = (target.parent.q, target.parent.r)
        if abs(qdiff) > abs(rdiff):
            #push q            
            if qdiff > 0:
                destination_coords = (target.parent.q+amount, target.parent.r) 
            else:
                destination_coords = (target.parent.q-amount, target.parent.r) 
        else:
            #push r
            if rdiff > 0:
                destination_coords = (target.parent.q, target.parent.r+amount)
            else:
                destination_coords = (target.parent.q, target.parent.r-amount)
        print("attempting to push ",target, " ", amount, " hexes")
        target.parent = Hex.map[destination_coords]
        
    def get_tokens(self, tokenType: str) -> int:
        if tokenType in self.tokens:
            return self.tokens[tokenType]
        else:
            return 0

    def add_tokens(self, tokenType: str, tokenAmount:int):
        if tokenType in self.tokens:
            self.tokens[tokenType] += tokenAmount 
        else:
            self.tokens[tokenType] = tokenAmount
    
    def spend_tokens(self, tokenType: str, tokenAmount:int):
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
            action.act(self, Die.selected.value)
            Die.selected.consume()
        else:
            action.act(self, None) #this will get more complicated later with token actions

    def start_turn(self):
        # anything else at start of turn
        for die in self.action_pool:
            die.roll()
        for index in range(len(self.actions)):
            action = self.actions[index]
            # these will have to adjust based on index in future when there are multiple
            action.x = window.top_left.x+.17
            action.y = .3 - .1125 * index
    
    def end_turn(self):
        self.tokens["speed"] = 0 # unless special conditions


# Basic actions


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