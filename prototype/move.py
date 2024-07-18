from ursina import *
from grid import Hex
from character import Character
#trying to put everything sofar together

if __name__ == "__main__":
    app = Ursina()
    Hex.create_map(10)
    player = Character(name="player")
    player.parent = Hex.map[(0,0)]
    dummy = Character("faceless_character.png", "dummy")
    dummy.parent = Hex.map[1,0]
    dummy.play_animation("walk_left")
    Hex.turns = [player, dummy]
    Hex.advance_turn()
    #window.fullscreen = True
    app.run()