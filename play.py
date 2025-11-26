import gymnasium as gym
from stable_baselines3 import PPO
from car_env import CarRacingEnv

def main():
    env = CarRacingEnv(render_mode="human")
    
    # Load model
    try:
        model = PPO.load("ppo_car_racing")
    except:
        print("Model not found. Please run train.py first.")
        return

    obs, info = env.reset()
    done = False
    
    while True:
        action, _states = model.predict(obs)
        obs, reward, done, truncated, info = env.step(action)
        
        if done or truncated:
            obs, info = env.reset()

if __name__ == "__main__":
    main()
