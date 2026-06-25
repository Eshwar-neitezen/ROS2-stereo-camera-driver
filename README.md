# ROS2 Stereo Camera Driver

A lightweight ROS2 Jazzy driver for USB global-shutter stereo cameras. Captures synchronized stereo frames, splits them into left/right streams, and publishes them as standard ROS2 image topics for perception pipelines and robot learning workflows.

---

## Installation and Requirements

### System Dependencies

Clone the repository into your ROS2 workspace:

```bash
cd ~/ros2_ws/src
git clone https://github.com/<your-username>/stereo_camera.git
```

Install required system packages:

```bash
sudo apt update
sudo apt install -y \
  python3-colcon-common-extensions \
  ros-jazzy-cv-bridge \
  python3-opencv
```

### Build the ROS2 Package

Build the stereo_camera package:

```bash
cd ~/ros2_ws
colcon build --packages-select stereo_camera
source install/setup.bash
```

---

## Hardware Configuration

| Component | Specification |
|-----------|---------------|
| Camera Model | Shenzhen Huashi J2AUG766L |
| Interface | USB Type-C |
| Shutter Type | Global Shutter |
| Sensor Configuration | Dual synchronized cameras |
| Combined Output | 4000 × 1200 pixels (2 × 2000×1200 side-by-side) |
| OS | Ubuntu 24.04 LTS |
| Middleware | ROS2 Jazzy |

---

## Software Architecture

### Perception Pipeline Design

1. **Hardware Interface** — USB stereo camera capture via OpenCV
2. **Frame Acquisition** — Global shutter ensures synchronized dual-sensor capture
3. **Frame Processing** — Split combined stereo image into independent left/right channels
4. **ROS2 Publishing** — Distribute left/right streams as standard image topics
5. **Visualization** — Real-time monitoring via Foxglove Studio
6. **Recording** — Dataset capture with rosbag2 for offline analysis

### System Components

The stereo_camera package contains a single Python node that handles the entire pipeline:

- **stereo_node.py** — Captures frames from USB camera, splits the combined stereo image, and publishes left/right streams as ROS2 Image messages.

---

## ROS2 Topics

| Topic | Message Type | Description |
|-------|--------------|-------------|
| `/left_camera/image_raw` | `sensor_msgs/msg/Image` | Left camera stream |
| `/right_camera/image_raw` | `sensor_msgs/msg/Image` | Right camera stream |

---

## Usage

### Run the Stereo Camera Node

Launch the stereo camera node:

```bash
ros2 run stereo_camera stereo_node
```

The node will begin capturing frames from the USB camera and publishing to `/left_camera/image_raw` and `/right_camera/image_raw`.

### Live Visualization with Foxglove

In a separate terminal, launch the Foxglove bridge:

```bash
ros2 launch foxglove_bridge foxglove_bridge_launch.xml
```

Connect in Foxglove Studio:
1. Open [Foxglove Studio](https://foxglove.dev/)
2. **Open Connection** → **Foxglove WebSocket**
3. Enter `ws://localhost:8765`
4. Add **Image** panels for `/left_camera/image_raw` and `/right_camera/image_raw`

### Dataset Recording and Playback

Record synchronized stereo dataset:

```bash
ros2 bag record /left_camera/image_raw /right_camera/image_raw -o stereo_dataset
```

Playback the dataset:

```bash
ros2 bag play stereo_dataset
```

---

## Repository Structure

```
stereo_camera/
├── LICENSE
├── package.xml
├── resource/
│   └── stereo_camera
├── setup.cfg
├── setup.py
├── stereo_camera/
│   ├── __init__.py
│   └── stereo_node.py
└── test/
    ├── test_copyright.py
    ├── test_flake8.py
    └── test_pep257.py
```

### Core Concepts

**Epipolar Geometry**
- Relationship between left/right image points and 3D world
- Essential for robust stereo matching

**Camera Calibration**
- Intrinsic parameters (focal length, principal point, distortion)
- Extrinsic parameters (relative pose between left/right cameras)
- Foundation for metric depth reconstruction

**Stereo Rectification**
- Transform images so corresponding points lie on same scanline
- Simplifies stereo matching algorithms
- Enables efficient hardware implementations

**Depth Estimation**
- Block matching (StereoSGBM)
- Disparity-to-depth conversion
- Point cloud generation from disparity maps

### From 2D to 3D

```
Left Image    Right Image
    ↓              ↓
    └──────────────┘
         ↓
    Stereo Matching
         ↓
    Disparity Map
         ↓
    Depth Estimation
         ↓
    3D Point Cloud
```

---

## Learning Outcomes

This project demonstrates hands-on proficiency with:

**ROS2 Core**
- Node lifecycle and composition
- Publisher/subscriber patterns
- ROS2 timers and callbacks
- Standard message types (sensor_msgs/Image)

**Image Processing**
- USB video capture with OpenCV
- Frame splitting and manipulation
- Message-based image transport
- cv_bridge integration for Mat ↔ Image conversion

**Perception Systems**
- Synchronized dual-camera acquisition
- Stereo vision fundamentals (epipolar geometry, rectification concepts)
- Dataset recording for offline analysis and machine learning

**Software Engineering**
- ROS2 Python package structure
- Code style and quality testing (flake8, pep257)
- Clean, modular node design

---

## Future Development

- [ ] Camera calibration pipeline (Kalibr integration)
- [ ] Stereo rectification
- [ ] StereoSGBM depth estimation
- [ ] 3D point cloud generation and publishing
- [ ] C++ node implementation for lower latency
- [ ] CameraInfo publisher with intrinsic/extrinsic parameters
- [ ] Parameter server for dynamic configuration
- [ ] Hardware trigger synchronization
- [ ] Performance benchmarking and profiling
- [ ] Integration with LeRobot dataset format

---

## References

**ROS2 Documentation**
- [ROS2 Jazzy Documentation](https://docs.ros.org/en/jazzy/)
- [Image Transport](http://wiki.ros.org/image_transport)
- [Rosbag2](https://index.ros.org/r/rosbag2/)

