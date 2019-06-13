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