"""Use YOLO to detect poses and extrapolate 3D data from there."""

import math

def compute_length(index: int, xz_pairs: list[list]):
    x1, z1 = xz_pairs[index]
    x2, z2 = xz_pairs[index - 2]
    return math.hypot(x2 - x1, z2 - z1)


def extrapolate_y(index: int, xz_pairs: list[tuple], default_lengths: list[list]) -> float:
    """Computes the implicit Y component from a sequence of (X, Z) coordinate pairs.

    Args:
        index (int): The index of the point in the (X, Z) list we want to compute Y for
        xz_pairs (list[tuple]): A list of (x, z) coordinate pairs.

    Returns:
        float: The extrapolated Y value.
    """

    # Compute Forearms
    if index == 9 or index == 10:
        x1, z1, y1 = xz_pairs[index]
        x2, z2, y2 = xz_pairs[index - 2]

        bone_length = default_lengths[index] # This will get the hypotenuse for the 2D right triangle
        y_dim = math.sqrt(max(50, bone_length**2 - (x2-x1)**2 - (z2-z1)**2)) # This will get the 3D Y dimension

        # bound_forearm_angle(index, xz_pairs) # Fix any errors in the forearm angles

        return y_dim
        
    # Compute Shoulders
    if index == 7 or index == 8:
        x1, z1, y1 = xz_pairs[index]
        x2, z2, y1 = xz_pairs[index - 2]

        bone_length = default_lengths[index] # This will get the hypotenuse for the 2D right triangle
        y_dim = math.sqrt(max(50, bone_length**2 - (x2-x1)**2 - (z2-z1)**2)) # This will get the 3D Y dimension
        
        return y_dim - 35

    # Leave others as default

    # Compute knees
    if index == 13 or index == 14:
        x1, z1, y1 = xz_pairs[index]
        x2, z2, y1 = xz_pairs[index - 2]
        
        bone_length = default_lengths[index]
        
        y_dim = math.sqrt(max(50, bone_length**2 - (x2-x1)**2 - (z2-z1)**2)) # This will get the 3D Y dimension
        
        return y_dim * 0.75 # Decrease multiplier to strighten
    

    # Compute feet
    if index == 15 or index == 16:
        x1, z1, y1 = xz_pairs[index]
        x2, z2, y1 = xz_pairs[index - 2]
        
        bone_length = default_lengths[index]
        
        y_dim = math.sqrt(max(50, bone_length**2 - (x2-x1)**2 - (z2-z1)**2)) # This will get the 3D Y dimension
        
        y_dim = bound_calf_angle(index, xz_pairs, y_dim)
        
        return y_dim
    
    else:
        return 0.5


def bound_forearm_angle(index: int, keypoints: list[list]):

        x1, z1, y1 = keypoints[index]
        x2, z2, y2 = keypoints[index - 2]

        # Check if the angle between the elbow and forarm is correct
        x2_shoulder, z2_shoulder, y2_shoulder = keypoints[index - 2]
        x1_shoulder, z1_shoulder, y1_shoulder = keypoints[index - 4]
        shoulder_vector = (y2_shoulder - y1_shoulder, z2_shoulder - z1_shoulder)
        elbow_vector = (y2 - y1, z2 - z1)

        angle_shoulder = math.degrees( math.atan2(shoulder_vector[0], shoulder_vector[1]))
        angle_elbow = math.degrees( math.atan2(elbow_vector[0], elbow_vector[1]))
        
        if abs(angle_elbow) >= abs(angle_shoulder):
            # forearm is equal-or-more tilted than upper arm -> nudge y
            keypoints[index][2] = elbow_vector[1] * math.tan(math.radians(angle_shoulder))

        return None

def bound_calf_angle(index: int, keypoints: list[list], extrapolated_y: float):
        """We are checking the x component of the line segment, and if the y component of the calf is greater 
        than the y component of the quad, then we have an overstreched bone"""
        x1, z1, y1 = keypoints[index] # Foot
        x2, z2, y2 = keypoints[index - 2] # Knee
        x3, z3, y3 = keypoints[index - 4] # Hip

        knee_angle_dimension = y2 - y3
        foot_angle_dimension = extrapolated_y - y2
        
        if foot_angle_dimension > knee_angle_dimension: # Overstreched
            extrapolated_y = y2

        return extrapolated_y
        


def normalize_keypoints(curr: list[float], prev: list[float], tolerance: float=0.01)-> list[float]:
    """Attempts to fix bone order inconsistencies by comparing with the previous frame, fixes ordering in-place.

    Args:
        curr (list[float]): The current frame's bone positions.
        prev (list[float]): The previous frame's bone positions.
        tolerance (float): Changes the tolerance for different positions to be the "same". Default: 0.01
    """
    iterations = 0

    if len(curr) != len(prev):
        curr = prev
        return None # Go back to last frame if keypoints have lost a point

    for i in range(len(curr)):
        if iterations == 0:
            iterations += 1
        else:
            if abs(prev[0][i] - curr[0][i]) > tolerance and abs(prev[2][i] - curr[2][i]) > tolerance:
                # This means the bones are in a different order than before
                if abs(prev[0][i+1] - curr[0][i+1]) > tolerance and abs(prev[2][i+1] - curr[2][i+1]) > tolerance:
                    curr[i], curr[i+1] = curr[i+1], curr[i] # swap forwards
                else:
                    Exception("ERROR! Could not reorder properly")

    return None