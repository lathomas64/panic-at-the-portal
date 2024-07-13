from ursina import *
from grid import Hex
from character import Character
from die import Die
#trying to put everything sofar together

if __name__ == "__main__":
    app = Ursina()
    Hex.create_map(3)
    player = Character()
    player.parent = Hex.map[(0,0)]
    Hex.current_character = player
    player.start_turn()
    #window.fullscreen = True
    for index in range(len(player.actions)):
        #action = Button(scale=(.3, .1), x = window.top_left.x+.170, y=.3, text=str(player.actions[index]))
        #action.on_click = lambda : Hex.current_character.take_action(player.actions[index])
        
        print(index, player.actions[index])
    app.run()