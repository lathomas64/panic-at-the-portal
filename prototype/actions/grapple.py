from prototype.actions.action import Action
from prototype.hud import UI
from prototype.fading_text import FadingText
from ursina import color

class GrappleAction(Action):
    def __init__(self, actor):
        super().__init__("X", 
               "Grapple", 
               "Choose an enemy or ally within range, and pull them X spaces towards you.",
               actor)

    def confirm_targets(self, actor, die, target_hex):
        if actor.parent.distance(target_hex) > actor.range:
            FadingText("out of range", target_hex, color.red)
            return
        if len(target_hex.children) == 0:
            FadingText("No valid target", target_hex, color.red)
            return
        target = target_hex.children[0]
        actor.pull(target, die.value)
        UI.game_map.targeting = None
        die.consume()
    