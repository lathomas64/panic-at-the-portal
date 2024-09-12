'''
Game Characters and their management housed here
'''
from ursina import SpriteSheetAnimation, window, color, time, Func
from prototype.actions.action import Action
from prototype.actions.move import MoveAction
from prototype.actions.damage import DamageAction
from prototype.actions.throw import ThrowAction
from prototype.actions.grapple import GrappleAction
from prototype.actions.open import OpenAction
from prototype.actions.douse import DouseAction
from prototype.actions.bring import BringAction
from prototype.actions.rescue import RescueAction
from prototype.actions.challenge import ChallengeAction
from prototype.actions.explore import ExploreAction

from prototype.die import Die
from prototype.fading_text import FadingText
from prototype.hud import UI
#from ursina.prefabs.health_bar import HealthBar

class Character(SpriteSheetAnimation):
    '''
    Base class for Character players and NPCs
    both have common behaviors here
    '''
    # actions movement die in speed tokens out
    basic_actions = []
    def __init__(self, sheet="placeholder_character.png", name="default"):
        self.action_pool = Die.create_pool(["d4", "d6", "d8", "d10"])
        self.tokens = {}
        self.actions : list = []
        self.hooks = {}
        self.max_health = 6
        self.health = self.max_health
        self.stance = None
        self.stances = []
        self.team = name
        self.default_animation = "walk_down"
        self.color = color.white

        super().__init__(sheet, scale=.5, fps=4, z=-1, tileset_size=[4,4], animations={
        'idle' : ((0,3), (0,3)),        # makes an animation from (0,0) to (0,0), a single frame
        'walk_up' : ((0,0), (3,0)),     # makes an animation from (0,0) to (3,0), the bottom row
        'walk_right' : ((0,1), (3,1)),
        'walk_left' : ((0,2), (3,2)),
        'walk_down' : ((0,3), (3,3)),
        })
        self.name = name
        self.play_animation('walk_down')
        self.challengers = []

    @property
    def range(self):
        '''
        How far can most actions for this character reach
        '''
        return 2

    def register_hook(self, name, func):
        """
        observer pattern
        let this character now to call the function when
        the appropriate event occurs
        """
        if name in self.hooks:
            self.hooks[name].append(func)
        else:
            self.hooks[name] = [func]

    def fire_hook(self, name, **kwargs):
        '''
        observer pattern
        fire all functions registered to listen to
        a particular hook
        '''
        for function in self.hooks.get(name, []):
            function(**kwargs)

    def is_active_turn(self):
        '''
        just a check if its this character's turn
        '''
        return UI.game_map.current_character == self

    def in_range(self, other, distance=None):
        '''
        compare distance of two characters to see if 
        the other is in range of this character
        '''
        if distance is None:
            distance = self.range
        return self.parent.distance(other.parent) <= distance

    def take_damage(self, amount):
        '''
        handle logic for when a character is damaged
        '''
        self.health -= amount
        #self.health_bar.value = self.health
        FadingText(amount, self, color.red)
        if self.health <= 0:
            self.color = color.gray
            self.health = 0
            self.play_animation("idle")
        print(self.health,"/",self.max_health)

    def heal(self, amount):
        '''
        handle logic for when a character is healed
        '''
        self.health += amount
        self.play_animation(self.default_animation)
        self.color = color.white
        FadingText(amount, self, color.green)
        print(self.health,"/",self.max_health)

    def push(self, target, amount):
        '''
        push the target away from us
        if there is nowhere for them to go they should stop
        '''
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
            if (destination_q, destination_r) in UI.game_map:
                target.parent = UI.game_map[destination_q, destination_r]
            #should we have an else?

    def pull(self, target, amount):
        '''
        pull the target towards us. 
        just pushes a negative amount
        '''
        self.push(target, -1 * amount)

    def get_tokens(self, token_type: str) -> int:
        '''
        get the number of tokens of a particular type
        a character has
        '''
        if token_type in self.tokens:
            return self.tokens[token_type]
        return 0

    def challenge(self, target):
        '''
        add self to the list of the target's challengers
        '''
        target.add_tokens("challenge", 1)
        target.challengers.append(self)
        self.fire_hook("after_challenge", target=target)

    def add_tokens(self, token_type: str, token_amount:int):
        '''
        add tokens to the current character
        '''
        FadingText("+"+str(token_amount) + " " + token_type, self, color.green)
        if token_type in self.tokens:
            self.tokens[token_type] += token_amount
        else:
            self.tokens[token_type] = token_amount

    def discard_tokens(self, token_type: str, token_amount:int=1):
        '''
        get rid of tokens and fire discard_token hook
        '''
        self.spend_tokens(token_type, token_amount)
        self.fire_hook("discard_token")

    def spend_tokens(self, token_type: str, token_amount:int=1):
        '''
        spend tokens and display a fading text
        '''
        FadingText("-"+str(token_amount) + " " + token_type, self, color.red)
        if token_type not in self.tokens:
            return
        self.tokens[token_type] -= token_amount
        if self.tokens[token_type] < 0:
            self.tokens[token_type] = 0

    def has_dice(self):
        '''
        check if the character has any dice
        '''
        for die in self.action_pool:
            if die.used is False:
                return True
        # no unused dice here
        return False

    def get_actions(self):
        '''
        get a fresh list of our actions
        '''
        print("get actions...")
        for action in self.actions:
            action.enabled = False
        #build out top level menu of actions
        self.actions = self.get_basic_actions()
        if self.stance is not None:
            self.actions += self.stance.get_actions()

    def set_actions(self, actions):
        '''
        modify our list of actions
        '''
        for action in self.actions:
            action.enabled = False
        self.actions = actions
        self.show_actions()

    def show_actions(self):
        '''
        make actions visible on screen
        '''
        for index, action in enumerate(self.actions):
            # these will have to adjust based on index in future when there are multiple
            action.x = window.top_left.x+.17
            action.y = .3 - .1125 * index
            action.enabled = True

    @property
    def enemies(self):
        '''
        Property for quick handle of enemies
        if our teams are different or you don't have a team
        we're enemies
        '''
        return [character for character in UI.game_map.turns
                if character.team is None or character.team != self.team]

    @property
    def allies(self):
        '''
        property for easy handle of allied characters
        if our team is the same we're allies!
        '''
        return [character for character in UI.game_map.turns if character.team == self.team]

    def start_turn(self):
        '''
        get actions set up at the beginning of turns
        '''
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
        '''
        cleanup dice and speed tokens at end of turn.
        '''
        self.tokens["speed"] = 0 # unless special conditions
        Die.selected = None
        for die in self.action_pool:
            die.enabled = False
        for action in self.actions:
            action.enabled = False
        UI.game_map.advance_turn()

    def __str__(self):
        '''
        string representation for characters
        '''
        return self.name + "\n" + str(self.health) + "/" + str(self.max_health)

    def get_basic_actions(self):
        '''
        returns an array of the basic actions available to everyone
        '''
        if self.basic_actions:
            return self.basic_actions
        move = MoveAction(self)
        damage = DamageAction(self)
        throw = ThrowAction(self)
        grapple = GrappleAction(self)
        open_path = OpenAction(self)
        challenger = ChallengeAction(self)
        douse = DouseAction(self)
        bringit = BringAction(self)
        rescue = RescueAction(self)

        act = Action("",
                     "Act",
                     "Other basic actions",
                     self)
        act.is_available = lambda: True
        action_list = [throw, grapple, open_path, challenger, douse, bringit, rescue]
        act.act = lambda die: act.actor.set_actions(action_list)

        end = Action("",
                     "End Turn",
                     "End your turn",
                     self)
        end.is_available = lambda: True
        end.act = lambda die: end.actor.end_turn()

        explore = ExploreAction(self)
        #[throw, grapple, open, challenger, douse, bringit, rescue]
        self.basic_actions = [move, damage,explore, act, end]
        return self.basic_actions

