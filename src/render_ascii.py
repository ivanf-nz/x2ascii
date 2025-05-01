# import tkinter as tk
import numpy as np
import argparse
from object3d import Object3D
from renderer import Renderer

# Directions for the 3D model viewer
# x positive is defined as going to the right
# y positive is defined as up and down
# z positive is defined as going towards the viewer, out of the screen


def main():
    parser = argparse.ArgumentParser(description="3D Model ASCII Viewer")
    parser.add_argument(
        "-o", "--obj_file", type=str, default="../models/cube2.obj", help="Path to the .obj file")
    parser.add_argument("--width", type=int, default=400,
                        # Doesnt actually change the height of the ascii art, changes the height of cv2 window which is resized
                        help="Width of the output ASCII art")
    parser.add_argument("--height", type=int, default=300,
                        help="Height of the output ASCII art")  # Same as above
    parser.add_argument("-f", "--flip", action='store_true',
                        help="If present, will flip the object upside down initially")
    parser.add_argument("-s", "--speed", type=int, default=45,
                        help="Speed of rotation in degrees per second")
    args = parser.parse_args()

    # Load the object from the specified file (has the points and faces)
    model = Object3D(args.obj_file)

    # Rotate the object upside down (180 degrees) if the flag is set
    if args.flip:
        model.rotate_z(np.radians(180))

    # Initial rotation regardless of flip
    model.rotate_y(np.radians(45))
    model.rotate_x(np.radians(45))

    # Create the renderer with the specified width and height
    renderer = Renderer(model, args.width, args.height, args.speed)

    # Run the renderer (which has the main loop)
    renderer.run()


# Run main file
if __name__ == "__main__":
    main()
