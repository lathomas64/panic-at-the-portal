from actions.action import Action
from hud import UI
from fadingText import FadingText
from ursina import color # TODO fold color from fading Text into fading text

class DamageAction(Action):
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

    def confirm_targets(self, actor, die, targetHex):
        print(actor, die, targetHex)
        print(targetHex.children)
        if len(targetHex.children) == 0:
            FadingText("No valid target", targetHex, color.red)
            return
        print(actor, actor.parent)
        if actor.parent.distance(targetHex) > actor.range:
            FadingText("out of range", targetHex, color.red)
            return
        target = targetHex.children[0]
        if type(target) == FadingText:
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