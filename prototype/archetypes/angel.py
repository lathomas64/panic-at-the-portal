from archetypes.archetype import Archetype
from ursina import color
from hud import ui
from fadingText import FadingText

class Angel(Archetype):
    def __init__(self):
        pass
    def confirm_targets(self, actor, _die, targetHex):
        if len(targetHex.children) == 0:
            FadingText("No valid target", targetHex, color.red)
            return
        target = targetHex.children[0]
        target.take_damage(1)
        actor.heal(1)
    
    def drain(self):
        ui.map.targeting = {"actor":self.actor, "action": self.confirm_targets}
    
    def on_add(self, character):# run when we are added to an actor
        character.register_hook("start_turn", self.drain)
        character.register_hook("after_challenge", self.drain)
