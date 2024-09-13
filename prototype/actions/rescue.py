from prototype.actions.action import Action
from prototype.hud import UI
from prototype.fading_text import FadingText
from ursina import color

class RescueAction(Action):
    def __init__(self, actor):
        super().__init__("5+",
                        "Rescue",
                        "Pick an ally within range who's at 0 HP, and heal them. If they aren't in play, they return to play on the space of their choice.",
                         actor)

    def confirm_targets(self, actor, die, target_hex):
        if len(target_hex.children) == 0:
            FadingText("No valid target", target_hex, color.red)
            return
        target = target_hex.children[0]
        if target.health > 0:
            FadingText("Target is not down", target_hex, color.red)
            return
        # TODO check if they are an ally, list for out of play allies 
        target.heal(2)
        UI.game_map.targeting = None
        die.consume()