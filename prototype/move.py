from ursina import *
from grid import Hex
from character import Character
#trying to put everything sofar together

if __name__ == "__main__":
    app = Ursina()
    Hex.create_map(3)
    player = Character()
    player.parent = Hex.map[(0,0)]
    dummy = Character("faceless_character.png")
    dummy.parent = Hex.map[1,0]
    dummy.play_animation("walk_left")
    Hex.current_character = player
    player.start_turn()
    #window.fullscreen = True
    app.run()