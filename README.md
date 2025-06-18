![yolo-3d-banner](https://github.com/user-attachments/assets/2a555c89-54a6-466c-8e96-2b737f9aaef9)


<a name="top"></a>

[![Python](https://img.shields.io/badge/Python-3ebeee?logo=python&logoColor=fff)](https://www.python.org/)
[![YOLOv11](https://img.shields.io/badge/model-Yolo11n--Pose-ff64da)](https://docs.ultralytics.com/tasks/pose/)
![Repo size](https://img.shields.io/github/repo-size/gabe-mc/3d-pose-detection?color=51f160)
![Repo created](https://img.shields.io/badge/repo%20created-June%2016%2C%202025-ff64da)
[![GitHub last commit](https://img.shields.io/github/last-commit/gabe-mc/3d-pose-detection)](https://github.com/gabe-mc/3d-pose-detection/commits)
[![License](https://img.shields.io/github/license/gabe-mc/3d-pose-detection?color=ff64da)](https://github.com/gabe-mc/3d-pose-detection/blob/main/LICENSE)


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


# Performance


# Usage

# Limitations and Next Steps


