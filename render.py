import tkinter as tk
import numpy as np


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
# Setup Tkinter
root = tk.Tk()
root.title("Render Screen")
root.geometry("400x300")
root.configure(bg="black")
canvas = tk.Canvas(root, width=400, height=300, bg="black")
canvas.pack()

# Variables
FOV = 2 # This is distance to the center of the screen - https://www.youtube.com/watch?v=nvWDgBGcAIM&ab_channel=GraverDev
WindowSizeY = 300
WindowSizeX = 400
white = "white"

#preprocess_obj("cube.obj", "cube_cleaned.obj")

#cube points and vertexs 
points = np.array([[0,0,0],[0,1,0],[1,1,0],[1,0,0],[0,0,1],[0,1,1],[1,1,1],[1,0,1]])

#points = [[x - 0.5 for x in sublist] for sublist in points] #subtract 0.5 from every point to put box in the middle
points = points - 0.5

vertexs = np.array([[0,1],[0,3],[0,4],[1,5],[1,2],[5,4],[5,6],[6,2],[6,7],[4,7],[7,3],[2,3]])

#project points
for point in points:
    px, py = project(point)
    projectpoint(px,py)

#project vertex
for vertex in vertexs:
    projectvertex(vertex)

root.mainloop()