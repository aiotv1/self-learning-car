# Self-Learning Car (PPO & Pygame) 🚗🧠

A reinforcement learning project where a car learns to drive autonomously on custom-drawn tracks using **Proximal Policy Optimization (PPO)**. The project features a complete ecosystem to draw tracks, train the AI, watch it perform, and even race against it.

<img width="800" height="200" alt="New Pdfgfdgroject" src="https://github.com/user-attachments/assets/3409005e-1596-4321-a1b9-06d481aa5aa9" />

*(Note: Replace the link above with a screenshot of your game)*

## 🌟 Features

* **🎨 Track Maker:** Draw your own racing circuits with a built-in editor. Add start lines, obstacles (cones), and rewards (coins).
* **🤖 AI Training:** Train the car using the PPO algorithm from `stable-baselines3`. The car uses raycasting (Lidar-like sensors) to "see" the track.
* **🏁 Race Mode:** Challenge your trained AI in a 1v1 race. You control the Blue car, AI controls the Red car.
* **🪙 Reward System:** The AI is rewarded for speed and collecting coins, and penalized for crashing.

## 🛠️ Installation

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/your-username/self-learning-car.git](https://github.com/your-username/self-learning-car.git)
    cd self-learning-car
    ```

2.  **Install dependencies:**
    You can install the required libraries using the provided requirements file:
    ```bash
    pip install -r requirements.txt
    ```
    *Dependencies include: `gymnasium`, `stable-baselines3`, `pygame`, `numpy`.*

## 🚀 Usage

Run the main menu script to access all features:

```bash
python main.py
