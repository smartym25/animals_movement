import math
from ntpath import join
import numpy as np 

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from mpl_toolkits.mplot3d import Axes3D

screen = plt.figure(figsize=(8,8))
axes = plt.axes(projection="3d")

height_chassis = 2

attach_joints = np.array([
    [4,2,height_chassis], [8,2, height_chassis],
    [9.5,6, height_chassis], [8,10, height_chassis],
    [4,10, height_chassis], [2.5,6, height_chassis]
])

knee_joints = np.array([
    [1.5,-0.5,2.5], [11.5,-0.5,2.5],
    [12,6,2.5], [11.5,12.5,2.5],
    [1.5,12.5,2.5], [-1,6,2.5] 
])

foot_joints = np.array([
    [0.5,-0.5,0], [12.5,-0.5,0],
    [13,6,0], [12.5,13.5,0],
    [0.5,13.5,0], [-2,6,0]
])

def plot_line(axes, p1, p2, color): 
    axes.plot([p1[0], p2[0]], [p1[1], p2[1]], [p1[2], p2[2]], color=color) 

def plot_tibia(axes, knee, foot, color):
    #the comma transform the upper_leg list directly in the object Line3D
    lower_leg, = axes.plot([knee[0], foot[0]], [knee[1], foot[1]], [knee[2], foot[2]], color= color)
    return lower_leg

def plot_femor(axes,attach,knee,color):
    upper_leg, = axes.plot([attach[0], knee[0]], [attach[1], knee[1]], [attach[2], knee[2]], color= color)
    return upper_leg

#chassis 
for i in range(6):
    plot_line(axes, attach_joints[i], attach_joints[(i+1)%6], color="red")

#legs
femors = []
for i in range(6):
    femor = plot_femor(axes, attach_joints[i], knee_joints[i],color = "blue")
    femors.append(femor)

tibias = []
for i in range(6):
    tibia = plot_tibia(axes, knee_joints[i], foot_joints[i], color = "blue")
    tibias.append(tibia)

coordinates_foots_steps = {
    1: [np.array([0.5, -1.5,0]), np.array([0.5, -1.5,0.5]), np.array([0.5, 4, 0.5]), np.array([0.5, 4, 0])],
    2: [np.array([12,4,0]), np.array([12,4,0.5]), np.array([12,-1.5,0.5]), np.array([12,-1.5,0])],
    3: [np.array([11,5.8,0]), np.array([11,5.8,0.5]), np.array([11, 6.2, 0.5]), np.array([11, 6.2, 0])],
    4: [np.array([12,13,0]), np.array([12,13,0.5]), np.array([12,8,0.5]), np.array([12,8,0])],
    5: [np.array([0.5,8.5,0]), np.array([0.5,8.5,0.5]), np.array([0.5,12.5,0.5]), np.array([0.5,12.5,0])],
    6: [np.array([1,6.2,0]), np.array([1,6.2,0.5]), np.array([1, 5.8, 0.5]), np.array([1, 5.8, 0.5])],
}

L2 = math.sqrt((attach_joints[0][1]-knee_joints[0][1])**2 + (attach_joints[0][2]-knee_joints[0][2])**2) 
L3 = math.sqrt((foot_joints[0][1]-knee_joints[0][1])**2 + (foot_joints[0][2]-knee_joints[0][2])**2)

def update_leg1(frames):
    for i in range(6):
        target_foot = coordinates_foots_steps[i+1][frames % 4]
        
        dx = target_foot[0] - attach_joints[i][0]
        dy = target_foot[1] - attach_joints[i][1]
        dz = target_foot[2] - attach_joints[i][2]
        
        H = math.sqrt( dx**2 + dy**2 )
        
        L = math.sqrt( H**2 + dz**2 )
        
        cos_J3 = np.cos((L3**2 + L2**2 - L**2) / (2*L3*L2))
        J3 = np.arccos(cos_J3)
        
        cos_beta = np.cos((L2**2 + L**2 - L3**2) / (2*L2*L))
        beta = np.arccos(cos_beta)
        
        alfa = np.arctan2(dz, H)
        J2 = beta - alfa
        
        J1 = np.arctan2(dy, dx)
        
        new_x_knee = attach_joints[i][0] + L2 * np.cos(J1) * np.cos(J2)
        new_y_knee = attach_joints[i][1] + L2 * np.sin(J1) * np.cos(J2)
        new_z_knee = 2.5
        
        new_x_foot = target_foot[0] + L3 * np.cos(J1) * np.cos(J3)
        new_y_foot = target_foot[1] + L3 * np.sin(J1) * np.cos(J3)
        new_z_foot = 0 #voglio che si alzi
        
        femors[i].set_data([attach_joints[i][0], new_x_knee], [attach_joints[i][1], new_y_knee])
        femors[i].set_3d_properties([attach_joints[i][2], new_z_knee])
        
        tibias[i].set_data([new_x_knee, new_x_foot], [new_y_knee, new_y_foot])
        tibias[i].set_3d_properties([new_z_knee, new_z_foot])
        
    return femors[i], tibias[i]

#reference line
point1 = np.array([-2, -2.5,0])
point2 = np.array([-2, -2.5,4])

reference_line, = axes.plot(
        [point1[0], point2[0]],
        [point1[1], point2[1]],
        [point1[2], point2[2]],
        color=(0,1,0,0)
)

#impost the animation
ani = FuncAnimation(screen, update_leg1, frames=100, interval=100)
#fit the animation in 3d axis
plt.tight_layout()
#show the results
plt.show()


