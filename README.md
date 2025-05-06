# 3D Model and Image to ASCII Art Converter

x2ascii is a Python project that converts 3D models (OBJ files) and images into ASCII art. It includes tools for rendering 3D objects as ASCII in the terminal and converting images into ASCII text files.

<img src="https://raw.githubusercontent.com/ivanf-nz/x2ascii/refs/heads/main/readme_images/spinning_cube.gif" alt="ascii_cube" width="300" height="300">
<img width="650" alt="image" src="https://raw.githubusercontent.com/ivanf-nz/x2ascii/refs/heads/main/readme_images/print_hello_ascii.png" />

---

## Features

-   **3D Model Rendering**: Renders 3D OBJ files as ASCII art in the terminal.
    -   Uses perspective projection and basic lighting.
    -   Supports filled faces (with backface culling and Painter's algorithm) or wireframe rendering.
    -   Utilizes NumPy for vectorized calculations (projection, normals, visibility, lighting, sorting) for improved performance.
    -   Highly customizable via command-line arguments (model, dimensions, rotation speed/axes, distance, wireframe thickness, initial flip).
-   **Image to ASCII Conversion**: Converts images (JPG/PNG) into ASCII text files.
-   **OBJ File Handling**: Automatically parses, cleans, centers, and normalizes OBJ files to extract vertices and faces.

---

## File Descriptions

### `src/main.py`
-   Main script for rendering 3D objects as ASCII art in the terminal.
-   Uses `argparse` for command-line arguments (model path, dimensions, speed, distance, thickness, rotation axes, etc.).
-   Initializes the `Object3D` and `Renderer` classes and runs the rendering loop.

### `src/image_to_ascii.py`
-   Converts images into ASCII text files.
-   Prompts the user for the image filename.
-   Outputs the ASCII art directly to the terminal and saves it to a text file in the `output/` directory.

### `src/obj_parser.py`
-   Parses and cleans OBJ files to extract vertices (points) and faces.
-   Handles basic OBJ file format variations (e.g., `f v/vt/vn`).
-   Automatically centers the model vertices around the origin and normalizes their scale.

### `src/object3d.py`
-   Defines the `Object3D` class to hold the points and faces of a 3D model loaded via `obj_parser`.
-   Includes methods for applying rotations to the object around the X, Y, and Z axes based on command-line flags.

### `src/renderer.py`
-   Defines the `Renderer` class responsible for the rendering logic.
-   Handles 3D projection, lighting calculations, face visibility (back-face culling), depth sorting (Painter's algorithm), and ASCII character mapping.
-   Uses vectorized NumPy operations for efficiency.
-   Contains the main rendering loop (`run` method) and drawing functions.

---

## Usage

### Rendering 3D Models
1.  Ensure you have an OBJ file (e.g., in the `models/` directory).
2.  Run the script from the root directory using `python3 src/main.py` with optional arguments:
    ```bash
    # Example using default values (models/cube2.obj, width 60, height 30, speed 45, distance 12, filled faces)
    python3 src/main.py

    # Example specifying a different model, wireframe, speed, and rotation axis
    python3 src/main.py -o models/your_model.obj -t 1 -s 90 -x
    ```
    -   `-o` or `--obj_file`: Path to the .obj file (default: `../models/cube2.obj`).
    -   `--width`: Width of the internal rendering canvas (default: 60).
    -   `--height`: Height of the internal rendering canvas (default: 30).
    -   `-f` or `--flip`: If present, flips the object upside down initially (default: False).
    -   `-s` or `--speed`: Speed of rotation in degrees per second (default: 45).
    -   `-d` or `--distance`: Distance multiplier for projection (affects perceived size) (default: 12).
    -   `-t` or `--thickness`: Thickness for wireframe edges. If `0` (default), renders filled faces. If `> 0`, enables wireframe mode with the specified thickness.
    -   `-x`, `-y`, `-z`: Flags to enable rotation around the respective axes. If none are specified, defaults to Y-axis rotation. Multiple axes can be combined.

### Converting Images to ASCII
1.  Place your image file (e.g., JPG, PNG) in the project directory or provide a path.
2.  Run the script from the root directory:
    ```bash
    python3 src/image_to_ascii.py
    ```
3.  Enter the image filename (e.g., `my_image.png`) when prompted.
4.  The ASCII art will be displayed in the terminal and saved to a file like `output/my_image_ascii.txt`.

---

## Project Hierarchy

```
x2ascii/
├── .gitignore              # Git ignore file
├── README.md               # Project documentation
├── src/                    # Source code
│   ├── main.py             # Renders 3D models as ASCII art (CLI entry point)
│   ├── image_to_ascii.py   # Converts images to ASCII art
│   ├── obj_parser.py       # Parses, cleans, centers, normalizes OBJ files
│   ├── object3d.py         # Represents a 3D object (points, faces, rotation)
│   ├── renderer.py         # Handles the rendering logic (projection, drawing, ASCII conversion)
├── models/                 # 3D model files (OBJ format)
│   ├── cube.obj
│   ├── cube2.obj
├── output/                 # Output directory for generated ASCII text files
├── readme_images/          # Images used in README.md
│   ├── spinning_cube.gif
│   └── print_hello_ascii.png
```

---

## Future Improvements
-   Add more command-line options to `image_to_ascii.py` (like character sets).
-   Implement camera controls (rotation, zoom, panning) instead of just rotating the object. (might not be possible due to being in the terminal)
-   Add unit tests to ensure calculations (projection, lighting, rotation) are performed correctly.
-   Explore removing the OpenCV dependency for a pure NumPy/Python rasterizer (potentially slower).
