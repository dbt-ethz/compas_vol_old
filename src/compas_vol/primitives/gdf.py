from compas.geometry import Vector

class GDF(object):
    """
    generalised distance function for euclidean polyhedra
    """
    va = 0.577
    vb = 0.357
    vc = 0.943
    vd = 0.851
    ve = 0.526

    gdfvecs = []
    gdfvecs.append(Vector(1,0,0))
    gdfvecs.append(Vector(0,1,0))
    gdfvecs.append(Vector(0,0,1))

    gdfvecs.append(Vector( va, va, va))
    gdfvecs.append(Vector(-va, va, va))
    gdfvecs.append(Vector( va,-va, va))
    gdfvecs.append(Vector( va, va,-va))

    gdfvecs.append(Vector(  0, vb, vc))
    gdfvecs.append(Vector(  0,-vb, vc))
    gdfvecs.append(Vector( vc,  0, vb))
    gdfvecs.append(Vector(-vc,  0, vb))
    gdfvecs.append(Vector( vb, vc,  0))
    gdfvecs.append(Vector(-vb, vc,  0))

    gdfvecs.append(Vector(  0, vd, ve))
    gdfvecs.append(Vector(  0,-vd, ve))
    gdfvecs.append(Vector( ve,  0, vd))
    gdfvecs.append(Vector(-ve,  0, vd))
    gdfvecs.append(Vector( vd, ve,  0))
    gdfvecs.append(Vector(-vd, ve,  0))

    gdfvecs.append(Vector(0,0,1))
    gdfvecs.append(Vector( 0.943,0,     -0.333))
    gdfvecs.append(Vector(-0.471, 0.816,-0.333))
    gdfvecs.append(Vector(-0.471,-0.816,-0.333))

    for v in gdfvecs:
        v.unitize()
    
    ranges = {}
    ranges['octahedron']   = ( 3, 6)
    ranges['dodacehedron'] = (13,18)
    ranges['icosahedron']  = ( 3,12)
    ranges['truncated_octahedron'] = (0,6)
    ranges['truncated_icosahedron'] = (0,6)

    def __init__(self):
        pass
    
    # ==========================================================================
    # distance function
    # ==========================================================================

    def get_distance(self,x,y,z):
        return self.gdfvecs[0]
    
# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":
    gdf = GDF()
    print(gdf.get_distance(1,2,3))