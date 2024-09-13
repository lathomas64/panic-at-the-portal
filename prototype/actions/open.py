from prototype.actions.action import Action
from prototype.hud import UI
from prototype.fading_text import FadingText
from ursina import color

class OpenAction(Action):
    def __init__(self, actor):
        super().__init__("1+", 
               "Open the Path", 
               """
               Destroy one Obstacle within range.
               4+: Also destroy Obstacles adjacent to it.
               8+: Also destroy Obstacles adjacent to those.
               """,
               actor)

    def confirm_targets(self, actor, die, target_hex):
        if target_hex.obstacle == None:
            FadingText("No Obstacles here", target_hex, color.red)
            return 
        radius = 0
        if die.value >= 8:
            radius = 2
        elif die.value >= 4:
            radius = 1
        target_hex.clear_obstacles(radius)
        UI.game_map.targeting = None
        die.consume() 
    