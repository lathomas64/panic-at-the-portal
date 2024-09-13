'''
Damage action
'''
from ursina import color
from prototype.actions.action import Action
from prototype.hud import UI
from prototype.fading_text import FadingText

class DamageAction(Action):
    '''
    turn dice into damage and maybe pushing
    '''
    def __init__(self, actor):
        super().__init__("1+",
               "Damage", 
                """
                Deal 1 damage to one enemy in your range
                    3+: Deal 2 damage instead.
                    5+: Deal 3 damage instead, and push them 1 space away.
                    7+: Deal 4 damage instead, and push them 1 more space.
                    9+: Deal 5 damage instead, and push them 1 more space.
                """,
                actor)

    def confirm_targets(self, actor, die, target_hex):
        '''
        handles the actual damage when targets are selected
        '''
        print(actor, die, target_hex)
        print(target_hex.children)
        if len(target_hex.children) == 0:
            FadingText("No valid target", target_hex, color.red)
            return
        print(actor, actor.parent)
        if actor.parent.distance(target_hex) > actor.range:
            FadingText("out of range", target_hex, color.red)
            return
        target = target_hex.children[0]
        if isinstance(target, FadingText):
            print("we can't attack fading text...")
            return
        print("deal damage to ",target)
        if die.value >= 9:
            print("deal 5 damage, and push them 3 spaces")
            target.take_damage(5)
            actor.push(target, 3)
        elif die.value >= 7:
            print("Deal 4 damage, and push them 2 spaces.")
            target.take_damage(4)
            actor.push(target, 2)
        elif die.value >= 5:
            print("Deal 3 damage, and push them 1 space away")
            target.take_damage(3)
            actor.push(target, 1)
        elif die.value >= 3:
            print("Deal 2 damage")
            target.take_damage(2)
        else:
            print("Deal 1 damage")
            target.take_damage(1)
        UI.game_map.targeting = None
        die.consume()
