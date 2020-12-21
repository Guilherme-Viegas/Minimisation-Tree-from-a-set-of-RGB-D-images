import cv2
import sys
import scipy.io
import numpy as np
from image_relations import *
import os

def display_image(line_number):
    file1 = open('output.txt', 'r') 
    count = 0
    
    while True:     
        # Get next line from file 
        line = file1.readline() 
    
        # if line is empty 
        # end of file is reached 
        if not line: 
            break
        
        if(count == line_number):
            break

        count += 1
    
    values = line.split()

    # print(values)
    # print(len(values))
    # print("\n\n")

    R = []
    T = []
    row_number = 0
    column_number = 1
    temp = []
    for val in values:
        if row_number == 3:
            R.append(temp.copy())
            temp.clear()
            row_number = 0
        temp.append(float(val))
        row_number += 1
    
    # print(R)

    T_String = values[-3:]
    T = []
    for val in T_String:
        T.append(float(val))

    
    # print(T)
        
    
    file1.close()

    return np.array(R),np.array(T).reshape(3,1)

# rgbimgs.txt
with open(sys.argv[1], 'r') as file:

    rgbimgs = []
    for img in file.readlines():
        rgbimgs.append( cv2.imread("./"+img.strip("\n"), cv2.IMREAD_COLOR)) if img.split('.')[-1].strip("\n") != 'mat' else rgbimgs.append(scipy.io.loadmat(img.strip("\n"))["depth_array"] )

# depthimgs.txt
with open(sys.argv[2], 'r') as file:

    depthimgs = []
    for img in file.readlines():
        depthimgs.append( cv2.imread("./"+img.strip("\n"), cv2.IMREAD_GRAYSCALE)) if img.split('.')[-1].strip("\n") != 'mat' else depthimgs.append(scipy.io.loadmat(img.strip("\n"))["depth_array"] )

# cameracalib.txt
with open(sys.argv[3], 'r') as calib:

    k_rgb = np.fromfile(calib, dtype=float, sep=' ', count=9).reshape((3,3))
    k_depth = np.fromfile(calib, dtype=float, sep=' ', count=9).reshape((3,3))
    r_depth2rgb = np.fromfile(calib, dtype=float, sep=' ', count=9).reshape((3,3))
    t_depth2rgb = np.fromfile(calib, dtype=float, sep=' ', count=3).reshape((3,1))


# transforms.txt
with open(sys.argv[4], 'r') as file:
    
    path_file_name_output = file.readline()

i = 20

rigid_transformation = lambda r, t, pc: r@pc + t
depth_pc_2_rgb_pc = lambda xyz: np.concatenate( (r_depth2rgb, t_depth2rgb), axis=1)@np.concatenate( (xyz, np.ones((1, xyz.shape[1]), dtype=float) ), axis=0 )



pc_rgb2 = depth_pc_2_rgb_pc( generate_depth_pc(depthimgs[i+1], k_depth) )

r,t = display_image(i)

# pc_generated = rigid_transformation(r, t, pc_rgb2)

# rgb_pc_to_rgb_img(pc_generated, k_rgb, rgbimgs[0])


from scipy.spatial import distance

r_1,t_1 = display_image(5)

for i in range(len(rgbimgs)-1):
    r_2,t_2 = display_image(i)
    print(distance.euclidean(np.concatenate( (r_1, t_1.T), axis=0).flatten() , np.concatenate( (r_2, t_2.T), axis=0).flatten() ))


# from sklearn.metrics.pairwise import cosine_similarity

# r_1,t_1 = display_image(0)
# r_2,t_2 = display_image(1)

# print(cosine_similarity(np.concatenate( (r_1, t_1.T), axis=0) , np.concatenate( (r_2, t_2.T), axis=0) ))

