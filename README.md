# ROS2 Stereo Camera Driver

A lightweight ROS2 Jazzy driver for USB global-shutter stereo cameras. Captures synchronized stereo frames, splits them into left/right streams, and publishes them as standard ROS2 image topics for perception pipelines and robot learning workflows.

---

## Installation and Requirements

### C++ / System Dependencies

```bash
cd /home/$USER/workspace/
git clone https://github.com/<your-username>/ros2_stereo_camera_driver.git
cd ros2_stereo_camera_driver
```

Install required system packages:

```bash
sudo apt update
sudo apt install -y \
  build-essential \
  cmake \
  python3-colcon-common-extensions \
  ros-jazzy-cv-bridge \
  ros-jazzy-image-transport \
  python3-opencv \
  libopencv-dev
```

### Build the ROS2 Package

Assuming you have a ROS2 Jazzy workspace at `~/ros2_ws`:

```bash
cd ~/ros2_ws/src
git clone https://github.com/<your-username>/ros2_stereo_camera_driver.git
cd ~/ros2_ws
colcon build --packages-select ros2_stereo_camera_driver
source install/setup.bash
```

### Python Dependencies

Create a conda environment (optional but recommended):

```bash
conda create -n stereo_driver python=3.12 -y
conda activate stereo_driver
```

Install Python packages:

```bash
pip install opencv-python
pip install numpy
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
| Frame Rate | Up to 60 FPS |
| OS | Ubuntu 24.04 LTS |
| Middleware | ROS2 Jazzy |

---

## Software Architecture

### Perception Pipeline Design

1. **Hardware Interface** — USB frame capture via OpenCV
2. **Synchronization** — Global shutter ensures frame alignment
3. **Frame Processing** — Split combined stereo image into independent channels
4. **ROS2 Publishing** — Distribute left/right streams as standard image topics
5. **Visualization** — Real-time monitoring via Foxglove Studio
6. **Recording** — Dataset capture with rosbag2 for offline analysis

### System Components

- **stereo_camera_node.py** — Main capture and publisher node
- **frame_splitter.py** — Image splitting and preprocessing logic
- **camera_params.yaml** — Configuration and topic parameters
- **stereo_camera.launch.py** — Launch file for integrated bring-up

---

## ROS2 Topics

| Topic | Message Type | Description |
|-------|--------------|-------------|
| `/left_camera/image_raw` | `sensor_msgs/msg/Image` | Left camera stream |
| `/right_camera/image_raw` | `sensor_msgs/msg/Image` | Right camera stream |

---

## Usage

### Run the Driver Node

```bash
ros2 run ros2_stereo_camera_driver stereo_camera_node
```

Or use the launch file for integrated bring-up with Foxglove bridge:

```bash
ros2 launch ros2_stereo_camera_driver stereo_camera.launch.py
```

### Live Visualization with Foxglove

Launch the Foxglove bridge:

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
ros2_stereo_camera_driver/
├── stereo_camera_driver/
│   ├── __init__.py
│   ├── stereo_camera_node.py      # Main node
│   └── frame_splitter.py          # Frame processing
├── launch/
│   └── stereo_camera.launch.py
├── config/
│   └── camera_params.yaml
├── resource/
│   └── ros2_stereo_camera_driver
├── test/
│   ├── test_flake8.py
│   └── test_pep257.py
├── package.xml
├── setup.py
├── setup.cfg
├── LICENSE
└── README.md
```

---

## Robotics Concepts and Design Principles

### Perception Pipeline Fundamentals

1. **Sensor Synchronization**
   - Global shutter ensures no rolling-shutter artifacts
   - Dual cameras capture at identical timestamps
   - Critical for stereo correspondence

2. **Image Transport & Message Passing**
   - Standard ROS2 `sensor_msgs/Image` format
   - cv_bridge for OpenCV ↔ ROS2 conversion
   - Efficient topic-based distribution

3. **Real-Time Constraints**
   - Fixed-rate frame capture with ROS2 timers
   - Predictable publishing latency
   - Foundation for real-time perception systems

### System Design Patterns

- **Node Composition** — Standalone node for modularity and reusability
- **Topic-Based Communication** — Decoupled from downstream consumers
- **Configuration via YAML** — Parameters for resolution, FPS, exposure
- **Rosbag2 Integration** — Separation of collection and processing

### Programmer Ethics in Robotics

Perception systems are foundational to autonomous behavior. Responsible development requires:

- **Data Integrity** — Ensure synchronized, calibrated sensor streams
- **Transparency** — Document sensor limitations and failure modes
- **Testing** — Validate in diverse lighting and environmental conditions
- **Traceability** — Maintain recorded datasets for auditing and debugging
- **Safety** — Monitor frame rates and latency; alert on degradation
- **Privacy** — Handle visual data with appropriate access controls

---

## Stereo Vision Fundamentals

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
- Launch file configuration

**Image Processing**
- USB video capture with OpenCV
- Frame splitting and preprocessing
- Message-based image transport
- cv_bridge integration

**Perception Systems**
- Synchronized multi-camera acquisition
- Stereo vision fundamentals
- Sensor fusion pipelines
- Dataset recording for machine learning

**Software Engineering**
- Clean module organization
- Configuration management
- Real-time system design
- Testing and debugging

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

**Stereo Vision & Calibration**
- [Kalibr IMU and Camera Calibration](https://github.com/ethz-asl/kalibr)
- [OpenCV Stereo Vision](https://docs.opencv.org/4.x/dd/d53/tutorial_py_depthmap.html)
- [Multiple View Geometry in Computer Vision](https://www.robots.ox.ac.uk/~vgg/hzbook/)

**Robotics & Perception**
- [Probabilistic Robotics (Thrun, Burgard, Fox)](https://mitpress.mit.edu/9780262201629/probabilistic-robotics/)
- [State Estimation for Robotics (Barfoot)](https://www.cambridge.org/core/books/state-estimation-for-robotics/E07C7A2B2D4F1F0F1F1F1F1F1F1F1F1F)

---

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.

---

## Contributing

Contributions are welcome. Please ensure:
- Code follows PEP 8 style guidelines
- New features include tests
- Documentation is updated
- Commits are descriptive

For bug reports or feature requests, open an issue on GitHub.

---

## Acknowledgments

Built as a foundation for stereo perception research and robot learning pipelines. Designed with extensibility in mind for future integration with calibration, rectification, depth estimation, and imitation learning frameworks.
