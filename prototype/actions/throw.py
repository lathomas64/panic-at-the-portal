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

    def confirm_targets(self, actor, die, target_hex):
        print(target_hex, target_hex.children)
        if actor.parent.distance(target_hex) > 1: #throw has a fixed range
            FadingText("out of range", target_hex, color.red)
            return
        if len(target_hex.children) == 0:
            FadingText("No valid target", target_hex, color.red)
            return
        target = target_hex.children[0]
        actor.push(target, die.value)
        UI.game_map.targeting = None
        die.consume()
    