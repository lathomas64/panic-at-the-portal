from actions.action import Action
from actions.move import MoveAction
from actions.damage import DamageAction
from actions.throw import ThrowAction
from actions.grapple import GrappleAction
from die import Die
from grid import Map
from fadingText import FadingText
from ursina import SpriteSheetAnimation, window, color, time, destroy, Func, Button
from sys import maxsize
from ursina.prefabs.button_list import ButtonList
#from ursina.prefabs.health_bar import HealthBar

class Character(SpriteSheetAnimation):
    # actions movement die in speed tokens out
    basic_actions = []
    def __init__(self, sheet="placeholder_character.png", name="default"):
        self.action_pool = Die.create_pool(["d4", "d6", "d8", "d10"])
        self.tokens = {}
        self.actions = []
        self.hooks = {}
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

    @property
    def range(self):
        return 2
    
    def register_hook(self, name, func):
        if name in self.hooks:
            self.hooks[name].append(func)
        else:
            self.hooks[name] = [func]
    
    def fire_hook(self, name):
        for function in self.hooks.get(name, []):
            function()

    def is_active_turn(self):
        return Map.get_map().current_character == self

    def in_range(self, other, distance=None):
        if distance == None:
            distance = self.range
        return self.parent.distance(other.parent) <= distance
    
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
        self.actions = self.get_basic_actions()
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
        self.fire_hook("start_turn")
    
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
    
    def get_basic_actions(self, ai=False):
        if self.basic_actions != [] and not ai: # TODO Horrible hack please fix this for ai characters
            return self.basic_actions 
        move = MoveAction(self)
        damage = DamageAction(self)
        throw = ThrowAction(self)
        grapple = GrappleAction(self)
        
        def do_open(actor, die, targetHex):
            if targetHex.obstacle == None:
                FadingText("No Obstacles here", targetHex, color.red)
                return 
            radius = 0
            if die.value >= 8:
                radius = 2
            elif die.value >= 4:
                radius = 1
            targetHex.clearObstacles(radius)
            Map.targeting = None
            die.consume()    

        open = Action("1+",
                      "Open the Path",
                      """
                      Destroy one Obstacle within range.
                      4+: Also destroy Obstacles adjacent to it.
                      8+: Also destroy Obstacles adjacent to those.
                      """,
                      self)
        open.confirm_targets = do_open
        
        def do_challenge(actor, die, targetHex):
            if actor.parent.distance(targetHex) > 4:
                FadingText("out of range", targetHex, color.red)
                return
            if len(targetHex.children) == 0:
                FadingText("No valid target", targetHex, color.red)
                return
            target = targetHex.children[0]
            target.add_tokens("challenge", 1) #TODO challenge tokens need to reference challenger
            Map.targeting = None 
            die.consume()
        
        challenger = Action("1+",
                            "A Challenger Approaches",
                            "Challenge an enemy within range 1-4.",
                            self,
                            range=4)
        challenger.confirm_targets = do_challenge

        def do_douse(actor, die, targetHex):
            if actor.parent.distance(targetHex) > actor.range:
                FadingText("out of range", targetHex, color.red)
                return
            if len(targetHex.children) == 0:
                FadingText("No valid target", targetHex, color.red)
                return
            target = targetHex.children[0]
            tokenCount = 1
            if die.value >= 7:
                tokenCount = 3
            elif die.value >= 4:
                tokenCount = 2
            cls.tokenCount = tokenCount #temporary variable to allow tokenCount to be accessible inside decrement
            def decrement_tokens(token_type):
                target.spend_tokens(token_type, 1)
                print(target.tokens)
                cls.tokenCount -= 1
                if target.get_tokens(token_type) <= 0:
                    print("does this fire?")
                    del token_dict[token_type]
                    token_list.button_dict = token_dict
                if cls.tokenCount == 0:
                    destroy(token_list)
                if len(token_dict) <= 0:
                    destroy(token_list)

            token_dict = {}
            for token_type in target.tokens.keys():
                if target.get_tokens(token_type) > 0:
                    token_dict[token_type] = Func(decrement_tokens, token_type)
            print(token_dict)
            if len(token_dict) <= 0:
                FadingText("No Tokens to remove", targetHex, color.red)
                return
            token_list = ButtonList(token_dict, font='VeraMono.ttf', button_height=1.5, popup=0, clear_selected_on_enable=False)
            Map.targeting = None 
            die.consume()
        
        douse = Action("2+",
                       "Put it Out!",
                       """
                        Remove one token from someone in range.
                        4+: Remove another token.
                        7+: Remove another token.
                       """,
                       self)
        douse.confirm_targets = do_douse
        
        def do_bring(actor, die, targetHex):
            if len(targetHex.children) == 0:
                FadingText("No valid target", targetHex, color.red)
                return
            target = targetHex.children[0]
            def challenge_targets():
                for targeted in Map.targeting["targets"]:
                    targeted.add_tokens("challenge", 1)
                Map.targeting = None
                die.consume()
                destroy(self.confirm)
            self.confirm = Button("confirm targets", scale=(.3,.1), on_click=Func(challenge_targets))
            self.confirm.x = window.top_right.x-.17
            Map.targeting["targets"].append(target)
        bringit = Action("4+",
                         "Bring it on!",
                         "Challenge any number of enemies you can see.",
                         self,
                         range=maxsize)
        bringit.confirm_targets = do_bring

        def do_rescue(actor, die, targetHex):
            if len(targetHex.children) == 0:
                FadingText("No valid target", targetHex, color.red)
                return
            target = targetHex.children[0]
            if target.health > 0:
                FadingText("Target is not down", targetHex, color.red)
                return
            # TODO check if they are an ally, list for out of play allies 
            target.heal(2)
            Map.targeting = None
            die.consume()
        rescue = Action("5+",
                        "Rescue",
                        "Pick an ally within range who's at 0 HP, and heal them. If they aren't in play, they return to play on the space of their choice.",
                        self)
        rescue.confirm_targets = do_rescue
        
        act = Action("",
                     "Act",
                     "Other basic actions",
                     self)
        act.is_available = lambda: True
        act.act = lambda die: act.actor.set_actions([throw, grapple, open, challenger, douse, bringit, rescue])
        
        end = Action("",
                     "End Turn",
                     "End your turn",
                     self)
        end.is_available = lambda: True 
        end.act = lambda die: end.actor.end_turn() 
        # TODO should act and end be actions?
        
        def basic_explore(actor, die):
            Map.get_map().explore()
            die.consume()
        explore = Action("1+",
                         "Explore",
                         "Explore what lies beyond visible borders. reveal more hexes at an edge.",
                         self)
        explore.act = basic_explore
        #[throw, grapple, open, challenger, douse, bringit, rescue]
        self.basic_actions = [move, damage,explore, act, end]
        print(ai)
        if ai:
            return [move,damage,throw,grapple,open,challenger,douse,bringit,rescue]
        return self.basic_actions



