from ursina import *
from grid import Hex
from character import Character
#trying to put everything sofar together

if __name__ == "__main__":
    app = Ursina()
    Hex.create_map(3)
    player = Character()
    player.parent = Hex.map[(0,0)]
    Hex.current_character = player
    player.start_turn()
    #window.fullscreen = True
    app.run()