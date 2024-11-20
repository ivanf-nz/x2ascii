import tkinter as tk
import numpy as np

#TODO:
    #load objs instead of creating arrays
        #clean objs
    #add rotation matrix and make the cube rotate slowly - DONE

    #figure out how to print faces and how to detect if a face is visible or not
    #add lighting to the faces depending on angle to a source of light (above)
    #convert each face to an ascii image? 
    #make it copy and pastable 
    #
    #optimise the drawing of points (doubling on making points and edges which is inefficient)
    
    


#import pywavefront
# def preprocess_obj(input_path, output_path):
#     with open(input_path, 'r') as infile, open(output_path, 'w') as outfile:
#         for line in infile:
#             # Strip inline comments starting with '#'
#             clean_line = line.split('#', 1)[0].strip()
#             if clean_line:  # Write only non-empty lines
#                 outfile.write(clean_line + '\n')

def project(point):
    x = point[0]
    y = point[1]
    z = point[2]
    px = WindowSizeX/2 + ((x*FOV)/(FOV+z)) * 50
    py =  WindowSizeY/2 + ((y*FOV)/(FOV+z)) * 50
    return px, py
def projectpoint(px,py):

    size = 2
    canvas.create_oval(px - size, py - size, px + size, py + size, fill=white, outline=white)

def projectvertex(vertex):
    px1,py1 = project(points[vertex[0]])
    px2,py2 = project(points[vertex[1]]) 
    canvas.create_line(px1,py1,px2,py2,fill = "white")

def rotateY(points):
    y_rotation_matrix = np.array([
            [1, 0, 0],
            [0, np.cos(angle), -np.sin(angle)],
            [0, np.sin(angle), np.cos(angle)]])
    points = points @ y_rotation_matrix.T #@ is matrix multiplication with T beaning its transpose
    return points
def rotateX(points):
    x_rotation_matrix = np.array([
            [np.cos(angle), 0, np.sin(angle)],
            [0, 1, 0],
            [-np.sin(angle), 0, np.cos(angle)]])
    points = points @ x_rotation_matrix.T
    return points

def rotateZ(points):
    z_rotation_matrix = np.array([
        [np.cos(angle), -np.sin(angle), 0],
        [np.sin(angle), np.cos(angle), 0],
        [0, 0, 1]])
    points = points @z_rotation_matrix.T
    return points
def drawscene():
    global angle,points
    canvas.delete("all")
    for point in points:
        px, py = project(point)
        projectpoint(px,py)

#project vertex
    for vertex in vertexs:
        projectvertex(vertex)
    
    rotate_all(angle)

    root.after(timedelay,drawscene)

def rotate_all(angle):
    global points
    points = rotateZ(rotateX(rotateY(points)))


# Setup Tkinter
root = tk.Tk()
root.title("Render Screen")
root.geometry("400x300")
root.configure(bg="black")
canvas = tk.Canvas(root, width=400, height=300, bg="black")
canvas.pack()

# Variables and constants
FOV = 2 # This is distance to the center of the screen - https://www.youtube.com/watch?v=nvWDgBGcAIM&ab_channel=GraverDev




timedelay = 16  # milliseconds
WindowSizeY = 300
WindowSizeX = 400
white = "white"


#preprocess_obj("cube.obj", "cube_cleaned.obj")

#cube points and vertexs 
points = np.array([[0,0,0],[0,1,0],[1,1,0],[1,0,0],[0,0,1],[0,1,1],[1,1,1],[1,0,1]])

#points = [[x - 0.5 for x in sublist] for sublist in points] #subtract 0.5 from every point to put box in the middle
points = points - 0.5

vertexs = np.array([[0,1],[0,3],[0,4],[1,5],[1,2],[5,4],[5,6],[6,2],[6,7],[4,7],[7,3],[2,3]])
angle = np.radians(1)
drawscene()


root.mainloop()