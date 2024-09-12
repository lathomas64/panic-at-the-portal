'''
Module representing the Angel Archetype
'''
from ursina import color
from prototype.archetypes.archetype import Archetype
from prototype.hud import UI
from prototype.fading_text import FadingText

class Angel(Archetype):
    '''
    Class for the Angel Archetype
    '''

    def confirm_targets(self, actor, _die, target_hex):
        '''
        implementing the targeted drain after we have picked a target
        challenges the target then drains them
        '''
        if len(target_hex.children) == 0:
            FadingText("No valid target", target_hex, color.red)
            return
        target = target_hex.children[0]
        actor.challenge(target)
        #target.add_tokens("challenge", 1)
        self.drain(target)
        UI.game_map.targeting = None

    def target_drain(self):
        '''
        implemention of angel's on start_turn hook
        At the beginning of your turn challenge an enemy you can see,
        deal 1 damage to them, then heal 1
        we start with picking a target
        '''
        UI.game_map.targeting = {"actor":self.actor, "action": self.confirm_targets, "die":None}

    def drain(self, target):
        '''
        Angel's after challenge hook
        after ou challenge an enemy, deal 1 damage to them, then heal 1
        '''
        target.take_damage(1)
        self.actor.heal(1)

    def on_add(self, character):# run when we are added to an actor
        '''
        on_add when we put this archetype on a character we should register its hooks
        '''
        character.register_hook("start_turn", self.target_drain)
        character.register_hook("after_challenge", self.drain)
        print(character.hooks, len(character.hooks))
