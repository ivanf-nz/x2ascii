import tkinter as tk
import numpy as np

# TODO:
# load objs instead of creating arrays
# clean objs

# convert each face to an ascii image?
# make it copy and pastable
# fix the comments
#rotate camera (how?)


# projects a 3d point onto a 2d surface (your screen)
def project(point):
    x = point[0]
    y = point[1]
    z = point[2]
    px = horizontalshift/2 + ((x*FOV)/(FOV+z)) * distance
    py = verticalshift/2 + ((y*FOV)/(FOV+z)) * distance
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

def lighting_intensity(face):
    normal = compute_normal(face)
    face_point = points[face[0]]  # any point on the face
    light_vector = light_pos - face_point # this is a vector from point on face to light and so in same direction as normal
    normal = normal / np.linalg.norm(normal)
    light_vector = light_vector / np.linalg.norm(light_vector) #normalized to ensure in range from 0 to 1
    intensity = max(0.1,np.dot(light_vector ,normal)) #1 means lit, 0 means not lit

    return intensity
def drawface(face, j):
    facepoints = []
    for i in range(len(face)):
        px, py = project(points[face[i]])
        facepoints.append((px, py))  # creates an array of points for that face
        colour_value = int(j*255)#int(255 - j*255)
        colour = f"#{colour_value:02x}{colour_value:02x}{colour_value:02x}"  # hex convert
        canvas.create_polygon(facepoints, fill=colour, outline=colour) #further away = lighter, closest = dark


def compute_normal(face):
    p1, p2, p3 = points[face[0]], points[face[1]], points[face[2]]
    edge1 = p2 - p1
    edge2 = p3 - p1
    normal = np.cross(edge1, edge2)  # Cross product
    return -(normal / np.linalg.norm(normal))  # Normalize to length of 1 and invert (cw direction)


def is_face_visible(face):
    normal = compute_normal(face)
    face_point = points[face[0]]  # any point on the face
    view_vector = camera_pos - face_point #from face point to camera pos
    return np.dot(view_vector, normal) > 0  # true if the face is visible


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
            i = lighting_intensity(face)
            drawface(face, i)
    rotate_all()

    root.after(TIMEDELAY, drawscene)


def rotate_all():
    global points
    # could make more efficient by matrix multiplying the rotation matrixes and then matrix multipy with transposing the points array
    #points = rotateZ(rotateY(points))
    points = rotateY(points)

def update_speed(val):
    global angle
    angle = np.radians(float(val))
def update_distance(val):
    global distance,camera_pos
    distance = int(val)
    camera_pos = np.array([0, 0, FOV+distance])
def update_horizontalshift(val):
    global horizontalshift
    horizontalshift = int(val)
def update_verticalshift(val):
    global verticalshift
    verticalshift = int(val)
# Setup Tkinter
root = tk.Tk()
root.title("Render Screen")
root.geometry("800x700")
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

horizontalshift_slider = tk.Scale(
    root, 
    from_=-200, 
    to=1000, 
    orient="horizontal", 
    label="horizontal shift", 
    command=update_horizontalshift,
    length=300
)
horizontalshift_slider.set(400)  # Default distance
horizontalshift_slider.pack()
verticalshift_slider = tk.Scale(
    root, 
    from_=-200, 
    to=1000, 
    orient="horizontal", 
    label="vertical shift",  
    command=update_verticalshift,
    length=300
)
verticalshift_slider.set(300)  # Default distance
verticalshift_slider.pack()
WindowSizeY = 300
WindowSizeX = 400
horizontalshift = WindowSizeX
verticalshift = WindowSizeY
# Variables and constants

#do not change lower than 100 it causes graphical problems ??????????
FOV = 100  # this is distance to the center of the screen - https://www.youtube.com/watch?v=nvWDgBGcAIM&ab_channel=GraverDev
camera_pos = np.array([horizontalshift, verticalshift, FOV+distance])
TIMEDELAY = 16  # for drawing the scene in milliseconds (16 ms is 60 fps)

angle = np.radians(1)
size = 2  # size of points in terms of a circles bounding box
# preprocess_obj("cube.obj", "cube_cleaned.obj")

light_pos = np.array([0,10,0]) #placed above in y direction
def load_shape(shape):
    shapes = {
        "cube": (
            np.array([[-0.5, -0.5, -0.5], [0.5, -0.5, -0.5], [0.5, 0.5, -0.5], [-0.5, 0.5, -0.5],
                      [-0.5, -0.5, 0.5], [0.5, -0.5, 0.5], [0.5, 0.5, 0.5], [-0.5, 0.5, 0.5]]),
            [[0, 1], [1, 2], [2, 3], [3, 0], [4, 5], [5, 6], [6, 7], [7, 4], [0, 4], [1, 5], [2, 6], [3, 7]],
            [[3, 2, 1, 0], [4, 5, 6, 7], [0, 4, 7, 3], [2, 6, 5, 1], [7, 6, 2, 3], [0, 1, 5, 4]] #clockwise face points direction!!!
        ),
        "pyramid": (
            np.array([[-0.5, -0.5, 0], [0.5, -0.5, 0], [0.5, 0.5, 0], [-0.5, 0.5, 0], [0, 0, 1]]),
            [[0, 1], [1, 2], [2, 3], [3, 0], [0, 4], [1, 4], [2, 4], [3, 4]],
            [[0, 1, 2, 3], [0, 1, 4], [1, 2, 4], [2, 3, 4], [3, 0, 4]] #clockwise face points direction!!!
        ),
        "tetrahedron": ( #BROKEN!!!!!!!! need to fix the faces in cw direction
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
