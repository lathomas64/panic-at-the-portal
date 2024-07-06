from ursina import *

app = Ursina()

left_margin = .1

for index in range(4):
    die = Entity(model="quad", texture=load_texture("d4.png"), parent=camera.ui, scale=.075)
    die.x = window.top_left.x + (.5 + left_margin + index + left_margin*index) * .075
    die.y = 6 * die.scale.y
    die_value = Text(text="4", parent=die, color=color.white, z=-1, scale=10)
    die_value.x = -1 * (die_value.scale.x * die_value.width) / 2

app.run()