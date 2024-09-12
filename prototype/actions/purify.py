from actions.action import Action
from hud import UI
from prototype.fading_text import FadingText
from ursina import color, destroy, Func 
from ursina.prefabs.button_list import ButtonList

class PurifyAction(Action):
    def __init__(self, actor):
        super().__init__("1+",
                        "Purify",
                        """
                         Remove one token token from yourself or an ally within range.
                         3+: Remove two tokens from someone within range.
                         6+: Do 3+ again.
                         """,
                         actor)

    def confirm_targets(self, actor, die, targetHex): # TODO this just does Douse right now need to let it target allies
        if actor.parent.distance(targetHex) > actor.range:
            FadingText("out of range", targetHex, color.red)
            return
        if len(targetHex.children) == 0:
            FadingText("No valid target", targetHex, color.red)
            return
        target = targetHex.children[0]
        tokenCount = 1
        if die.value >= 7:
            tokenCount = 3
        elif die.value >= 4:
            tokenCount = 2
        self.tokenCount = tokenCount #temporary variable to allow tokenCount to be accessible inside decrement
        def decrement_tokens(token_type):
            target.spend_tokens(token_type, 1)
            print(target.tokens)
            self.tokenCount -= 1
            if target.get_tokens(token_type) <= 0:
                print("does this fire?")
                del token_dict[token_type]
                token_list.button_dict = token_dict
            if self.tokenCount == 0:
                destroy(token_list)
            if len(token_dict) <= 0:
                destroy(token_list)

        token_dict = {}
        for token_type in target.tokens.keys():
            if target.get_tokens(token_type) > 0:
                token_dict[token_type] = Func(decrement_tokens, token_type)
        print(token_dict)
        if len(token_dict) <= 0:
            FadingText("No Tokens to remove", targetHex, color.red)
            return
        token_list = ButtonList(token_dict, font='VeraMono.ttf', button_height=1.5, popup=0, clear_selected_on_enable=False)
        UI.game_map.targeting = None 
        die.consume()