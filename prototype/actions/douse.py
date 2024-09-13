'''
Douse action
'''
from ursina import color, destroy, Func
from ursina.prefabs.button_list import ButtonList
from prototype.actions.action import Action
from prototype.hud import UI
from prototype.fading_text import FadingText
from prototype.actions.actor import Actor

class DouseAction(Action):
    '''
    Remove 1-3 tokens from someone in range
    '''
    def __init__(self, actor: Actor):
        super().__init__("2+",
                         "Put it Out!",
                         """
                         Remove one token from someone in range.
                         4+: Remove another token.
                         7+: Remove another token.
                         """,
                         actor)
        self.token_count = 1

    def confirm_targets(self, actor, die, target_hex):
        '''
        pops up a menu of tokens to select which one to remove
        after we select our target
        '''
        if actor.parent.distance(target_hex) > actor.range:
            FadingText("out of range", target_hex, color.red)
            return
        if len(target_hex.children) == 0:
            FadingText("No valid target", target_hex, color.red)
            return
        target = target_hex.children[0]
        token_count = 1
        if die.value >= 7:
            token_count = 3
        elif die.value >= 4:
            token_count = 2
        self.token_count = token_count
        def decrement_tokens(token_type):
            target.spend_tokens(token_type, 1)
            print(target.tokens)
            self.token_count -= 1
            if target.get_tokens(token_type) <= 0:
                del token_dict[token_type]
                token_list.button_dict = token_dict
            if self.token_count == 0:
                destroy(token_list)
            if len(token_dict) <= 0:
                destroy(token_list)

        token_dict = {}
        for token_type in target.tokens.keys():
            if target.get_tokens(token_type) > 0:
                token_dict[token_type] = Func(decrement_tokens, token_type)
        print(token_dict)
        if len(token_dict) <= 0:
            FadingText("No Tokens to remove", target_hex, color.red)
            return
        token_list = ButtonList(token_dict,
                                font='VeraMono.ttf',
                                button_height=1.5,
                                popup=0,
                                clear_selected_on_enable=False)
        UI.game_map.targeting = None
        die.consume()
