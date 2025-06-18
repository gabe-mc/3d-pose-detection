![yolo-3d-banner](https://github.com/user-attachments/assets/2a555c89-54a6-466c-8e96-2b737f9aaef9)

<p align="center">
  <a href="https://docs.ultralytics.com/tasks/pose/">
    <img src="https://img.shields.io/badge/model-Yolo11n--Pose-ff64da" alt="YOLOv11" />
  </a>
  <img src="https://img.shields.io/github/repo-size/gabe-mc/3d-pose-detection?color=51f160" alt="Repo size" />
  <img src="https://img.shields.io/badge/repo%20created-June%2016%2C%202025-ff64da" alt="Repo created" />
  <a href="https://github.com/gabe-mc/3d-pose-detection/commits">
    <img src="https://img.shields.io/github/last-commit/gabe-mc/3d-pose-detection" alt="GitHub last commit" />
  </a>
  <a href="https://github.com/gabe-mc/3d-pose-detection/blob/main/LICENSE">
    <img src="https://img.shields.io/github/license/gabe-mc/3d-pose-detection?color=ff64da" alt="License" />
  </a>
</p>



YOLO-3D is an extension of the 2D Ultralytics [YOLO pose model](https://docs.ultralytics.com/tasks/pose/), lifting the pose output of YOLO to a third dimension though vector computations, thus requiring neglagble extra compute on top of YOLO. The resulting model allows for 3D motion capture in real time on a sufficiently performant CPU, when using YOLO's nano pose model.

## Overview

**YOLO-3D** extends 2D skeleton output from YOLO by inferring a third spatial dimension using geometric constraints. Assuming that human bone lengths remain constant over time, the model uses this consistency to reconstruct the Z-dimension. Specifically, when a bone appears shorter in 2D due to foreshortening, the depth component `y` can be extrapolated using the relation:

$$
y = \sqrt{l^2 - x^2}
$$

where:  
- `l` is the true (3D) bone length established from an initial calibration  
- `x` is the observed 2D length  
- `y` is the inferred depth offset required to preserve length `l` in 3D space

The model requires a **calibration pose** — a frame captured with the subject in a known, approximately flat or neutral body position. This frame is used to calculate default bone lengths and define the ground level. Once this initial calibration is complete, 3D projection can be performed in real-time.

<p align="center">
  <img src="https://github.com/user-attachments/assets/8bb135a1-e242-4013-b487-dd19c2592858" width="400" alt="running-demo" />
</p>

Real-time inference is achievable on CPU using the lightweight YOLO11n model. To mitigate noise and jitter from the reduced model size, several normalization and smoothing functions are applied.


## Performance

Thorough testing is still needed to evaluate performance across various devices. Below is the current benchmark data with YOLO11n Nano:

| Device               | FPS  |
|----------------------|--------------------|
| MacBook Pro M1 Max (CPU) | 16 FPS         |

## Usage

To use YOLO-3D locally, follow these steps:

### 1. Clone the Repository

Fork the repository to your own account and then clone it to your local machine:

```bash
git clone https://github.com/your-username/yolo-3d.git
cd yolo-3d
```

### 2. Install Dependencies

Install the required Python packages listed in `requirements.txt`:

```bash
pip install -r requirements.txt
```

### 3. Choose input source

To use YOLO-3D in real-time, ensure that at the top of `main.py` you have chosen `model = YOLO('models/yolo11n-pose.pt')` and have `cap = cv2.VideoCapture(0)`. 

If you would like to draw from a prerecorded source, instead set `cap = cv2.VideoCapture("path_to_your_video/your_video_here.mp4")` ensuring your video is in mp4 format. 

While YOLO11n (nano) is recommended for real-time processing, you’re welcome to experiment with the small (s) or medium (m) models for prerecorded videos. Keep in mind that performance improvements tend to plateau beyond the medium model size.

### 4. Run the Model

After setup, you're ready to run YOLO-3D. From the project root directory, run:

```bash
python src/main.py
```

This will launch a 3D visualization window using Matplotlib, along with a playback window of your input video through OpenCV.

## Limitations and Next Steps

There is still significant work needed to refine this model for deployment. Key issues that require attention include:

1. Backward leg movement is jittery and needs improved tolerance parameters.
2. Jumping is not supported, as the model assumes at least one leg remains fixed to ground level.
3. Calf bone lengths are inconsistent due to the current ground normalization process.

Overall, distinguishing between forward and backward movement is the main source of error in this project and will likely require further research and potentially new techniques to resolve.


