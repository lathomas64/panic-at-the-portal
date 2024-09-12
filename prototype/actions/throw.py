from prototype.actions.action import Action
from prototype.hud import UI
from prototype.fading_text import FadingText
from ursina import color

class ThrowAction(Action):
    def __init__(self, actor):
        super().__init__("X", 
               "Throw", 
               "Choose an adjacent enemy or ally, and push them X spaces.",
               actor,
               action_range=1)

    def confirm_targets(self, actor, die, targetHex):
        print(targetHex, targetHex.children)
        if actor.parent.distance(targetHex) > 1: #throw has a fixed range
            FadingText("out of range", targetHex, color.red)
            return
        if len(targetHex.children) == 0:
            FadingText("No valid target", targetHex, color.red)
            return
        target = targetHex.children[0]
        actor.push(target, die.value)
        UI.game_map.targeting = None
        die.consume()
    