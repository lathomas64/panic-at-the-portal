from actions.action import Action
from hud import ui
from fadingText import FadingText
from ursina import color, Button, window, destroy, Func
from sys import maxsize

class BringAction(Action):
    def __init__(self, actor):
        super().__init__("1+",
                         "A Challenger Approaches",
                         "Challenge an enemy within range 1-4.",
                         actor,
                         range=maxsize)

    def confirm_targets(self, actor, die, targetHex):
        if len(targetHex.children) == 0:
            FadingText("No valid target", targetHex, color.red)
            return
        target = targetHex.children[0]
        def challenge_targets():
            for targeted in ui.map.targeting["targets"]:
                targeted.add_tokens("challenge", 1)
            ui.map.targeting = None
            die.consume()
            destroy(self.confirm)
        self.confirm = Button("confirm targets", scale=(.3,.1), on_click=Func(challenge_targets))
        self.confirm.x = window.top_right.x-.17
        ui.map.targeting["targets"].append(target)