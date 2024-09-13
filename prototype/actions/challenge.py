'''
module for the challenge action
'''
from ursina import color
from prototype.actions.action import Action
from prototype.hud import UI
from prototype.fading_text import FadingText

class ChallengeAction(Action):
    '''
    Challenge action
    '''
    def __init__(self, actor):
        super().__init__("1+",
                         "A Challenger Approaches",
                         "Challenge an enemy within range 1-4.",
                         actor,
                         action_range=4)

    def confirm_targets(self, actor, die, target_hex):
        '''
        When we have chosen targets, the target gets challenged
        '''
        if actor.parent.distance(target_hex) > 4:
            FadingText("out of range", target_hex, color.red)
            return
        if len(target_hex.children) == 0:
            FadingText("No valid target", target_hex, color.red)
            return
        target = target_hex.children[0]
        actor.challenge(target)
        UI.game_map.targeting = None
        die.consume()
