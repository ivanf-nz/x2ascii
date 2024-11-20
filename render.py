import tkinter as tk
import numpy as np

#TODO:
    #load objs instead of creating arrays
        #clean objs

    #figure out how to print faces - DONE
    # how to detect if a face is visible or not - z depth filtering
    #add lighting to the faces depending on angle to a source of light (above)
    #convert each face to an ascii image? 
    #make it copy and pastable 
    #
    #optimise the drawing of points (doubling on making points and edges which is inefficient)
    #make rotation a slider that can speed up and slow down
    

# projects a 3d point onto a 2d surface (your screen)
def project(point):
    x = point[0]
    y = point[1]
    z = point[2]
    px = WindowSizeX/2 + ((x*FOV)/(FOV+z)) * 50
    py =  WindowSizeY/2 + ((y*FOV)/(FOV+z)) * 50
    return px, py
# draws the projected 3d point onto a 2d surface
def projectpoint(px,py):
    canvas.create_oval(px - size, py - size, px + size, py + size, fill="white", outline="white")

# draws the projected 3d edge onto a 2d surface
def projectedge(edge):
    px1,py1 = project(points[edge[0]]) #edge has the point number ex (1,5) there is an edge between points 1 and 5 
    px2,py2 = project(points[edge[1]]) 
    canvas.create_line(px1,py1,px2,py2,fill = "white")

def projectface(face):
    facepoints = []
    for i in range(len(face)):
        px,py = project(points[face[i]])
        facepoints.append((px,py)) #creates an array of points for that face
        canvas.create_polygon(facepoints, fill="white", outline="white") 


def rotateY(points):
    y_rotation_matrix = np.array([
            [1, 0, 0],
            [0, np.cos(angle), -np.sin(angle)],
            [0, np.sin(angle), np.cos(angle)]])
    points = points @ y_rotation_matrix.T # @ is matrix multiplication with T being its transpose
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
    global points
    canvas.delete("all")
    for point in points:
        px, py = project(point)
        projectpoint(px,py)

    for edge in edges:
        projectedge(edge)
    for face in faces:
        projectface(face)
    rotate_all()

    root.after(TIMEDELAY,drawscene)

def rotate_all():
    global points
    points = rotateX(rotateY(points)) #could make more efficient by matrix multiplying the 
                                               #rotation matrixes and then matrix multipy with transposing the points array


# Setup Tkinter
root = tk.Tk()
root.title("Render Screen")
root.geometry("400x300")
root.configure(bg="black")
canvas = tk.Canvas(root, width=400, height=300, bg="black")
canvas.pack()

# Variables and constants
FOV = 10 # This is distance to the center of the screen - https://www.youtube.com/watch?v=nvWDgBGcAIM&ab_channel=GraverDev
TIMEDELAY = 16  # for drawing the scene in milliseconds (16 ms is 60 fps)
WindowSizeY = 300
WindowSizeX = 400
angle = np.radians(1)
size = 2 #size of points in terms of a circles bounding box
#preprocess_obj("cube.obj", "cube_cleaned.obj")

def load_shape(shape):
    shapes = {
        "cube": (
            np.array([[-0.5, -0.5, -0.5], [0.5, -0.5, -0.5], [0.5, 0.5, -0.5], [-0.5, 0.5, -0.5],
                      [-0.5, -0.5, 0.5], [0.5, -0.5, 0.5], [0.5, 0.5, 0.5], [-0.5, 0.5, 0.5]]),
            [[0, 1], [1, 2], [2, 3], [3, 0], [4, 5], [5, 6], [6, 7], [7, 4], [0, 4], [1, 5], [2, 6], [3, 7]],
            [[0, 1, 2, 3], [4, 5, 6, 7], [0, 4, 7, 3], [1, 5, 6, 2], [3, 2, 6, 7], [0, 1, 5, 4]]
        ),
        "pyramid": (
            np.array([[-0.5, -0.5, 0], [0.5, -0.5, 0], [0.5, 0.5, 0], [-0.5, 0.5, 0], [0, 0, 1]]),
            [[0, 1], [1, 2], [2, 3], [3, 0], [0, 4], [1, 4], [2, 4], [3, 4]],
            [[0, 1, 2, 3], [0, 1, 4], [1, 2, 4], [2, 3, 4], [3, 0, 4]]
        ),
        "tetrahedron": (
            np.array([[0, 0, 0], [1, 0, 0], [0.5, np.sqrt(3)/2, 0], [0.5, np.sqrt(3)/6, np.sqrt(2/3)]]),
            [[0, 1], [1, 2], [2, 0], [0, 3], [1, 3], [2, 3]],
            [[0, 1, 2], [0, 1, 3], [1, 2, 3], [2, 0, 3]]
        )
    }
    return shapes.get(shape.lower()) or ValueError(f"Shape '{shape}' is not defined.")

# Example usage
shape_name = "tetrahedron"  # Change to "pyramid" or "tetrahedron"
points, edges,faces = load_shape(shape_name)

drawscene()

root.mainloop()