import laspy as lp
import gc
import time
import datetime
import numpy as np
import matplotlib.pyplot as plt
import matplotlib

start_time = time.time()
points_arr = []
colors_arr = []
for i in range(0,2):
    #j = (i == 19) * 983 + (i < 19) * ((i+1) % 10) * 100
    file = "/Users/danieleligato/Desktop/Thesis/point_projection/LAS/202107280658_Un_F_0+"+str(i)+"00_0+"+str(i+1)+"00.las"
    #print("Reading " + file)
    point_cloud_i = lp.read(file)
    points_i = np.vstack((point_cloud_i.x, point_cloud_i.y, point_cloud_i.z)).transpose()
    colors_i = np.vstack((point_cloud_i.red, point_cloud_i.green, point_cloud_i.blue)).transpose()
    points_i = points_i[0::20]
    colors_i = colors_i[0::20]
    del point_cloud_i
    points_arr.extend(points_i)
    colors_arr.extend(colors_i)
    gc.collect()

points_arr = np.array(points_arr)
colors_arr = np.array(colors_arr)/65535
print("Done in " + str(time.time() - start_time) + " sec.")


fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.scatter(points_arr[0::1000], c=colors_arr[0::1], marker='o')

'''import pptk
v = pptk.viewer(points_arr[0::1], colors_arr[0::1]/65535.)
v.set(point_size=0.1)
'''