'''
Bring it on action
'''
from sys import maxsize
from ursina import color, Button, window, Func
from prototype.actions.action import Action
from prototype.hud import UI
from prototype.fading_text import FadingText


class BringAction(Action):
    '''
    Implementation of Bring it on action
    5+ challenge any number of enemies within line of sight
    basic action
    '''
    def __init__(self, actor):
        super().__init__("5+",
                         "Bring it on!",
                         "Challenge any number of enemies within line of sight",
                         actor,
                         action_range=maxsize)
        self.confirm = None

    def confirm_targets(self, actor, die, target_hex):
        '''
        confirm_targets
        because we have multiple targets we
        add our target to a list and keep going
        but setup a button to confirm all targets.
        '''
        if len(target_hex.children) == 0:
            FadingText("No valid target", target_hex, color.red)
            return
        target = target_hex.children[0]
        def challenge_targets():
            for targeted in UI.game_map.targeting["targets"]:
                actor.challenge(targeted)
            UI.game_map.targeting = None
            die.consume()
            self.confirm.disable()

        if not hasattr(self, "confirm"): # don't add button again if we already added it
            self.confirm = Button("confirm targets", scale=(.3,.1),
                                  on_click=Func(challenge_targets))
            self.confirm.x = window.top_right.x-.1
        else:
            print("reenabling confirm button")
            self.confirm.enable()
            self.confirm.on_click = Func(challenge_targets)
            self.confirm.x = window.top_right.x-.1
        UI.game_map.targeting["targets"].append(target)
