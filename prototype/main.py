from ursina import *
from character import Character, AICharacter
from ursina.prefabs.splash_screen import SplashScreen
from actions.actor import Actor
from hud import ui
#trying to put everything sofar together

def make_dummy(x,y):
    dummy = AICharacter("faceless_character.png", "dummy")
    dummy.parent = ui.map[x,y]
    dummy.play_animation("walk_left")
    dummy.default_animation = "walk_left"
    dummy.state = dummy.fight
    ui.map.turns.append(dummy)
    hex = ui.map[x,y]
    print(hex.children)

if __name__ == "__main__":
    player = Character(name="player")
    player.parent = ui.map[(0,0)]
    ui.map.turns = [player]
    ui.map.explore_hex(2,0)
    a = Animation("fire",fps=8, parent=ui.map[(2,0)])
    ui.map.explore_hex(4,0)
    make_dummy(4,0)
    #make_dummy(0,0)
    ui.map.explore_hex(-2,2)
    make_dummy(-2,2)
    print("before advance turn", ui.map.current_character)
    ui.map.advance_turn()
    print("after advance turn", ui.map.current_character)
    #window.fullscreen = True
    splash = SplashScreen()
    Sprite("background", z=1)

    print("is Character an actor?", issubclass(Character, Actor))
  
    ui.run()