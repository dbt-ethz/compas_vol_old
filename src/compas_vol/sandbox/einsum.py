import numpy as np

def myfunc(m):
    return np.einsum('...j,ij->i', m, b)

if __name__ == "__main__":
        
    p = np.array([1, 0, 0, 1])

    pts = np.array([[1, 0, 0, 1],
                    [2, 3, 1, 1],
                    [3, 2, 1, 1],
                    [5, 6, 3, 1],
                    [1, 4, 1, 1]])

    # r = np.array([[0.9428, -0.3335, 0, 0],
    #               [0.3335,  0.9428, 0, 0],
    #               [0, 0, 1, 0],
    #               [0, 0, 0, 1]])

    b = np.array([[0.9428, -0.3335,  0.0000,  0.8850],
                  [0.3335,  0.9428,  0.0000,  3.4952],
                  [0.0000,  0.0000,  1.0000,  4.0000],
                  [0.0000,  0.0000,  0.0000,  1.0000]])

    # print(np.einsum('...j,ij->i', p, b))
    # print(np.einsum('i,j->ij', p, b))

    r = np.apply_along_axis(myfunc, 1, pts)
    print(r)
    print(b.dot(p))
