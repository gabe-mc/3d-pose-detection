"""Main file for executing live 3d-motioncapture demo"""

import cv2
from ultralytics import YOLO
import matplotlib.pyplot as plt

from pose_detect import normalize_keypoints, extrapolate_y, compute_length, maintain_ground_level
from visualization import draw_3d_skeleton

if __name__ == "__main__":
    
    model = YOLO('models/yolo11s-pose.pt')

    # cap = cv2.VideoCapture(0)
    cap = cv2.VideoCapture("videos/full_body_motion_4.mp4")

    # Setup plot
    plt.ion()  # Interactive mode
    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')


    default_lengths = []
    default_positions = []
    ground_offset = 0
    captured = False
    prev_kpts = []
    iterations = 0
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        results = model(frame)
        poses = results[0].keypoints

        if poses is None or len(poses) == 0:
            print("No detections.")
        else:
            for idx, pose in enumerate(poses):
                kps = pose.xy[0]
                

                ############# Data transformations and extractions #############
                # Steps:
                # 1. Normalize kpts
                # 2. Call different bone extractions to get y dimension
                # 3. Call 3D draw with X,Y,Z passed in
                
                keypoints = kps.tolist()

                if iterations == 0:
                    prev_kpts = kps
                    iterations += 1
                else:
                    # normalize_keypoints(kps, prev_kpts) # Not currently being used (smoothing)
                    keypoints = maintain_ground_level(ground_offset, keypoints) # Leg normalization
                    

                if not captured: # First frame
                    ground_offset = keypoints
                    

                # We need to pad the y value of each point
                for i in range(len(keypoints)):
                    keypoints[i] += [0.5]

                if len(default_lengths) != 0:
                    for i in range(0, len(kps)):
                        keypoints[i][2] = extrapolate_y(i, keypoints, default_lengths)
                
                draw_3d_skeleton(keypoints, ax, ground_offset[15][1])

                plt.draw()
                plt.pause(0.01)
        
        cv2.imshow("Video", frame)

        
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
        elif not captured: # key == ord('c'):
            captured = True
            for index in range(len(kps.tolist())):
                default_lengths += [compute_length(index, kps.tolist())]


    cap.release()
    cv2.destroyAllWindows()