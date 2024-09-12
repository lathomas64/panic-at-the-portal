from actions.action import Action
from hud import UI
from fadingText import FadingText
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

    def confirm_targets(self, actor, die, targetHex):
        if targetHex.obstacle == None:
            FadingText("No Obstacles here", targetHex, color.red)
            return 
        radius = 0
        if die.value >= 8:
            radius = 2
        elif die.value >= 4:
            radius = 1
        targetHex.clearObstacles(radius)
        UI.game_map.targeting = None
        die.consume() 
    