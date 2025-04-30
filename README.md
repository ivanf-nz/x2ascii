# x2ascii

x2ascii is a Python project that converts 3D models (OBJ files) and images into ASCII art. It includes tools for rendering 3D objects as ASCII in the terminal and converting images into ASCII text files.

<img src="https://raw.githubusercontent.com/ivanf-nz/x2ascii/refs/heads/main/readme_images/spinning_cube.gif" alt="ascii_cube" width="300" height="300">
<img width="650" alt="image" src="https://raw.githubusercontent.com/ivanf-nz/x2ascii/refs/heads/main/readme_images/print_hello_ascii.png" />

---

## Features

- **3D Model Rendering**: Render 3D OBJ files as ASCII art in the terminal using perspective projection and lighting. Supports command-line arguments for customization.
- **Image to ASCII Conversion**: Convert images (JPG/PNG) into ASCII text files.
- **OBJ File Cleaning**: Automatically parses and cleans OBJ files to extract vertices and faces.

---

## File Descriptions

### `src/render_ascii.py`
- Main script for rendering 3D objects as ASCII art in the terminal.
- Uses `argparse` for command-line arguments (model path, width, height).
- Initializes the `Object3D` and `Renderer` classes and runs the rendering loop.

### `src/image_to_ascii.py`
- Converts images into ASCII text files.
- Prompts the user for the image filename.
- Outputs the ASCII art directly to the terminal and saves it to a text file in the `output/` directory.

### `src/obj_parser.py`
- Parses and cleans OBJ files to extract vertices (points) and faces.
- Handles basic OBJ file format variations (e.g., `f v/vt/vn`).

### `src/object3d.py`
- Defines the `Object3D` class to hold the points and faces of a 3D model.
- Includes methods for rotating the object around the X, Y, and Z axes.

### `src/renderer.py`
- Defines the `Renderer` class responsible for the rendering logic.
- Handles 3D projection, lighting calculations, face visibility (back-face culling), depth sorting, and ASCII character mapping.
- Contains the main rendering loop (`run` method) and drawing functions.

---

## Usage

### Rendering 3D Models
1. Ensure you have an OBJ file (e.g., in the `models/` directory).
2. Run the script from the root directory using `python3 src/render_ascii.py` with optional arguments:
   ```bash
   # Example using default values (models/cube2.obj, width 400, height 300)
   python3 src/render_ascii.py

   # Example specifying a different model and dimensions
   python3 src/render_ascii.py -o models/your_model.obj --width 600 --height 450
   ```
   - `-o` or `--obj_file`: Path to the .obj file (default: `../models/cube2.obj` relative to `src/`).
   - `--width`: Width of the internal rendering canvas (default: 400).
   - `--height`: Height of the internal rendering canvas (default: 300).
   - `--f`: Flip the object upside down initially (default: False).

### Converting Images to ASCII
1. Place your image file (e.g., JPG, PNG) in the project directory or provide a path.
2. Run the script from the root directory:
   ```bash
   python3 src/image_to_ascii.py
   ```
3. Enter the image filename (e.g., `my_image.png`) when prompted.
4. The ASCII art will be displayed in the terminal and saved to a file like `output/my_image_ascii.txt`.

---

## Project Hierarchy

```
x2ascii/
├── .gitignore              # Git ignore file
├── README.md               # Project documentation
├── src/                    # Source code
│   ├── render_ascii.py     # Renders 3D models as ASCII art
│   ├── image_to_ascii.py   # Converts images to ASCII art
│   ├── obj_parser.py       # Parses and cleans OBJ files
│   ├── object3d.py         # Represents a 3D object
│   ├── renderer.py         # Handles the rendering logic
├── models/                 # 3D model files (OBJ format)
│   ├── cube.obj            # Cube OBJ file from - https://gist.github.com/MaikKlein/0b6d6bb58772c13593d0a0add6004c1c
│   ├── cube2.obj           # Another cube OBJ but uses squares instead of triangles
├── output/                 # Output directory for generated ASCII text files
├── readme_images/          # Images used in README.md
│   ├── spinning_cube.gif
│   └── print_hello_ascii.png
```

---

## Future Improvements
- Add more command-line options to `image_to_ascii.py` (like character sets).
- Implement camera controls (rotation, zoom, panning) instead of just rotating the object.
- Add option to draw edges rather than faces.
- Add unit tests to ensure calculations (projection, lighting, rotation) are performed correctly.
- Optimize rendering performance and try to remove the use of cv2.
