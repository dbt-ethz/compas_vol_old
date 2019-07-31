import numpy as np

# rot = np.array([[0.7071, -0.7071,  0.0000,  0.0000],
#                 [0.7071,  0.7071,  0.0000,  0.0000],
#                 [0.0000,  0.0000,  1.0000,  0.0000],
#                 [0.0000,  0.0000,  0.0000,  1.0000]
#                 ])
# X, Y, Z = np.meshgrid(np.linspace(0, 1, 5), np.linspace(0, 1, 5), np.linspace(0, 1, 5), indexing='ij')
# print(Y)
# # X,Y,Z=np.meshgrid([0,1,2],[0,1,2,3],[0,1,2],indexing='ij')
# XYZ = np.array((X, Y, Z, X))
# XYZ2 = np.einsum('ij,jabc->iabc', rot, XYZ)

# X2, Y2, Z2, W = XYZ2
# print(X2)

# 2d case
# x, y = np.meshgrid(xspan, yspan)
# np.einsum('ji, mni -> jmn', RotMatrix, np.dstack([x, y]))

A = np.array([1, 2, 3, 1])

B = np.array([[ 1,  0,  0,  3],
              [ 0,  1,  0,  7],
              [ 0,  0,  1,  5],
              [ 0,  0,  0,  1]])

r = np.einsum('i,ij->i', A, B)
print(r)