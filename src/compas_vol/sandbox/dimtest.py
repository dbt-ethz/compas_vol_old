import numpy as np

num = 8
lb = -15.0
ub =  15.0
fact = (ub-lb)/(num-1)
for i in range(num):
    # y = lb + float(i)/(num-1) * (ub-lb)
    y = lb + i*fact
    print(i, y)

x = np.ogrid[lb:ub:8j]
print(x)
