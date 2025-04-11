# x2ascii

x2ascii is a Python project that converts 3D models (OBJ files) and images into ASCII art. It includes tools for rendering 3D objects as ASCII in the terminal and converting images into ASCII text files.

<img src="https://github.com/user-attachments/assets/e886bc03-a480-4845-895f-f8f832e1f0df" alt="ascii_cube" width="300" height="300">
<img width="650" alt="image" src="https://github.com/user-attachments/assets/bf9367cf-ef32-46a2-9e1d-d3b6004928ba" />

---

## Features

- **3D Model Rendering**: Render 3D OBJ files as ASCII art in the terminal using perspective projection and lighting.
- **Image to ASCII Conversion**: Convert images (JPG/PNG) into ASCII text files.
- **OBJ File Cleaning**: Automatically parses and cleans OBJ files to extract vertices and faces.

---

## File Descriptions

### `src/render_ascii.py`
- Renders 3D objects as ASCII art in the terminal.
- Supports lighting and face visibility calculations.
- Allows rotation of objects and camera adjustments.

### `src/image_to_ascii.py`
- Converts images into ASCII text files.
- Input the image name (with extension) when prompted.
- Outputs the ASCII art directly to the terminal and a text file in output/ directory.

### `src/obj_parser.py`
- Parses and cleans OBJ files to extract vertices and faces.
- Provides utility functions for processing OBJ files.

---

## Usage

### Rendering 3D Models
1. Place your OBJ file in the `models/` directory.
2. Update the `obj` variable in `src/render_ascii.py` with the name of your OBJ file.
3. Run the script:
   ```bash
   python3 src/render_ascii.py
   ```

### Converting Images to ASCII
1. Place your image file (JPG/PNG) in the project directory.
2. Run the script:
   ```bash
   python3 src/image_to_ascii.py
   ```
3. Enter the image location when prompted.
4. The ASCII art will be displayed directly in the terminal and a text file to the output/ directory.

---

## Project Hierarchy

```
x2ascii/
├── README.md               # Project documentation
├── src/                    # Source code
│   ├── render_ascii.py     # Renders 3D models as ASCII art
│   ├── image_to_ascii.py   # Converts images to ASCII art
│   ├── obj_parser.py       # Parses and cleans OBJ files
├── models/                 # 3D model files
│   ├── cube.obj            # Cube OBJ file from - https://gist.github.com/MaikKlein0b6d6bb58772c13593d0a0add6004c1c
│   ├── cube2.obj           # Another cube OBJ but uses squares instead of triangles
├── output/                 # Output directory for ASCII text files
```

---

## Future Improvements
- Add command-line options to `render_ascii.py` and `image_to_ascii.py` to allow customization of rendering parameters, such as object rotation, camera position, and lighting settings.
- Add unit tests to ensure calculations and other methods are being preformed correctly.
