"""A 3D visualization of the pose tracking"""

"""Use YOLO to detect poses and extrapolate 3D data from there."""

import numpy as np

def draw_3d_skeleton(point_pairs, ax, ground_offset):
    ax.cla()
    IMG_W, IMG_H, IMG_Y = 1920, 1080, 1500

    # Define your bones in terms of joint‐indices 0…N−1
    skeleton = [
        (0, 1), (0, 2), (1, 3), (2, 4),
        (5, 6), (5, 7), (7, 9), (6, 8), (8, 10),
        (5, 11), (6, 12), (11, 12),
        (11, 13), (13, 15), (12, 14), (14, 16)
    ]

    # Build a full‐length list of (x, y, z) or None
    coords3d = []
    for x_img, z_img, y_img in point_pairs:
        
        if x_img == 0.0 and z_img == 0.0:
            coords3d.append(None)
        else:
            x = (x_img / IMG_W)
            z = ((z_img - ground_offset) / IMG_H) + 1
            y = 0.5 - (y_img / IMG_Y)
            coords3d.append((x, y, z))

    # Extract valid scatter points
    xs = [c[0] for c in coords3d if c is not None]
    ys = [c[1] for c in coords3d if c is not None]
    zs = [c[2] for c in coords3d if c is not None]

    ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.set_zlim(0, 1)
    ax.invert_zaxis()  # Flips the Z-axis so 0 is at the bottom and 1 is at the top
    ax.set_xlabel('X'); ax.set_ylabel('Y'); ax.set_zlabel('Z')

    # Draw joints
    if coords3d[14] is not None:
        x8, y8, z8 = coords3d[15]
        ax.scatter(x8, y8, z8, s=15)

    # Draw bones
    for i, j in skeleton:
        pi = coords3d[i]
        pj = coords3d[j]
        if pi is None or pj is None:
            continue
        xi, yi, zi = pi
        xj, yj, zj = pj
        ax.plot([xi, xj], [yi, yj], [zi, zj])
