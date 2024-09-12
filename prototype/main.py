'''
Main entry point into the game
'''
from ursina import Animation, window, Sprite
from ursina.prefabs.splash_screen import SplashScreen
from character import Character, AICharacter
from stance import Stance
from hud import UI
from archetypes.angel import Angel
from styles.halcyon import HalcyonStyle
from forms.blaster import BlasterForm
#trying to put everything sofar together

def make_dummy(x,y):
    '''
    create enemies at a given location
    '''
    dummy = AICharacter("faceless_character.png", "dummy")
    dummy.parent = UI.game_map[x,y]
    dummy.play_animation("walk_left")
    dummy.default_animation = "walk_left"
    dummy.state = dummy.fight
    UI.game_map.turns.append(dummy)

if __name__ == "__main__":
    player = Character(name="player")
    player.archetype = Angel(player)
    player.stances.append(Stance(HalcyonStyle(player), BlasterForm(player)))
    player.parent = UI.game_map[(0,0)]
    UI.game_map.turns = [player]
    UI.game_map.explore_hex(2,0)
    a = Animation("fire",fps=8, parent=UI.game_map[(2,0)])
    UI.game_map.explore_hex(4,0)
    make_dummy(4,0)
    #make_dummy(0,0)
    UI.game_map.explore_hex(-2,2)
    make_dummy(-2,2)
    print("before advance turn", UI.game_map.current_character)
    UI.game_map.advance_turn()
    print("after advance turn", UI.game_map.current_character)
    window.fullscreen = True
    splash = SplashScreen()
    Sprite("background", z=1)


    UI.run()
    print("\n\ndoes after run happen?\n\n")
    UI.game_active = True
