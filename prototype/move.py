from ursina import *
from grid import Map
from character import Character, AICharacter
from ursina.prefabs.splash_screen import SplashScreen
#trying to put everything sofar together

def make_dummy(x,y):
    dummy = AICharacter("faceless_character.png", "dummy")
    dummy.parent = Map.get_map()[x,y]
    dummy.play_animation("walk_left")
    dummy.default_animation = "walk_left"
    map.turns.append(dummy)

if __name__ == "__main__":
    app = Ursina()
    map = Map.create_map(5)
    player = Character(name="player")
    player.parent = map[(-4,0)]
    map.turns = [player]

    make_dummy(4,0)
    make_dummy(0,0)
    make_dummy(-2,2)
    print("before advance turn", map.current_character)
    map.advance_turn()
    print("after advance turn", map.current_character)
    #window.fullscreen = True
    splash = SplashScreen()
    Sprite("background", z=1)
    app.run()