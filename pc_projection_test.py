import math
import sys
#sys.path.append('../../../../../configs')
#from odt_configs import *
import pandas as pd
import numpy as np
import cv2
import las_reader
import matplotlib.pyplot as plt
from point_projection import PointProjection
import open3d as o3d
from math import atan2, degrees, radians
from scipy.spatial.transform import Rotation as R

def angle(v1, v2, acute):
# v1 is your firsr vector
# v2 is your second vector
    angle = np.arccos(np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2)))
    if (acute == True):
        return angle
    else:
        return 2 * np.pi - angle

def shift_coords(fotogramma_n):

    points_las_shift = pd.DataFrame(columns=['X','Y','Z'])
    las_reader.set_n(las_file)
    points_las = las_reader.return_points()
    points_las_df = pd.DataFrame(points_las, columns = ['X','Y','Z'])
    
    camera = "/Users/danieleligato/Desktop/Thesis/Data/Processed/Ladybug0_1.ori.txt"
    camera_data = pd.read_csv(camera, header=None, delimiter=r"\s+")
    camera_arr = camera_data.to_numpy()
   # curret_frame = pd.DataFrame(columns=['X','Y','Z', 'Heading','Roll', 'Pitch'])
    curret_frame = camera_arr[fotogramma_n][:]#  NF, X, Y, Z, Heading , Roll, pitch
    if(fotogramma_n >= 2):
        previous_frame = camera_arr[fotogramma_n-1][:]

        # Miei radianti = formula(frame_macchina[1] - Frame_macchina[2])
    myradians = math.atan2(float(previous_frame[1]) - float(curret_frame[1]),float(previous_frame[2]) - float(curret_frame[2]))  # boh
    mydegrees = degrees(myradians)  # ci vuole 0 per il frame 50 (170 in termini assoluti)
    print("La mia rotazione rispetto il punto iniziale " + str(mydegrees))


    #Coordinate relative = coordinate assolute nuvola - coordinate assolute macchina
    points_las_shift['X'] = (points_las_df['X'][:] - float(curret_frame[1])) #lato
    points_las_shift['Y'] = (points_las_df['Y'][:] - float(curret_frame[2])) #profondità
    points_las_shift['Z'] = (points_las_df['Z'][:] - float(curret_frame[3])) #altezza

    print("Previous frame")
    print(previous_frame[0], previous_frame[1], previous_frame[2], previous_frame[3])
    print("Current frame")
    print(curret_frame[0],curret_frame[1],curret_frame[2], curret_frame[3])

    df = points_las_shift.to_numpy()


    rotation_degrees = float(mydegrees) #MAYBEMAYBE
    rotation_radians = np.radians(rotation_degrees)
    rotation_axis = np.array([0, 0, 1])

    rotation_vector = rotation_radians * rotation_axis
    rotation = R.from_rotvec(rotation_vector)
    #Punti ruotati = rotazione.apply(Coordinate relative)
    rotated_df = rotation.apply(df)

    return rotated_df


def find_las(fotogramma):
    fotogramma_n = fotogramma
    las_file = 0
    if(fotogramma_n < 50):
        las_file = 0
    else:
        las_file = int(fotogramma_n/50)
    print("Las file: " + str(las_file),"Fotogramma: "+str(fotogramma_n))
    return las_file,fotogramma_n

if __name__ == "__main__":
    n_fotogrammi = 1

    #for i in range(n_fotogrammi):
     #   las_file,fotogramma_n = find_las(i+1)

    las_file, fotogramma_n = find_las(500) #minimum 2 , inserisci il numero del tuo fotogramma

    IMG_FILE = "./Cam1/202107280658_Rectified_" + str(fotogramma_n) + "_Cam1.jpg"

    tal = PointProjection()
    points_las_shift = shift_coords(fotogramma_n)
    
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(points_las_shift[:, 0], points_las_shift[:, 1], points_las_shift[:, 2], marker='o')
    points = np.asarray(points_las_shift)
    res = tal.project_pointcloud_to_image(np.array(points))

    cv2.namedWindow("frame", cv2.WINDOW_NORMAL)

    frame = cv2.imread(IMG_FILE)
    
    for i in range(0, len(res), 1):
        #if points[i][0] > 0 and points[i][1] < 0: #fatto con marzia per eliminare i punti nel cielo
        cv2.circle(frame, (int(res[i][0]), int(res[i][1])), 1, (0, 0, 255), -1)
            #print ("original 3D points: "+str(points[i])+" projected 2D points: ["+str(int(res[i][0]))+" , "+str(int(res[i][1]))+"]" )

    cv2.imshow("frame", frame)
    cv2.waitKey(0)

    print(list(points))
