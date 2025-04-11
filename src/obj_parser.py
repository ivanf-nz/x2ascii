import numpy as np
import os
def get_obj(obj):
    obj = os.path.join(os.path.dirname(__file__), obj)
    if not os.path.exists(obj):
        raise FileNotFoundError(f"The file {obj} does not exist.")    
    faces = []
    points = []
    with open(obj,'r') as f:
        for line in f:
            line = line.strip()

            if line.startswith('f '):
                faces.append(clean_line(line,'f')) 
            elif line.startswith('v '):
                points.append(clean_line(line,'v'))
    return points, faces

#returns a clean line as a array
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

