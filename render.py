import tkinter as tk
import numpy as np
from PIL import Image, ImageGrab,ImageOps
from obj_cleaning import get_obj, clean_line
#######################################################################
#                                                                     #
#                   3D MODEL ASCII VIEWER                             #
#                                                                     #
# X positive is defined as going to the right                         #
# Y positive is defiend as up and down                                #
# Z positive is defined as going towards the viewer, out of the screen#
#######################################################################

# TODO:

# load objs instead of creating arrays
# clean objs

#make options for loading objs, moving them by 0.5 or 1 (points array)
#option for disabling black outline between edges

#rotation to add a input of degree

#make the grid a 2d array instead of taking screen shots

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

# draws the projected 3d edge onto a 2d surface
def drawedge(start,end):
    px1, py1 = project(start)
    px2, py2 = project(end)
    canvas.create_line(px1, py1, px2, py2, fill="black",width=size)

# determines the lighting intensity of a face compared to the light position (assuming light is pointing at object at all times)
# returns a value from 0 to 1 where 0 means lit and 1 means unlight (because of how white = nothing printing in ascii and so 0 = black)
def lighting_intensity(face):
    normal = compute_normal(face)
    face_point = points[face[0]]  # any point on the face
    light_vector = light_pos - face_point # this is a vector from point on face to light and so in same direction as normal
    normal = normal / np.linalg.norm(normal) # normalize to length of 1
    light_vector = light_vector / np.linalg.norm(light_vector) #normalized to ensure in range from 0 to 1

    #dot product means that 1 = same direction, 0 = 90 degrees to each other and -1 is opposite direction
    intensity = 1-max(0.3,np.dot(light_vector ,normal)) #changed with 1- (1 minus) to have black bg for ascii 
    #intensity = max(0.1,np.dot(light_vector ,normal)) 1 means lit, 0 means not lit
    return intensity

#draws the faces with light values included
# black = lit, white = unlit 
def drawface(face, intensity):
    facepoints = []
    for i in range(len(face)):
        px, py = project(points[face[i]])
        facepoints.append((px, py))  # creates an array of points for that face
        colour_value = int(intensity*255) #255 = white, 0 = black
        colour = f"#{colour_value:02x}{colour_value:02x}{colour_value:02x}"  # hex convert
        canvas.create_polygon(facepoints, fill=colour, outline=colour)
    #for i in range(len(face)-1): #draws the edges
        #drawedge(points[face[i]],points[face[i + 1]])
    #drawedge(points[face[0]],points[face[(len(face)-1)]]) #loops back from the end point to the start point - if not here will have missing edges

# computes the normal of a face. used in determining if a face is visible and used in lighting calculations
def compute_normal(face):
    p1, p2, p3 = points[face[0]], points[face[1]], points[face[2]]
    edge1 = p2 - p1
    edge2 = p3 - p1
    normal = np.cross(edge1, edge2)  # cross product
    return - (normal / np.linalg.norm(normal))  # Normalize to length of 1 and invert with negative sign (ccw->cw direction)

def is_face_visible(face):
    normal = compute_normal(face)
    face_point = points[face[0]]  # any point on the face
    view_vector = camera_pos - face_point # from face point to camera pos
    return np.dot(view_vector, normal) > 0  # true if the face is visible

#rotates the whole array by the given angle and using matrix multiplication
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

#NEED TO BE FIXED
#gets a image of the canvas containing the model and returns the image
def get_canvas_img():

    xmonitor = canvas.winfo_rootx()
    ymonitor = canvas.winfo_rooty()
    canvaswidth = canvas.winfo_width()
    canvasheight = canvas.winfo_height()
    windowwidth = root.winfo_width()
    windowheight = root.winfo_height() #should be set as constants
 
    bbox = (xmonitor+(windowwidth-canvaswidth)/2, ymonitor+28, xmonitor+(windowwidth-canvaswidth)/2+canvaswidth, ymonitor + canvasheight+28)

    image = ImageGrab.grab(bbox) #broken and i dont know why
    return image
    #print(f"Pixel value at ({x}, {y}): {pixel_value}")
