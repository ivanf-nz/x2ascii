import numpy as np
from obj_parser import get_obj

# This class is used to represent a 3D object in space.


class Object3D:
    def __init__(self, filepath):
        points, faces = get_obj(filepath)
        # Points in 3D space
        self.points = points
        # Faces of the object, defined by index in the points array
        self.faces = faces

    # Rotation matrix calculations
    def rotate_x(self, angle):
        rotation_matrix = np.array([[1, 0, 0],
                                    [0, np.cos(angle), -np.sin(angle)],
                                    [0, np.sin(angle), np.cos(angle)]])
        # @ is matrix multiplication with T being its transpose
        self.points = self.points @ rotation_matrix.T

    def rotate_y(self, angle):
        rotation_matrix = np.array([[np.cos(angle), 0, np.sin(angle)],
                                    [0, 1, 0],
                                    [-np.sin(angle), 0, np.cos(angle)]])
        self.points = self.points @ rotation_matrix.T

    def rotate_z(self, angle):
        rotation_matrix = np.array([[np.cos(angle), -np.sin(angle), 0],
                                    [np.sin(angle), np.cos(angle), 0],
                                    [0, 0, 1]])
        self.points = self.points @ rotation_matrix.T
