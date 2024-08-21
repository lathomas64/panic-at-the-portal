from ursina import Button, window, color, Tooltip, Func, destroy
from grid import Map, Hex 
from die import Die
from fadingText import FadingText
from ursina.prefabs.button_list import ButtonList
from sys import maxsize

class Action(Button):
    basic_actions = []
    def __init__(self, cost, name, description, available, act):
        super().__init__(scale=(.3,.1), x = window.top_left.x+.170, y=3, text=str(self))
        self.cost = cost
        self.name = name 
        self.description = description 
        self.available = available 
        self.act = act
        self.tooltip = Tooltip(self.description)
        self.enabled = False
    
    def update(self):
        self.text = self.cost + ": " + self.name
        if self.available(Map.get_map().current_character):
            #self.enabled = True 
            self.disabled = False
            self.on_click = self.on_click = lambda : self.act(Map.get_map().current_character, Die.selected)
            self.color = color.black
            pass
        else:
            #self.enabled = False
            self.disabled = True
            self.on_click = lambda : None
            self.color = color.gray
            pass
    
    @classmethod 
    def get_basic_actions(cls, ai=False):
        if cls.basic_actions != [] and not ai: # TODO Horrible hack please fix this for ai characters
            return cls.basic_actions 
        def do_move(actor, die):
            actor.add_tokens("speed", die.value)
            die.consume()
        move = Action("X", 
               "Movement", 
               "Gain X speed tokens", 
               lambda actor: actor.has_dice() and Die.selected != None,
               do_move)
        def do_damage(actor, die, targetHex):
            print(actor, die, targetHex)
            print(targetHex.children)
            if len(targetHex.children) == 0:
                FadingText("No valid target", targetHex, color.red)
                return
            if actor.parent.distance(targetHex) > actor.range:
                FadingText("out of range", targetHex, color.red)
                return
            target = targetHex.children[0]
            if type(target) == FadingText:
                print("we can't attack fading text...")
                return
            print("deal damage to ",target)
            if die.value >= 9:
                print("deal 5 damage, and push them 3 spaces")
                target.take_damage(5)
                actor.push(target, 3)
            elif die.value >= 7:
                print("Deal 4 damage, and push them 2 spaces.")
                target.take_damage(4)
                actor.push(target, 2)
            elif die.value >= 5:
                print("Deal 3 damage, and push them 1 space away")
                target.take_damage(3)
                actor.push(target, 1)
            elif die.value >= 3:
                print("Deal 2 damage")
                target.take_damage(2)
            else:
                print("Deal 1 damage")
                target.take_damage(1)
            Map.targeting = None
            die.consume()
        def basic_damage(actor, die):
            print(actor, " trying to use damage action with ",die)
            Map.targeting = {"actor":actor, "action":do_damage, "die":die}
        damage = Action("1+",
                        "Damage",
                        """
                        Deal 1 damage to one enemy in your range
                            3+: Deal 2 damage instead.
                            5+: Deal 3 damage instead, and push them 1 space away.
                            7+: Deal 4 damage instead, and push them 1 more space.
                            9+: Deal 5 damage instead, and push them 1 more space.
                        """,
                        lambda actor: actor.has_dice() and Die.selected != None,
                        basic_damage)
        def do_throw(actor, die, targetHex):
            if actor.parent.distance(targetHex) > 1: #throw has a fixed range
                FadingText("out of range", targetHex, color.red)
                return
            if len(targetHex.children) == 0:
                FadingText("No valid target", targetHex, color.red)
                return
            target = targetHex.children[0]
            actor.push(target, die.value)
            Map.targeting = None
            die.consume()
        def basic_throw(actor, die):
            Map.targeting = {"actor": actor, "action": do_throw, "die": die, "range":1}
        throw = Action("X",
                       "Throw",
                       "Choose an adjacent enemy or ally, and push them X spaces.",
                       lambda actor: actor.has_dice() and Die.selected != None,
                       basic_throw
                       )
        
        def do_grapple(actor, die, targetHex):
            if actor.parent.distance(targetHex) > actor.range:
                FadingText("out of range", targetHex, color.red)
                return
            if len(targetHex.children) == 0:
                FadingText("No valid target", targetHex, color.red)
                return
            target = targetHex.children[0]
            actor.pull(target, die.value)
            Map.targeting = None
            die.consume()
        def basic_grapple(actor, die):
            Map.targeting = {"actor": actor, "action": do_grapple, "die": die}
        grapple = Action("X",
                       "Grapple",
                       "Choose an enemy or ally within range, and pull them X spaces towards you.",
                       lambda actor: actor.has_dice() and Die.selected != None,
                       basic_grapple
                       )
        
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
        def basic_open(actor, die):
            Map.targeting = {"actor": actor, "action": do_open, "die": die}

        open = Action("1+",
                      "Open the Path",
                      """
                      Destroy one Obstacle within range.
                      4+: Also destroy Obstacles adjacent to it.
                      8+: Also destroy Obstacles adjacent to those.
                      """,
                      lambda actor: actor.has_dice() and Die.selected != None,
                      basic_open)
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
        def basic_challenge(actor, die):
            Map.targeting = {"actor": actor, "action": do_challenge, "die":die, "range":4}
        challenger = Action("1+",
                            "A Challenger Approaches",
                            "Challenge an enemy within range 1-4.",
                            lambda actor: actor.has_dice() and Die.selected != None,
                            basic_challenge)
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
        def basic_douse(actor, die):
            Map.targeting = {"actor": actor, "action": do_douse, "die":die}
        douse = Action("2+",
                       "Put it Out!",
                       """
                        Remove one token from someone in range.
                        4+: Remove another token.
                        7+: Remove another token.
                       """,
                       lambda actor: actor.has_dice() and Die.selected != None and Die.selected.value >=2,
                       basic_douse)
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
                destroy(cls.confirm)
            cls.confirm = Button("confirm targets", scale=(.3,.1), on_click=Func(challenge_targets))
            cls.confirm.x = window.top_right.x-.17
            Map.targeting["targets"].append(target)
        def basic_bring(actor, die):
            Map.targeting = {"actor": actor, "action": do_bring, "die":die, "range": maxsize, "targets":[]}
        bringit = Action("4+",
                         "Bring it on!",
                         "Challenge any number of enemies you can see.",
                         lambda actor: actor.has_dice() and Die.selected != None and Die.selected.value >=4,
                         basic_bring)
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
        def basic_rescue(actor, die):
            Map.targeting = {"actor": actor, "action": do_rescue, "die":die}
        rescue = Action("5+",
                        "Rescue",
                        "Pick an ally within range who's at 0 HP, and heal them. If they aren't in play, they return to play on the space of their choice.",
                        lambda actor: actor.has_dice() and Die.selected != None and Die.selected.value >=5,
                        basic_rescue)
        act = Action("",
                     "Act",
                     "Other basic actions",
                     lambda actor: True,
                     lambda actor, die: actor.set_actions([throw, grapple, open, challenger, douse, bringit, rescue]))
        end = Action("",
                     "End Turn",
                     "End your turn",
                     lambda actor: True,
                     lambda actor, die: actor.end_turn())
        def basic_explore(actor, die):
            Map.get_map().explore()
            die.consume()
        explore = Action("1+",
                         "Explore",
                         "Explore what lies beyond visible borders. reveal more hexes at an edge.",
                         lambda actor: actor.has_dice() and Die.selected != None,
                         basic_explore)
        #[throw, grapple, open, challenger, douse, bringit, rescue]
        cls.basic_actions = [move, damage,explore, act, end]
        print(ai)
        if ai:
            return [move,damage,throw,grapple,open,challenger,douse,bringit,rescue]
        return cls.basic_actions