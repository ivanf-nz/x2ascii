import numpy as np
from obj_parser import get_obj

# This class is used to represent a 3D object in space.


class Object3D:
    def __init__(self, filepath, rotations):
        points, faces = get_obj(filepath)
        # Points in 3D space [[x, y, z], [x, y, z], ...]
        self.points = np.array(points)
        # Faces of the object[[point1, point2, point3],[point1],[point2] ...]
        # where point is the index of the point in the points array
        self.faces = np.array(faces)

        # Check if rotations are all False
        if all(not r for r in rotations):
            self.rotations = [False, True, False]  # default to y rotation
        else:
            self.rotations = rotations

    def rotate(self, angle):
        # Initialize the combined rotation matrix for this specific rotation call
        self.rotation_matrix = np.eye(3)

        # Accumulate rotations into self.rotation_matrix based on the axes specified
        if angle:
            # Corrected loop logic: Check index for axis
            if self.rotations[0]:  # Index 0 for X
                self._build_rotate_x(angle)
            if self.rotations[1]:  # Index 1 for Y
                self._build_rotate_y(angle)
            if self.rotations[2]:  # Index 2 for Z
                self._build_rotate_z(angle)

        # Apply the final combined rotation matrix to all points at once
        self.points = self.points @ self.rotation_matrix.T

    # Methods to apply a specific rotation immediately
    def apply_rotation_x(self, angle):
        rotation_matrix = np.array([[1, 0, 0],
                                    [0, np.cos(angle), -np.sin(angle)],
                                    [0, np.sin(angle), np.cos(angle)]])
        self.points = self.points @ rotation_matrix.T

    def apply_rotation_y(self, angle):
        rotation_matrix = np.array([[np.cos(angle), 0, np.sin(angle)],
                                    [0, 1, 0],
                                    [-np.sin(angle), 0, np.cos(angle)]])
        self.points = self.points @ rotation_matrix.T

    def apply_rotation_z(self, angle):
        rotation_matrix = np.array([[np.cos(angle), -np.sin(angle), 0],
                                    [np.sin(angle), np.cos(angle), 0],
                                    [0, 0, 1]])
        self.points = self.points @ rotation_matrix.T

    # Renamed methods to indicate they build the internal rotation matrix for the main 'rotate' method
    def _build_rotate_x(self, angle):
        rotation_matrix = np.array([[1, 0, 0],
                                    [0, np.cos(angle), -np.sin(angle)],
                                    [0, np.sin(angle), np.cos(angle)]])
        # @ is matrix multiplication with T being its transpose
        self.rotation_matrix = self.rotation_matrix @ rotation_matrix.T

    def _build_rotate_y(self, angle):
        rotation_matrix = np.array([[np.cos(angle), 0, np.sin(angle)],
                                    [0, 1, 0],
                                    [-np.sin(angle), 0, np.cos(angle)]])
        self.rotation_matrix = self.rotation_matrix @ rotation_matrix.T

    def _build_rotate_z(self, angle):
        rotation_matrix = np.array([[np.cos(angle), -np.sin(angle), 0],
                                    [np.sin(angle), np.cos(angle), 0],
                                    [0, 0, 1]])
        self.rotation_matrix = self.rotation_matrix @ rotation_matrix.T
