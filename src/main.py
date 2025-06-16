"""Main file for executing live 3d-motioncapture demo"""

import cv2
from ultralytics import YOLO
import matplotlib.pyplot as plt

from pose_detect import normalize_keypoints, extrapolate_y, compute_length
from visualization import draw_3d_skeleton

if __name__ == "__main__":
    
    model = YOLO('models/yolo11m-pose.pt')

    # cap = cv2.VideoCapture(0)
    cap = cv2.VideoCapture("videos/full_body_motion_4.mp4")

    # Setup plot
    plt.ion()  # Interactive mode
    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')


    captured_lengths = []
    ground_offset = 0
    captured = False
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        results = model(frame)
        poses = results[0].keypoints

        iterations = 0
        prev_kpts = []
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
                if iterations == 0:
                    prev_kpts = kps
                    iterations += 1
                else:
                    normalize_keypoints(kps, prev_kpts)
                    

                prev_kpts = kps
                keypoints = kps.tolist()

                if not captured: # First frame
                    ground_offset = keypoints[15][1]
                    

                # We need to pad the y value of each point
                for i in range(len(keypoints)):
                    keypoints[i] += [0.5]

                if len(captured_lengths) != 0:
                    for i in range(0, len(kps)):
                        keypoints[i][2] = extrapolate_y(i, keypoints, captured_lengths)
                
                draw_3d_skeleton(keypoints, ax, ground_offset)

                plt.draw()
                plt.pause(0.01)
        
        cv2.imshow("Video", frame)

        
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
        elif not captured: # key == ord('c'):
            captured = True
            for index in range(len(kps.tolist())):
                captured_lengths += [compute_length(index, kps.tolist())]


    cap.release()
    cv2.destroyAllWindows()