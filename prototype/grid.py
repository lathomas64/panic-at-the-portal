from ursina import *

app = Ursina()

class Hex(Entity):
    directions = {
        "northeast":(0,1),
        "east" : (1,0),
        "southeast" : (1,-1),
        "northwest" : (-1,1),
        "west" : (-1,0),
        "southwest" : (0,-1)
    }

    def __init__(self, q,r, **kwargs):
        self.q = q
        self.r = r
        x_offset = q  + r/2
        y_offset = r * .75
        print(kwargs)
        super().__init__(x=x_offset, y=y_offset, model='quad', texture=load_texture("hexbordered.png"), kwargs=kwargs)
    @classmethod
    def create_map(cls, radius):
        result = {}
        for q in range(-radius, radius+1):
            for r in range(-radius, radius+1):
                if abs(q+r) <=radius:
                    hex = Hex(q,r)
                    result[(q,r)] = hex
        return result

my_map = Hex.create_map(3)

print(my_map[(1,1)])


app.run()