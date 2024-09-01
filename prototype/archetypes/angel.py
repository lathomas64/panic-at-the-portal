from archetypes.archetype import Archetype
from ursina import color
from hud import ui
from fadingText import FadingText

class Angel(Archetype):
    
    def confirm_targets(self, actor, _die, targetHex):
        if len(targetHex.children) == 0:
            FadingText("No valid target", targetHex, color.red)
            return
        target = targetHex.children[0]
        actor.challenge(target)
        #target.add_tokens("challenge", 1)
        self.drain(target)
        ui.map.targeting = None

    def target_drain(self):
        ui.map.targeting = {"actor":self.actor, "action": self.confirm_targets, "die":None}
    
    def drain(self, target):
        target.take_damage(1)
        self.actor.heal(1)
    
    def on_add(self, character):# run when we are added to an actor
        character.register_hook("start_turn", self.target_drain)
        character.register_hook("after_challenge", self.drain)
        print(character.hooks, len(character.hooks))