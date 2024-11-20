import tkinter as tk
import numpy as np

# TODO:
# load objs instead of creating arrays
# clean objs

# add lighting to the faces depending on angle to a source of light (above)
# convert each face to an ascii image?
# make it copy and pastable
#
# optimise the drawing of points (doubling on making points and edges which is inefficient)
# make rotation a slider that can speed up and slow down
# need to fix the colouring (probably switch to light source from the sky)
# fix the comments


# projects a 3d point onto a 2d surface (your screen)
def project(point):
    x = point[0]
    y = point[1]
    z = point[2]
    px = WindowSizeX/2 + ((x*FOV)/(FOV+z)) * distance
    py = WindowSizeY/2 + ((y*FOV)/(FOV+z)) * distance
    return px, py
# draws the projected 3d point onto a 2d surface


def drawpoint(px, py):
    canvas.create_oval(px - size, py - size, px + size, py + size, fill="white", outline="white")

# draws the projected 3d edge onto a 2d surface


def drawedge(edge):
    # edge has the point number ex (1,5) there is an edge between points 1 and 5
    px1, py1 = project(points[edge[0]])
    px2, py2 = project(points[edge[1]])
    canvas.create_line(px1, py1, px2, py2, fill="white")


def drawface(face, j):
    facepoints = []
    for i in range(len(face)):
        px, py = project(points[face[i]])
        facepoints.append((px, py))  # creates an array of points for that face
        colour_value = 30+j*30
        colour = f"#{colour_value:02x}{colour_value:02x}{colour_value:02x}"  # hex convert
        canvas.create_polygon(facepoints, fill=colour, outline=colour) #further away = lighter, closest = dark


def compute_normal(face):
    p1, p2, p3 = points[face[0]], points[face[1]], points[face[2]]
    edge1 = p2 - p1
    edge2 = p3 - p1
    normal = np.cross(edge1, edge2)  # Cross product
    return normal / np.linalg.norm(normal)  # Normalize to length of 1


def is_face_visible(face):
    normal = compute_normal(face)
    face_point = points[face[0]]  # any point on the face
    view_vector = camera_pos - face_point
    return np.dot(view_vector, normal) < 0  # true if the face is visible


def sort_faces_by_distance(faces):
    centroids = [np.mean(points[face], axis=0) for face in faces]
    distances = [np.linalg.norm(camera_pos - centroid) for centroid in centroids]
    sorted_faces = sorted(zip(faces, distances),key=lambda x: x[1], reverse=True)
    # sorted from furthest to closest
    return [face for face, _ in sorted_faces]


def rotateY(points):
    y_rotation_matrix = np.array([
        [1, 0, 0],
        [0, np.cos(angle), -np.sin(angle)],
        [0, np.sin(angle), np.cos(angle)]])
    # @ is matrix multiplication with T being its transpose
    points = points @ y_rotation_matrix.T
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
    points = points @ z_rotation_matrix.T
    return points


def drawscene():
    global points
    canvas.delete("all")
    # for point in points:
    #     px, py = project(point)
    #     drawpoint(px,py)

    # for edge in edges:
    #     drawedge(edge)
    # for face in faces:
    #     drawface(face)
    sorted_faces = sort_faces_by_distance(faces)
    i = 0
    for face in sorted_faces:
        if is_face_visible(face):
            drawface(face, i)
            i += 1
    rotate_all()

    root.after(TIMEDELAY, drawscene)


def rotate_all():
    global points
    # could make more efficient by matrix multiplying the rotation matrixes and then matrix multipy with transposing the points array
    points = rotateX(rotateY(points))

def update_speed(val):
    global angle
    angle = np.radians(float(val))
def update_distance(val):
    global distance,camera_pos
    distance = int(val)
    camera_pos = np.array([0, 0, FOV+distance])

# Setup Tkinter
root = tk.Tk()
root.title("Render Screen")
root.geometry("700x500")
root.configure(bg="black")
canvas = tk.Canvas(root, width=400, height=300, bg="black")
canvas.pack()
speed_slider = tk.Scale(
    root, 
    from_=0, 
    to=5, 
    orient="horizontal", 
    label="Rotation Speed (degrees/sec)", 
    command=update_speed,
    length=300
)
speed_slider.set(1)  # Default rotation speed
speed_slider.pack()
distance_slider = tk.Scale(
    root, 
    from_=1, 
    to=500, 
    orient="horizontal", 
    label="distance", 
    command=update_distance,
    length=300
)
distance_slider.set(50)  # Default distance
distance_slider.pack()
distance = 50
# Variables and constants

#do not change lower than 100 it causes graphical problems ??????????
FOV = 100  # this is distance to the center of the screen - https://www.youtube.com/watch?v=nvWDgBGcAIM&ab_channel=GraverDev
camera_pos = np.array([0, 0, FOV+distance])
TIMEDELAY = 16  # for drawing the scene in milliseconds (16 ms is 60 fps)
WindowSizeY = 300
WindowSizeX = 400
angle = np.radians(1)
size = 2  # size of points in terms of a circles bounding box
# preprocess_obj("cube.obj", "cube_cleaned.obj")


def load_shape(shape):
    shapes = {
        "cube": (
            np.array([[-0.5, -0.5, -0.5], [0.5, -0.5, -0.5], [0.5, 0.5, -0.5], [-0.5, 0.5, -0.5],
                      [-0.5, -0.5, 0.5], [0.5, -0.5, 0.5], [0.5, 0.5, 0.5], [-0.5, 0.5, 0.5]]),
            [[0, 1], [1, 2], [2, 3], [3, 0], [4, 5], [5, 6], [6, 7], [7, 4], [0, 4], [1, 5], [2, 6], [3, 7]],
            [[3, 2, 1, 0], [4, 5, 6, 7], [0, 4, 7, 3], [2, 6, 5, 1], [7, 6, 2, 3], [0, 1, 5, 4]]
        ),
        "pyramid": (
            np.array([[-0.5, -0.5, 0], [0.5, -0.5, 0], [0.5, 0.5, 0], [-0.5, 0.5, 0], [0, 0, 1]]),
            [[0, 1], [1, 2], [2, 3], [3, 0], [0, 4], [1, 4], [2, 4], [3, 4]],
            [[0, 1, 2, 3], [0, 1, 4], [1, 2, 4], [2, 3, 4], [3, 0, 4]]
        ),
        "tetrahedron": ( #BROKEN!!!!!!!! need to fix the faces 
            np.array([[0, 0, 0], [1, 0, 0], [0.5, np.sqrt(3)/2, 0], [0.5, np.sqrt(3)/6, np.sqrt(2/3)]]),
            [[0, 1], [1, 2], [2, 0], [0, 3], [1, 3], [2, 3]],
            [[0, 1, 2], [0, 1, 3], [1, 2, 3], [2, 0, 3]]
        )
    }
    return shapes.get(shape.lower()) or ValueError(f"Shape '{shape}' is not defined.")


shape_name = "cube"
points, edges, faces = load_shape(shape_name)

drawscene()

root.mainloop()
