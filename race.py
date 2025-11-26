import gymnasium as gym
from stable_baselines3 import PPO
from car_env import CarRacingEnv
import pygame
import numpy as np
import math
import sys

def main():
    # 1. Init Environment (No internal rendering)
    env = CarRacingEnv(render_mode=None)
    obs, info = env.reset()
    
    # 2. Load AI Model
    try:
        model = PPO.load("ppo_car_racing")
    except:
        print("Model not found. Please train first.")
        return

    # 3. Setup Pygame Window (We handle it manually here)
    pygame.init()
    screen = pygame.display.set_mode((env.width, env.height))
    pygame.display.set_caption("Race: You (Blue) vs AI (Red)")
    clock = pygame.time.Clock()
    
    # 4. User Car Setup
    # Start at same position as AI
    user_pos = list(env.car_pos)
    user_angle = env.car_angle
    user_speed = 0
    
    # Load User Car Image (Blue)
    try:
        user_img = pygame.image.load("car.png")
        user_img = pygame.transform.scale(user_img, (30, 15))
        # Tint it blue (simple way: fill a surface with blue and multiply)
        color_surface = pygame.Surface(user_img.get_size()).convert_alpha()
        color_surface.fill((0, 0, 255, 100)) # Blue tint
        user_img.blit(color_surface, (0,0), special_flags=pygame.BLEND_RGBA_MULT)
    except:
        user_img = pygame.Surface((30, 15), pygame.SRCALPHA)
        user_img.fill((0, 0, 255)) # Blue rectangle

    running = True
    while running:
        # Event Handling
        keys = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                
        # --- AI Logic ---
        action, _ = model.predict(obs)
        obs, reward, done, truncated, info = env.step(action)
        if done or truncated:
            # AI crashed or finished, reset AI only? 
            # For a race, if AI crashes, it respawns or loses. 
            # Let's just reset AI to start for now to keep it going.
            obs, info = env.reset()
            
        # --- User Logic ---
        # Controls: Arrows
        if keys[pygame.K_LEFT]:
            user_angle -= 5
        if keys[pygame.K_RIGHT]:
            user_angle += 5
        if keys[pygame.K_UP]:
            user_speed += 0.2
        if keys[pygame.K_DOWN]:
            user_speed -= 0.2
            
        # Friction
        user_speed *= 0.95
        user_speed = np.clip(user_speed, -2, 5) # Max speed 5
        
        # Move
        rad = math.radians(user_angle)
        user_pos[0] += math.cos(rad) * user_speed
        user_pos[1] += math.sin(rad) * user_speed
        
        # Collision Check (User)
        user_crashed = False
        if not env._is_valid(user_pos[0], user_pos[1]):
            user_crashed = True
            # Respawn User at start (or just stop)
            # Let's respawn at AI start pos for simplicity or just bounce
            user_speed = -user_speed * 0.5 # Bounce
            
        # --- Rendering ---
        screen.blit(env.track_surface, (0, 0))
        
        # Draw AI Car (Red)
        # We need to access env's car image if possible, or just load it again.
        # env.car_img is available
        rotated_ai = pygame.transform.rotate(env.car_img, -env.car_angle)
        rect_ai = rotated_ai.get_rect(center=(int(env.car_pos[0]), int(env.car_pos[1])))
        screen.blit(rotated_ai, rect_ai.topleft)
        
        # Draw User Car (Blue)
        rotated_user = pygame.transform.rotate(user_img, -user_angle)
        rect_user = rotated_user.get_rect(center=(int(user_pos[0]), int(user_pos[1])))
        screen.blit(rotated_user, rect_user.topleft)
        
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    env.close()

if __name__ == "__main__":
    main()
