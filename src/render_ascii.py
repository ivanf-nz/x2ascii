# import tkinter as tk
import numpy as np
from obj_parser import get_obj
import cv2
import time
import argparse
from object3d import Object3D
from renderer import Renderer
#######################################################################
#                                                                     #
#                   3D MODEL ASCII VIEWER                             #
#                                                                     #
# X positive is defined as going to the right                         #
# Y positive is defined as up and down                                #
# Z positive is defined as going towards the viewer, out of the screen#
#######################################################################

# TODO:
#
# make options for loading objs, moving them by 0.5 or 1 (points array)
# option for disabling black outline between edges

# rotation to add a input of degree

# make it copy and pastable kinda already done but could be improved (button outputs a ascii file)
# improve the comments
# rotate camera - not the cube (how?)


#######################################################################

def main():
    parser = argparse.ArgumentParser(description="3D Model ASCII Viewer")
    parser.add_argument(
        "-o", "--obj_file", type=str, default="../models/cube2.obj", help="Path to the .obj file")
    parser.add_argument("--width", type=int, default=400,
                        help="Width of the output ASCII art")
    parser.add_argument("--height", type=int, default=300,
                        help="Height of the output ASCII art")
    parser.add_argument("--f", type=bool, default=False,
                        help="If True, will flip the object upside down")
    args = parser.parse_args()

    # Load the object from the specified file (has the points and faces)
    model = Object3D(args.obj_file)

    # Rotate the object upside down (180 degrees)
    # if args.f:
    model.rotate_z(np.radians(180))

    model.rotate_y(np.radians(45))
    model.rotate_x(np.radians(45))

    # Create the renderer with the specified width and height
    renderer = Renderer(model, args.width, args.height)

    # Run the renderer (which has the main loop)
    renderer.run()


# Run file
if __name__ == "__main__":
    main()
