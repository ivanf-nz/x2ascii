#import tkinter as tk
import numpy as np
from obj_parser import get_obj
import cv2
import time
#######################################################################
#                                                                     #
#                   3D MODEL ASCII VIEWER                             #
#                                                                     #
# X positive is defined as going to the right                         #
# Y positive is defined as up and down                                #
# Z positive is defined as going towards the viewer, out of the screen#
#######################################################################

# TODO:
#remove the gui(tkinter) and instead have options (python parameters)
#  
#make options for loading objs, moving them by 0.5 or 1 (points array)
#option for disabling black outline between edges

#rotation to add a input of degree

# make it copy and pastable kinda already done but could be improved (button outputs a ascii file)
# improve the comments
#rotate camera - not the cube (how?)



#######################################################################

# projects a 3d point onto a 2d surface (your screen)
def project(point):
    x = point[0]
    y = point[1]
    z = point[2]
    px = horizontalshift/2 + ((x*FOV)/(FOV+z)) * distance
    py = verticalshift/2 + ((y*FOV)/(FOV+z)) * distance
    return px, py


# determines the lighting intensity of a face compared to the light position (assuming light is pointing at object at all times)
# returns a value from 0 to 1 where 0 means lit and 1 means unlight (because of how white = nothing printing in ascii and so 0 = black)
def lighting_intensity(face):
    normal = compute_normal(face)
    face_point = points[face[0]]  # any point on the face
    #light_vector = light_pos - face_point # this is a vector from point on face to light and so in same direction as normal
    light_vector = face_point - light_pos
    normal = normal / np.linalg.norm(normal) # normalize to length of 1
    light_vector = light_vector / np.linalg.norm(light_vector) #normalized to ensure in range from 0 to 1

    #dot product means that 1 = same direction, 0 = 90 degrees to each other and -1 is opposite direction
    intensity = 1-max(0.1,np.dot(light_vector ,normal))  #changed with 1- (1 minus) to have black bg for ascii 
    #intensity = max(0.1,np.dot(light_vector ,normal)) #1 means lit, 0 means not lit
    return intensity

#draws the faces with light values included
# black = lit, white = unlit 

def drawface(face, intensity):
    global grid

    facepoints = []
    for i in range(len(face)):
        px, py = project(points[face[i]])
        facepoints.append((px, py))  # creates an array of points for that face
        
    colour_value = int(intensity*255) #255 = white, 0 = black 
    facepoints = np.array(facepoints, dtype=np.int32)
    cv2.fillPoly(grid, [facepoints], color=colour_value)

    #need to add option for drawing edges
    #for i in range(len(face)-1): #draws the edges
        #drawedge(points[face[i]],points[face[i + 1]])
    #drawedge(points[face[0]],points[face[(len(face)-1)]]) #loops back from the end point to the start point - if not here will have missing edges

# computes the normal of a face. used in determining if a face is visible and used in lighting calculations
def compute_normal(face):
    p1, p2, p3 = points[face[0]], points[face[1]], points[face[2]]
    edge1 = p2 - p1
    edge2 = p3 - p1
    normal = np.cross(edge1, edge2)  # cross product
    return (normal / np.linalg.norm(normal))  # Normalize to length of 1 and invert with negative sign (ccw->cw direction)

def is_face_visible(face):
    normal = compute_normal(face)
    face_point = points[face[0]]  # any point on the face
    view_vector = camera_pos - face_point # from face point to camera pos
    return np.dot(view_vector, normal) < 0  # true if the face is visible

#rotates the whole array by the given angle and using matrix multiplication
def rotateY(points, frame_angle): # Add frame_angle parameter
    y_rotation_matrix = np.array([
        [1, 0, 0],
        [0, np.cos(frame_angle), -np.sin(frame_angle)], 
        [0, np.sin(frame_angle), np.cos(frame_angle)]]) 
    # @ is matrix multiplication with T being its transpose
    points = points @ y_rotation_matrix.T
    return points

def rotateX(points, frame_angle): # Add frame_angle parameter
    x_rotation_matrix = np.array([
        [np.cos(frame_angle), 0, np.sin(frame_angle)], 
        [0, 1, 0],
        [-np.sin(frame_angle), 0, np.cos(frame_angle)]]) 
    points = points @ x_rotation_matrix.T
    return points

