from compas.geometry import matrix_from_frame
from compas.geometry import Frame
import numpy as np

frame = Frame([6, 5, 0], [1, 0, 0], [0, 1, 0])
m = matrix_from_frame(frame)
nm = np.array(m)

pt = np.array([1, 2, 0, 1])

# correct output dimension but wrong result!
print(np.dot(pt, nm))
# print(np.multiply(pt, nm))

# a = np.arange(12).reshape(3,4)
# b = np.arange(-4,8).reshape(3,4)
# c = np.ones(12).reshape(3,4)

# print(np.minimum.reduce([a,b,c]))

# print(np.asarray([a,b,c]).min(axis=0))