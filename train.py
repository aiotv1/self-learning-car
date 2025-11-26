import gymnasium as gym
from stable_baselines3 import PPO
from stable_baselines3.common.callbacks import BaseCallback
from car_env import CarRacingEnv
import pygame
import os

class StopTrainingCallback(BaseCallback):
    def __init__(self, verbose=0):
        super(StopTrainingCallback, self).__init__(verbose)

    def _on_step(self) -> bool:
        # Check for Q key to stop training
        keys = pygame.key.get_pressed()
        if keys[pygame.K_q]:
            print("\nTraining interrupted by user!")
            return False # Stop training
        return True

def main():
    # Create environment
    env = CarRacingEnv(render_mode="human") # render_mode="human" to see it training (slow)
    
    # Initialize Agent
    try:
        model = PPO.load("ppo_car_racing", env=env, verbose=1)
        print("Loaded existing model to continue training.")
    except:
        model = PPO("MlpPolicy", env, verbose=1)
        print("Created new model.")
    
    print("Starting training... Press 'Q' to stop and save.")
    
    # Train
    TIMESTEPS = 50000
    callback = StopTrainingCallback()
    model.learn(total_timesteps=TIMESTEPS, callback=callback)
    
    # Save
    model.save("ppo_car_racing")
    print("Model saved as ppo_car_racing.zip")
    
    env.close()

if __name__ == "__main__":
    main()
