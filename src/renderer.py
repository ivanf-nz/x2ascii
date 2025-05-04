import numpy as np
import cv2
import time
from object3d import Object3D

# This class is used to render a 3D object in a 2D space.


class Renderer:
    def __init__(self, model: Object3D, width: int, height: int, distance: int, speed: int, thickness: int):
        # Object3D(filepath) which contains the points and faces of the object
        self.model = model

        # Width and height of the screen
        self.width = 60
        self.height = 30

        # Fov and distance constants for projection (triangle calculations)
        self.fov = 10
        self.distance = distance

        # placed above in y and a little bit in z direction (x,y,z)
        self.light_pos = np.array([0, 10, 3])
        self.camera_pos = np.array([0, 0, 100])

        self.grid = np.full((self.height, self.width), 255,
                            dtype=np.uint8)
        self.ascii_chars = "@%#*+=-:. "

        self.degree_per_second = speed

        self.thickness = thickness

    # projects a 3d point onto a 2d surface (your screen)
    # the points are in the format [[x,y,z],[x,y,z]...]
    # the projected points are in the format [[x,y],[x,y]...]
    # vectorized for speed and efficiency
    def project_all_points(self, points):

        x = points[:, 0]
        y = points[:, 1]
        z = points[:, 2]
        px = self.width / 2 + ((x * self.fov) / (self.fov + z)) * self.distance
        py = self.height / 2 + \
            ((y * self.fov) / (self.fov + z)) * \
            self.distance * 0.5  # adjust for height of chars
        return np.column_stack((px, py)).astype(int)

    def compute_normal(self, face):
        p1, p2, p3 = self.model.points[face[0]
                                       ], self.model.points[face[1]], self.model.points[face[2]]
        edge1 = p2 - p1
        edge2 = p3 - p1
        normal = np.cross(edge1, edge2)
        # Normalize to length of 1 (ccw->cw direction depends on negative sign of normal)
        return normal / np.linalg.norm(normal)

    # determines the lighting intensity of a face compared to the light position (assuming light is pointing at object at all times)
    # returns a value from 0 to 1 where 0 means lit and 1 means unlight (because of how white = nothing printing in ascii and so 0 = black)
    def lighting_intensity(self, face):
        normal = self.compute_normal(face)
        face_point = self.model.points[face[0]]  # any point on the face
        # light_vector = light_pos - face_point # this is a vector from point on face to light and so in same direction as normal
        light_vector = face_point - self.light_pos
        normal = normal / np.linalg.norm(normal)  # normalize to length of 1
        # normalized to ensure in range from 0 to 1
        light_vector = light_vector / np.linalg.norm(light_vector)

        # dot product means that 1 = same direction, 0 = 90 degrees to each other and -1 is opposite direction
        # changed with 1 minus to have black bg for ascii
        intensity = 1 - max(0.1, np.dot(light_vector, normal))

        return intensity

    # draws the faces with light values included
        # black = lit, white = unlit

    def drawface(self, face, intensity, projected_points):

        facepoints = []
        for i in range(len(face)):
            px, py = projected_points[face[i]]
            # creates an array of points for that face
            facepoints.append((px, py))

        colour_value = int(intensity * 255)  # 255 = white, 0 = black
        facepoints = np.array(facepoints, dtype=np.int32)
        cv2.fillPoly(self.grid, [facepoints], color=colour_value)

    def calculate_edge(self, face, projected_points):
        # need to add option for drawing edges
        for i in range(len(face)-1):  # draws the edges

            self.drawedge(projected_points[face[i]],
                          projected_points[face[i + 1]])
        # loops back from the end point to the start point - if not here will have missing edges
        self.drawedge(projected_points[face[0]],
                      projected_points[face[(len(face)-1)]])

    def drawedge(self, point1, point2):
        # Draw a line between two points
        cv2.line(self.grid, point1, point2, (0, 0, 0), self.thickness)

    def is_face_visible(self, face):
        normal = self.compute_normal(face)
        face_point = self.model.points[face[0]]  # any point on the face
        view_vector = self.camera_pos - face_point  # from face point to camera pos
        return np.dot(view_vector, normal) < 0  # true if the face is visible

    def sort_faces_by_distance(self, faces):
        centroids = [np.mean(self.model.points[face], axis=0)
                     for face in faces]
        distances = [np.linalg.norm(self.camera_pos - centroid)
                     for centroid in centroids]
        # put reverse=True for really trippy ghost effect
        sorted_faces = sorted(zip(faces, distances), key=lambda x: x[1])
        # sorted from furthest to closest
        return [face for face, _ in sorted_faces]

    def print_ascii(self):

        im = self.grid
        # initialise the ascii line to be printed
        print_line = ""

        # goes thorugh each pixel
        for i in range(self.height):

            for j in range(self.width):

                # gets pixel value
                pixel = im[i, j]

                # make each pixel an ascii char 0(black)-255(white)
                print_line += str(self.ascii_chars[int(pixel /
                                                       255*(len(self.ascii_chars)-1))])

            print_line += "\n"  # combine this with the line above
        # ensure clean output using Carriage Return
        print(f"\r{print_line}", end="", flush=True)

    def draw_scene(self, dt):

        frame_rotation_angle = np.radians(
            # rotate x degrees per second * dt (to ensure rotation is the same regardless of frame rate)
            self.degree_per_second) * dt
        # if no rotation is set, rotate around y axis
        self.model.rotate(frame_rotation_angle)
        projected_points = self.project_all_points(self.model.points)
        # 255 to set background to white
        self.grid = np.full((self.height, self.width), 255, dtype=np.uint8)
        if self.thickness == 0:
            sorted_faces = self.sort_faces_by_distance(self.model.faces)
            for face in sorted_faces:
                if self.is_face_visible(face):
                    intensity = self.lighting_intensity(face)
                    self.drawface(face, intensity, projected_points)
        else:
            for face in self.model.faces:
                self.calculate_edge(face, projected_points)

        try:  # printing to screen hasnt been fixed and can cause errors as the canvas is being created
            self.print_ascii()
        except Exception as e:
            print(f"An error occurred: {e}")

    def run(self):
        self.last_frame_time = time.perf_counter()
        while True:
            current_time = time.perf_counter()
            dt = current_time - self.last_frame_time
            if dt < 1/60:  # limit to no more than 60 FPS
                time.sleep(1/60 - dt)
                current_time = time.perf_counter()  # Recalculate time after sleep
                dt = current_time - self.last_frame_time

            self.last_frame_time = current_time

            self.draw_scene(dt)
            print(f"fps={1/dt:.2f}", end="\r")  # Print the FPS to the console