class AICharacter(Character):
    '''
    Extra handling for AI characters
    '''

    def __init__(self, sheet="placeholder_character.png", name="default"):
        '''
        initializing AI characters same as default but with
        state setup
        '''
        super().__init__(sheet, name)
        self.state = Func(None)
        self.wait_time = -1
        self.wait_function = None
        self.default_state = Func(None)

    def get_basic_actions(self):
        move = MoveAction(self)
        damage = DamageAction(self)
        throw = ThrowAction(self)
        grapple = GrappleAction(self)
        open_path = OpenAction(self)
        challenger = ChallengeAction(self)
        douse = DouseAction(self)
        bringit = BringAction(self)
        rescue = RescueAction(self)
        return [move,damage,throw,grapple,open_path,challenger,douse,bringit,rescue]

    def get_action(self, name):
        '''
        gets an action by its name
        '''
        print(name, self.get_basic_actions())
        for action in self.get_basic_actions():
            if action.name == name:
                return action
        return None

    def available_dice(self, value=-1):
        '''
        boolean of if this character has any available dice
        if value is set checks any available dice with that value or hire
        '''
        if value > 1:
            return [die for die in self.action_pool if die.used is False and die.value > value]
        else:
            return [die for die in self.action_pool if die.used is False]

    def enemies_in_range(self, distance=None):
        '''
        calculate how many enemies are within a certain distance of this character
        '''
        if distance is None:
            distance = self.range
        return [character for character in self.enemies if self.in_range(character, distance)]

    def freeze(self):
        '''
        state function do nothing with this character's turn
        '''
        FadingText(self.name + " Freezes in panic",self.parent, color.black, 1)
        self.wait_time = 1
        self.wait_function = self.end_turn
        #self.end_turn()

    def flight(self):
        '''
        state function not implemented. try to put distance between self and enemies
        '''
        FadingText(self.name + " tries to flee.", self.parent, color.black, 1)
        self.wait_time = 1
        while len(self.available_dice()) > 0:
            print("how to flee?")

    def fight(self):
        '''
        state function attack a nearby enemy if one is in range
        otherwise attempt to challenge enemies
        '''
        FadingText(self.name + " is looking for a fight.", self.parent, color.black, 1)
        self.wait_time = 1
        dice = self.available_dice()
        if len(dice) == 0:
            self.wait_function = self.end_turn
            return
        nearby = self.enemies_in_range()
        if len(nearby) > 0:
            die = self.available_dice()[0]
            target = nearby[0]
            action = self.get_action("Damage")
            print("damage action:", action)
            action.act(die)
            UI.game_map.targeting["action"](self, die, target.parent)
            return
        if len(self.enemies_in_range(4)) > 0:
            challengable = self.enemies_in_range(4)
            die = self.available_dice()[0]
            target = challengable[0]
            action = self.get_action("A Challenger Approaches")
            action.act(die)
            UI.game_map.targeting["action"](self, die, target.parent)
            return
        if len(self.enemies) > 0 and len(self.available_dice(4)) > 0:
            die = self.available_dice(4)[0]
            target = self.enemies[0]
            action = self.get_action("Bring it on!")
            action.act(die)
            for enemy in self.enemies:
                UI.game_map.targeting["action"](self, die, enemy.parent)
            action.confirm.on_click()
            return
        # if we get here there's no action we can take
        self.wait_function = self.end_turn

    def start_turn(self):
        '''
        setup at beginning of ai character's turn
        '''
        print("AICharacter start turn...")
        super().start_turn()
        print("enemies:", self.enemies)
        if self.state is None:
            self.state.func = self.freeze
        self.wait_time = 1
        self.wait_function = self.state

    def end_turn(self):
        '''
        clean up at end of AI character's turn
        '''
        self.wait_time = -1
        self.wait_function = None
        super().end_turn()

    def update(self):
        '''
        AI character game loop
        '''
        if self.state != Func(self.end_turn) and self.health <= 0:
            self.default_state = self.state
            self.state.func = self.end_turn
        elif self.state == Func(self.end_turn) and self.health > 0:
            self.state = self.default_state
        if UI.game_map.current_character == self:
            if self.wait_time > 0 and self.wait_function is not None:
                self.wait_time -= time.dt
                if self.wait_time <= 0:
                    self.wait_function()
