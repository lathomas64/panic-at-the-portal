from ursina import *
from grid import Hex
from character import Character
from ursina.prefabs.splash_screen import SplashScreen
#trying to put everything sofar together

if __name__ == "__main__":
    app = Ursina()
    Hex.create_map(5)
    player = Character(name="player")
    player.parent = Hex.map[(-4,0)]
    dummy = Character("faceless_character.png", "dummy")
    dummy.parent = Hex.map[4,-1]
    dummy.play_animation("walk_left")
    Hex.turns = [player, dummy]
    Hex.advance_turn()
    #window.fullscreen = True
    splash = SplashScreen()
    Sprite("background", z=1)
    app.run()