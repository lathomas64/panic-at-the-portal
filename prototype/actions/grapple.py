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

    def confirm_targets(self, actor, die, targetHex):
        if actor.parent.distance(targetHex) > actor.range:
            FadingText("out of range", targetHex, color.red)
            return
        if len(targetHex.children) == 0:
            FadingText("No valid target", targetHex, color.red)
            return
        target = targetHex.children[0]
        actor.pull(target, die.value)
        UI.game_map.targeting = None
        die.consume()
    