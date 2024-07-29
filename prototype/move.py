from ursina import *
from grid import Hex
from character import Character
from ursina.prefabs.splash_screen import SplashScreen
#trying to put everything sofar together

def make_dummy(x,y):
    dummy = Character("faceless_character.png", "dummy")
    dummy.parent = Hex.map[x,y]
    dummy.play_animation("walk_left")
    dummy.default_animation = "walk_left"
    Hex.turns.append(dummy)

if __name__ == "__main__":
    app = Ursina()
    Hex.create_map(5)
    player = Character(name="player")
    player.parent = Hex.map[(-4,0)]
    Hex.turns = [player]

    make_dummy(4,0)
    make_dummy(0,0)
    make_dummy(-2,2)
    Hex.advance_turn()
    #window.fullscreen = True
    splash = SplashScreen()
    Sprite("background", z=1)
    app.run()