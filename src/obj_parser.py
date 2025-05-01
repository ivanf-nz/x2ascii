import numpy as np
import os


def get_obj(obj_path_or_name):
    script_dir = os.path.dirname(__file__)

    # Attempt 1: Path relative to ../models/
    model_path = os.path.abspath(os.path.join(
        script_dir, '..', 'models', obj_path_or_name))

    # Attempt 2: Path relative to script directory (src/)
    relative_path = os.path.abspath(os.path.join(script_dir, obj_path_or_name))

    # Determine the correct path
    if os.path.exists(model_path):
        resolved_path = model_path
    elif os.path.exists(relative_path):
        resolved_path = relative_path
    else:
        # If neither path worked, raise an error
        raise FileNotFoundError(
            f"Could not find '{obj_path_or_name}'. Checked:\n"
            f"- {model_path}\n"
            f"- {relative_path}"
        )

    print(f"Loading model from: {resolved_path}")  # Optional: confirm path
    faces = []
    points = []
    with open(resolved_path, 'r') as f:
        for line in f:
            line = line.strip()

            if line.startswith('f '):
                faces.append(clean_line(line, 'f'))
            elif line.startswith('v '):
                points.append(clean_line(line, 'v'))
    return points, faces

# returns a clean line as a array


def clean_line(line, funct):
    clean_line = line.split('#')[0].strip()
    clean_line = clean_line[2:]
    if funct == 'f':
        points = clean_line.split()
        clean_line = [point.split('/')[0] for point in points]

        clean_line = " ".join(clean_line)
        clean_line = [int(x) for x in clean_line.split()]
        clean_line = [x - 1 for x in clean_line]
    elif funct == 'v':
        clean_line = [float(x) for x in clean_line.split()]
        clean_line = np.array(clean_line)
    return clean_line
