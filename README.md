# 🧊 Inverted 3D Cube: Gesture-Controlled Simulation

A Python-based 3D wireframe and solid-face simulation that uses Computer Vision to manipulate geometry. Unlike standard simulations, this project features an **Inverted Scaling Mechanic**—where the object grows larger as your hand moves further away.

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![MediaPipe](https://img.shields.io/badge/MediaPipe-007f00?style=for-the-badge&logo=google&logoColor=white)
![Pygame](https://img.shields.io/badge/Pygame-3c73ad?style=for-the-badge&logo=python&logoColor=white)

---

## 💡 The Concept
This project explores the relationship between real-world depth and virtual scaling. By calculating the Euclidean distance between hand landmarks, the engine dynamically adjusts the 3D projection matrix.

- **Far = Big**: As your hand recedes, the cube scales up.
- **Close = Small**: As your hand approaches, the cube shrinks.

## 🚀 Features
- **Real-time 3D Projection**: Converts 3D coordinates $(x, y, z)$ into 2D screen space.
- **Depth Sorting (Painters Algorithm)**: Faces are rendered based on Z-depth to ensure correct overlapping.
- **Dynamic Shading**: Face brightness changes based on rotation and distance.
- **Hand Gesture Control**:
  - **Pitch**: Vertical hand movement.
  - **Roll**: Wrist rotation.
  - **Scale**: Hand-to-camera distance.

## 🛠️ Installation

1. **Clone the repo:**
   ```bash
   git clone [https://github.com/YOUR_USERNAME/Inverted-3D-Cube.git](https://github.com/YOUR_USERNAME/Inverted-3D-Cube.git)

   Install Dependencies:
   pip install pygame mediapipe opencv-python numpy

   Run Simulation:Bashpython cube_sim.py
🎮 ControlsW Key: Toggle between Wireframe and Solid Face mode.Q Key: Quit the application.
Hand: Move and rotate your hand to interact with the cube.

## 📝 Mathematical Logic

The projection uses a focal length formula to map 3D coordinates to a 2D plane:

$$f(z) = \frac{focal\_length}{z + z\_offset}$$

The scaling is handled via `numpy.interp` to map the hand-to-camera distance to the cube's size. This creates the "Inversion" effect:

| Hand Distance (px) | Resulting Cube Scale |
|--------------------|----------------------|
| 60 (Far)           | 300 (Large)          |
| 220 (Close)        | 50 (Small)           |

---Developed by Jemeli Mercy