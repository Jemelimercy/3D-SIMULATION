# 3D Cuboid  Simulation 🧊🔥

An interactive 3D simulation built with **Python**, **Pygame**, and **MediaPipe**. This project allows users to control a solid 3D cuboid using real-time hand tracking and orientation.

## 🚀 Features
- **3D Solid Rendering:** Uses Z-sorting (Painter's Algorithm) and perspective projection to render a solid, multi-colored cube.
- **Hand Gesture Control:** - **Rotation:** Tilt your palm (Pitch/Roll) to rotate the cube in 3D space.
  - **Inverted Scaling:** Move your hand closer to the camera to shrink the cube, and further away to make it larger.
- **Visual Modes:** Toggle between a solid-face mode and a **Wireframe Mode** by pressing the `W` key.
- **Dynamic Shading:** Faces darken based on depth ($z$-axis) to enhance the 3D effect.

## 🛠️ Tech Stack
- **Language:** Python 3.11+
- **Computer Vision:** MediaPipe (Hand Landmarking)
- **Graphics:** Pygame
- **Math:** NumPy & Trigonometric Rotation Matrices

## 📦 Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/Jemelimercy/3D-SIMULATION.git](https://github.com/Jemelimercy/3D-SIMULATION.git)
   cd 3D-SIMULATION

   Install Dependencies:
   pip install pygame mediapipe opencv-python numpy

   Run Simulation:
python cube_sim.py

🎮 Controls
W Key: Toggle between Wireframe and Solid Face mode.

Q Key: Quit the application.

Hand: Move and rotate your hand to interact with the cube

  📝 Mathematical LogicThe projection uses a focal length formula:
  $$f(z) = \frac{\text{focal\_length}}{z + z\_offset}$$
  The scaling is handled via numpy.interp to map hand distance $(60, 220)$ to cube scale $(300, 50)$.
  
  Developed by Jemeli Mercy