class AICharacter(Character):
    state = None
    wait_time = -1
    wait_function = None

    def get_action(self, name):
        print(name, Character.get_basic_actions(True))
        for action in Character.get_basic_actions(True):
            if action.name == name:
                return action
        return None

    def available_dice(self, value=-1):
        if value > 1:
            return [die for die in self.action_pool if die.used == False and die.value > value]
        else:    
            return [die for die in self.action_pool if die.used == False]
    
    def enemies_in_range(self, distance=None):
        if distance == None:
            distance = self.range
        return [character for character in self.find_enemies() if self.in_range(character, distance)]

    def freeze(self):
        FadingText(self.name + " Freezes in panic",self.parent, color.black, 1)
        self.wait_time = 1
        self.wait_function = self.end_turn
        #self.end_turn()
    
    def flight(self):
        FadingText(self.name + " tries to flee.", self.parent, color.black, 1)
        self.wait_time = 1
        while len(self.available_dice()) > 0:
            print("how to flee?")

    def fight(self):
        FadingText(self.name + " is looking for a fight.", self.parent, color.black, 1)
        self.wait_time = 1
        dice = self.available_dice()
        if len(dice) == 0:
            self.wait_function = self.end_turn
            return
        nearby = self.enemies_in_range()
        if len(nearby) > 0:
            # TODO smarter selection of which die and which target
            die = self.available_dice()[0]
            target = nearby[0]
            action = self.get_action("Damage")
            action.act(self, die)
            Map.get_map().targeting["action"](self, die, target.parent)
            return
        elif len(self.enemies_in_range(4)) > 0:
            challengable = self.enemies_in_range(4)
            die = self.available_dice()[0]
            target = challengable[0]
            action = self.get_action("A Challenger Approaches")
            action.act(self,die)
            Map.get_map().targeting["action"](self, die, target.parent)
            return
        elif len(self.find_enemies()) > 0 and len(self.available_dice(4)) > 0:
            enemies = self.find_enemies()
            die = self.available_dice(4)[0]
            target = enemies[0]
            action = self.get_action("Bring it on!")
            action.act(self,die)
            [Map.get_map().targeting["action"](self, die,enemy.parent) for enemy in enemies]
            Action.confirm.on_click()
            return
        # if we get here there's no action we can take
        self.wait_function = self.end_turn

    def find_enemies(self):
        return [character for character in Map.get_map().turns if character.team == None or character.team != self.team]
    
    def start_turn(self):
        print("AICharacter start turn...")
        super().start_turn()
        print("enemies:", self.find_enemies())
        if self.state == None:
            self.state = self.freeze
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