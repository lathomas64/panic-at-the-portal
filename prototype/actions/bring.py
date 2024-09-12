from actions.action import Action
from hud import UI
from fadingText import FadingText
from ursina import color, Button, window, destroy, Func
from sys import maxsize

class BringAction(Action):
    def __init__(self, actor):
        super().__init__("5+",
                         "Bring it on!",
                         "Challenge any number of enemies within line of sight",
                         actor,
                         range=maxsize)

    def confirm_targets(self, actor, die, targetHex):
        if len(targetHex.children) == 0:
            FadingText("No valid target", targetHex, color.red)
            return
        target = targetHex.children[0]
        def challenge_targets():
            for targeted in UI.game_map.targeting["targets"]:
                actor.challenge(targeted)
            UI.game_map.targeting = None
            die.consume()
            self.confirm.disable()

        if not hasattr(self, "confirm"): # don't add button again if we already added it
            self.confirm = Button("confirm targets", scale=(.3,.1), on_click=Func(challenge_targets))
            self.confirm.x = window.top_right.x-.1
        else:
            print("reenabling confirm button")
            self.confirm.enable()
            self.confirm.on_click = Func(challenge_targets)
            self.confirm.x = window.top_right.x-.1
        UI.game_map.targeting["targets"].append(target)