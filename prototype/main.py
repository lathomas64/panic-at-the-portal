from ursina import *
from grid import Map
from hud import Hud
from character import Character, AICharacter
from ursina.prefabs.splash_screen import SplashScreen
from actions.actor import Actor
#trying to put everything sofar together

def make_dummy(x,y):
    dummy = AICharacter("faceless_character.png", "dummy")
    dummy.parent = Map.get_map()[x,y]
    dummy.play_animation("walk_left")
    dummy.default_animation = "walk_left"
    dummy.state = dummy.fight
    map.turns.append(dummy)
    hex = Map.get_map()[x,y]
    print(hex.children)

if __name__ == "__main__":
    app = Ursina()
    ui = Hud()
    map = Map.create_map(5)
    player = Character(name="player")
    player.parent = map[(0,0)]
    map.turns = [player]
    map.explore_hex(2,0)
    a = Animation("fire",fps=8, parent=map[(2,0)])
    map.explore_hex(4,0)
    make_dummy(4,0)
    #make_dummy(0,0)
    map.explore_hex(-2,2)
    make_dummy(-2,2)
    print("before advance turn", map.current_character)
    map.advance_turn()
    print("after advance turn", map.current_character)
    #window.fullscreen = True
    splash = SplashScreen()
    Sprite("background", z=1)

    print("is Character an actor?", issubclass(Character, Actor))
  
    app.run()