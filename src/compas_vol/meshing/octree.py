from math import sqrt
from compas.geometry import Point


class Octree(object):
    sq2 = sqrt(2.0)
    sq3 = sqrt(3.0)

    def __init__(self):
        self._p = Point(0, 0, 0)
        self._ws = 100.0  # world size
        self._ml = 4      # max levels
        self._rn = OctNode(0, 0, 0, self._ws, 0)
        self._o = None
    
    def divide(self, node):
        if node.level < self._ml:
            d = self._o.get_distance(node.pos.x, node.pos.y, node.pos.z)
            if abs(d) < Octree.sq3 * node._el/2.0:
                node.divide_node()
                for b in node._branches:
                    self.divide(b)


class OctNode(object):
    def __init__(self, x, y, z, e, l):
        self._p = Point(x, y, z)
        self._el = e
        self._l = l
        self._branches = None
    
    @property
    def level(self):
        return self._l

    @level.setter
    def level(self, l):
        self._l = float(l)
    
    def divide_node(self):
        self._branches = []
        qs = self._el/4.0
        nl = self.level + 1
        self._branches.append(OctNode(self._p.x-qs, self._p.y-qs, self._p.z-qs, qs*2, nl))
        self._branches.append(OctNode(self._p.x+qs, self._p.y-qs, self._p.z-qs, qs*2, nl))
        self._branches.append(OctNode(self._p.x-qs, self._p.y+qs, self._p.z-qs, qs*2, nl))
        self._branches.append(OctNode(self._p.x+qs, self._p.y+qs, self._p.z-qs, qs*2, nl))
        self._branches.append(OctNode(self._p.x-qs, self._p.y-qs, self._p.z+qs, qs*2, nl))
        self._branches.append(OctNode(self._p.x+qs, self._p.y-qs, self._p.z+qs, qs*2, nl))
        self._branches.append(OctNode(self._p.x-qs, self._p.y+qs, self._p.z+qs, qs*2, nl))
        self._branches.append(OctNode(self._p.x+qs, self._p.y+qs, self._p.z+qs, qs*2, nl))


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":
    pass
