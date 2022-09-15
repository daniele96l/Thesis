import time
import datetime
import numpy as np
import laspy as lp
import gc
import pandas as pd
#import pptk
import open3d as o3d
import numpy as np
import laspy
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import matplotlib
from geopy.distance import geodesic
import geopy
import math
start_time = time.time()
points_arr = []
colors_arr = []
n = 0

def set_n(n_from_pc):
    global n
    n = n_from_pc

def return_points():
    df = pd.DataFrame(columns=['NF','X','Y','Z','Heading','Roll','Pitch','Time'])
    if(n < 9):
        file = "/Users/danieleligato/Desktop/Thesis/point_projection/LAS/202107280658_Un_F_0+"+str(n)+"00_0+"+str(n+1)+"00.las"
    if(n==9):
        file = "/Users/danieleligato/Desktop/Thesis/point_projection/LAS/202107280658_Un_F_0+" + str(n) + "00_1+" + str(0) + "00.las"
    if(n>9):
        file = "/Users/danieleligato/Desktop/Thesis/point_projection/LAS/202107280658_Un_F_1+" + str(n-9) + "00_1+" + str(n+1-9) + "00.las"
    camera = "/Users/danieleligato/Desktop/Thesis/Data/Processed/Ladybug0_1.ori.txt"
    camera_data = pd.read_csv(camera, header=None, delimiter=r"\s+")
    print("1")
    point_cloud_i = lp.read(file)
    points_i = np.vstack((point_cloud_i.x, point_cloud_i.y, point_cloud_i.z)).transpose()
    colors_i = np.vstack((point_cloud_i.red, point_cloud_i.green, point_cloud_i.blue)).transpose()
    campionamento = 50
    points_i = points_i[0::campionamento]
    colors_i = colors_i[0::campionamento]/65535.
    return points_i



"""y = 0
max_d = 100

punto_iniziale = 100 #punto da dove inizia la mia mappa di punti
#da questo punto considererò 40m e poi taglio'''



resticted_points = np.zeros(shape=(y,3))
resticted_points_c = np.zeros(shape=(y,3))
d = 0
j = 0


print("3")
# plotting points
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.scatter(points_i[:,0], points_i[:,1], points_i[:,2], c=colors_i, marker='o')
print("3.5")
#plt.show()
print("4")"""
