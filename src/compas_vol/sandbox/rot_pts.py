import numpy as np
import matplotlib.pyplot as plt


def d(x, y, z, m):
    p = np.array([x, y, z, 1])
    # print(p.shape)
    return np.dot(m, p)

# def e(x, y, m):
#     p = np.array([x, y])
#     np.einsum('j,ij->i', p, m)


if __name__ == "__main__":
    z, y, x = np.ogrid[-1:1:4j, -1:1:5j, -1:1:6j]
    m = np.array([[0.9428, -0.3335], [0.3335, 0.9428]])
    b = np.array([[0.9428, -0.3335,  0.0000,  0.8850],
                  [0.3335,  0.9428,  0.0000,  3.4952],
                  [0.0000,  0.0000,  1.0000,  4.0000],
                  [0.0000,  0.0000,  0.0000,  1.0000]])
    c = np.array([[0.9553, -0.2940,  0.0295,  2.2750],
                  [0.2955,  0.9506, -0.0954,  2.7972],
                  [0.0000,  0.0998,  0.9950,  1.0000],
                  [0.0000,  0.0000,  0.0000,  1.0000]])
    r = d(x, y, z, c)
    plt.scatter(*np.meshgrid(x, y))
    plt.scatter(r[0], r[1])
    plt.axis('equal')
    plt.show()
