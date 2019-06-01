class Shell(object):
    """
    creates a shell of thickness d
    side factor s:
        1.0 > inside
        0.5 > half half
        0.0 > outside
    """

    def __init__(self, obj, d=1.0, s=0.0):
        self.o = obj
        self.d = d
        self.s = s

    def get_distance(self,x,y,z):
        do = self.o.get_distance(x,y,z)
        return abs(do + (self.s-0.5)*self.d)-self.d/2.0

if __name__ == "__main__":
    from compas_vol.primitives import Box
    b = Box(3,4,5)
    s = Shell(b, d=0.6, s=0.75)
    d = s.get_distance(2,3,4)
    print(d)