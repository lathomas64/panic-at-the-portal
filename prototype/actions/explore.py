from actions.action import Action
from hud import ui

class ExploreAction(Action):
    def __init__(self, actor):
        super().__init__("1+",
                         "Explore",
                         "Explore what lies beyond visible borders. reveal more hexes at an edge.",
                         actor,
                         range=4)

    def act(self, die):
        ui.map.explore()
        die.consume()
