from actions.action import Action
from hud import UI
from fadingText import FadingText
from ursina import color

class ChallengeAction(Action):
    def __init__(self, actor):
        super().__init__("1+",
                         "A Challenger Approaches",
                         "Challenge an enemy within range 1-4.",
                         actor,
                         range=4)

    def confirm_targets(self, actor, die, targetHex):
        if actor.parent.distance(targetHex) > 4:
            FadingText("out of range", targetHex, color.red)
            return
        if len(targetHex.children) == 0:
            FadingText("No valid target", targetHex, color.red)
            return
        target = targetHex.children[0]
        actor.challenge(target)
        UI.game_map.targeting = None 
        die.consume()
        
