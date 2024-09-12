from actions.action import Action
from hud import UI
from prototype.fading_text import FadingText
from ursina import color

class RescueAction(Action):
    def __init__(self, actor):
        super().__init__("5+",
                        "Rescue",
                        "Pick an ally within range who's at 0 HP, and heal them. If they aren't in play, they return to play on the space of their choice.",
                         actor)

    def confirm_targets(self, actor, die, targetHex):
        if len(targetHex.children) == 0:
            FadingText("No valid target", targetHex, color.red)
            return
        target = targetHex.children[0]
        if target.health > 0:
            FadingText("Target is not down", targetHex, color.red)
            return
        # TODO check if they are an ally, list for out of play allies 
        target.heal(2)
        UI.game_map.targeting = None
        die.consume()