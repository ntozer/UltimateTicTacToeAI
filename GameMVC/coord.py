class Coord(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        if isinstance(other, Coord):
            return (self.x, self.y) == (other.x, other.y)
        return False