def print_ascii(im, new_width):
    width, height = im.size
    new_height = int(height/width * new_width *0.5)
    im = im.resize((new_width, new_height))
    
    #convert to grayscale
    im = ImageOps.grayscale(im)


    #ascii define white to black
    ascii_chars = "@%#*+=-:. "
    ascii_string = ""
    #opens the text file - to be added later
    #f = open("outputascii.txt","w")

    #goes thorugh each pixel
    for i in range(new_height):
        
        for j in range(new_width):

            #gets pixel value
            pixel = im.getpixel((j,i))

            #make each pixel an ascii char 0(black)-255(white)
            ascii_string += str(ascii_chars[int(pixel/255*(len(ascii_chars)-1))]) 

        ascii_string += "\n" #combine this with the line above
    print(f"\r{ascii_string}",end="",flush=True) #ensure clean output using Carriage Return 

    #print("Outputted ascii text file")
def drawscene():
    global points
    canvas.delete("all") # some artifcating stuff occuring at one of the corners not sure how to remove
    for face in faces:
        if is_face_visible(face):
            intensity = lighting_intensity(face)
            drawface(face, intensity)
    
    rotate_all()
    image = get_canvas_img()
    try: #printing to screen hasnt been fixed and can cause errors as the canvas is being created
        print_ascii(image,70)
    except Exception as e:
        print(f"An error occurred: {e}")
    
    # call the same function to repeatedly draw the scene
    root.after(TIMEDELAY, drawscene)

#rotates the scene 
def rotate_all():
    global points
    # could make more efficient by matrix multiplying the rotation matrixes and then matrix multipy with transposing the points array
    points = rotateX(points)

# functions for changing the slider values 
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

# setup Tkinter
root = tk.Tk()
root.title("Render Screen")
root.geometry("800x700") #width x height
root.configure(bg="black")

# setup canvas size for rendering object
WindowSizeY = 300
WindowSizeX = 400
canvas = tk.Canvas(root, width=WindowSizeX, height=WindowSizeY, bg="white")  
canvas.pack()

#default values for sliders

angle = np.radians(1)
print(np.degrees(angle))
distance = 50
horizontalshift = WindowSizeX
verticalshift = WindowSizeY 

# setup sliders
speed_slider = tk.Scale(
    root, 
    from_=0, 
    to=5, 
    orient="horizontal", 
    label="Rotation Speed (degrees/sec)", 
    command=update_speed,
    length=300
)
speed_slider.set(np.degrees(angle))  # default rotation speed
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
distance_slider.set(distance)  # default distance
distance_slider.pack()
horizontalshift_slider = tk.Scale(
    root, 
    from_=-200, 
    to=1000, 
    orient="horizontal", 
    label="horizontal shift", 
    command=update_horizontalshift,
    length=300
)
horizontalshift_slider.set(horizontalshift)  # Default x value
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
verticalshift_slider.set(verticalshift)  # Default y value
verticalshift_slider.pack()

# Variables and constants

#fov lower than 100 used to cause problems rendering ?
FOV = 100  # this is distance to the center of the screen - https://www.youtube.com/watch?v=nvWDgBGcAIM&ab_channel=GraverDev
camera_pos = np.array([horizontalshift, verticalshift, FOV+distance])
TIMEDELAY = 16  # for drawing the scene in milliseconds (16 ms is 60 fps)
size = 2  # size of edges
# preprocess_obj("cube.obj", "cube_cleaned.obj")

light_pos = np.array([0,10,0]) #placed above in y direction

#default shape loader (some are broken)
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
            [[3, 2, 1, 0], [0, 1, 4], [1, 2, 4], [2, 3, 4], [3, 0, 4]] #clockwise face points direction!!!
        ),
        "tetrahedron": ( #faces work but lighting is working in the opposite of how it's meant to be ?
            np.array([[0, 0, 0], [1, 0, 0], [0.5, np.sqrt(3)/2, 0], [0.5, np.sqrt(3)/6, np.sqrt(2/3)]]) -0.5,
            [[0, 1], [1, 2], [2, 0], [0, 3], [1, 3], [2, 3]],
            [[2, 1, 0], [3, 1, 0], [3, 2, 1], [3, 0, 2]]
        )
    }
    return shapes.get(shape.lower()) or ValueError(f"Shape '{shape}' is not defined.")


# shape_name = "cube"
# points, edges, faces = load_shape(shape_name)

obj = "fox.obj" #https://www.a1k0n.net/2011/07/20/donut-math.html website might help with lighting
points, faces = get_obj(obj)
for i in range(180):
    points = rotateZ(points)
drawscene()

root.mainloop()