def rotateZ(points, frame_angle): # Add frame_angle parameter
    z_rotation_matrix = np.array([
        [np.cos(frame_angle), -np.sin(frame_angle), 0], 
        [np.sin(frame_angle), np.cos(frame_angle), 0], 
        [0, 0, 1]])
    points = points @ z_rotation_matrix.T
    return points

def print_ascii(im, new_width):
    width, height = WindowSizeX, WindowSizeY
    new_height = int(height/width * new_width *0.5)
    im = cv2.resize(im,(new_width, new_height))
    
    #ascii define white to black
    ascii_string = ""
    #opens the text file - to be added later
    #f = open("outputascii.txt","w")

    #goes thorugh each pixel
    for i in range(new_height):
        
        for j in range(new_width):

            #gets pixel value
            pixel = im[i,j]

            #make each pixel an ascii char 0(black)-255(white)
            ascii_string += str(ascii_chars[int(pixel/255*(len(ascii_chars)-1))]) 

        ascii_string += "\n" #combine this with the line above
    print(f"\r{ascii_string}",end="",flush=True) #ensure clean output using Carriage Return 

def sort_faces_by_distance(faces):
    centroids = [np.mean(points[face], axis=0) for face in faces]
    distances = [np.linalg.norm(camera_pos - centroid) for centroid in centroids]
    sorted_faces = sorted(zip(faces, distances),key=lambda x: x[1],) #put reverse=True for really trippy ghost effect
    # sorted from furthest to closest
    return [face for face, _ in sorted_faces]
def drawscene(dt):
    global grid
    grid = np.full((WindowSizeY,WindowSizeX),255, dtype=np.uint8) #255 to set background to white
    sorted_faces = sort_faces_by_distance(faces)
    for face in sorted_faces:
        if is_face_visible(face):
            intensity = lighting_intensity(face)
            drawface(face, intensity)
    
    rotate_all(dt)

    try: #printing to screen hasnt been fixed and can cause errors as the canvas is being created
        print_ascii(grid,70)
    except Exception as e:
        print(f"An error occurred: {e}")
    

#rotates the scene 
def rotate_all(dt):
    global points
    frame_rotation_angle = np.radians(ROTATION_DEGREES_PER_SECOND * dt)
    # could make more efficient by matrix multiplying the rotation matrixes and then matrix multipy with transposing the points array
    #points = rotateZ(rotateX(points))
    points = rotateX(points, frame_rotation_angle)



# setup canvas size for rendering object
WindowSizeY = 300
WindowSizeX = 400
#rasterize settings
grid = np.full((WindowSizeY,WindowSizeX),255, dtype=np.uint8) #(height,width)
ascii_chars = "@%#*+=-:. "

#default values for sliders
angle = np.radians(1)
distance = 50
horizontalshift = WindowSizeX
verticalshift = WindowSizeY 

# Variables and constants
#fov lower than 100 used to cause problems rendering ?
FOV = 100  # this is distance to the center of the screen - https://www.youtube.com/watch?v=nvWDgBGcAIM&ab_channel=GraverDev
camera_pos = np.array([0, 0, 100])
TIMEDELAY = 16  # for drawing the scene in milliseconds (16 ms is 60 fps)
size = 2  # size of edges

ROTATION_DEGREES_PER_SECOND = 45

light_pos = np.array([0,10,3]) #placed above in y direction (x,y,z)

obj = "../models/cube2.obj" #https://www.a1k0n.net/2011/07/20/donut-math.html website might help with lighting
points, faces = get_obj(obj)    
initial_angle_rad = np.radians(1) #rotation angle in radians (needed for rotation functions)
for i in range(180): #added for fox as it is upside down
    points = rotateZ(points, initial_angle_rad)
for i in range(45):
    points = rotateY(points, initial_angle_rad)
for i in range(45):
    points = rotateX(points, initial_angle_rad)

last_frame_time = time.perf_counter()
while True:

    current_time = time.perf_counter()

    #delta time ensures that the rotation speed is constant regardless of the frame rate (remember dt is 1 frame behind!)
    dt = current_time - last_frame_time #delta time 
    last_frame_time = current_time  # update last_frame_time for the next frame
    drawscene(dt)
    time.sleep(TIMEDELAY/1000) #sleep to ensure 60 fps