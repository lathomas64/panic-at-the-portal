from ursina import *
from grid import Map
from character import Character, AICharacter
from ursina.prefabs.splash_screen import SplashScreen
import linecache
import os
import tracemalloc
#trying to put everything sofar together

def make_dummy(x,y):
    dummy = AICharacter("faceless_character.png", "dummy")
    dummy.parent = Map.get_map()[x,y]
    dummy.play_animation("walk_left")
    dummy.default_animation = "walk_left"
    dummy.state = dummy.fight
    map.turns.append(dummy)

def display_top(snapshot, key_type='lineno', limit=3):
    snapshot = snapshot.filter_traces((
        tracemalloc.Filter(False, "<frozen importlib._bootstrap>"),
        tracemalloc.Filter(False, "<unknown>"),
    ))
    top_stats = snapshot.statistics(key_type)

    print("Top %s lines" % limit)
    for index, stat in enumerate(top_stats[:limit], 1):
        frame = stat.traceback[0]
        # replace "/path/to/module/file.py" with "module/file.py"
        filename = os.sep.join(frame.filename.split(os.sep)[-2:])
        print("#%s: %s:%s: %.1f KiB"
              % (index, filename, frame.lineno, stat.size / 1024))
        line = linecache.getline(frame.filename, frame.lineno).strip()
        if line:
            print('    %s' % line)

    other = top_stats[limit:]
    if other:
        size = sum(stat.size for stat in other)
        print("%s other: %.1f KiB" % (len(other), size / 1024))
    total = sum(stat.size for stat in top_stats)
    print("Total allocated size: %.1f KiB" % (total / 1024))

def input(key):
    if key == "p":
        snapshot = tracemalloc.take_snapshot()
        display_top(snapshot)   
if __name__ == "__main__":
    tracemalloc.start()
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