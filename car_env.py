import gymnasium as gym
from gymnasium import spaces
import numpy as np
import pygame
import math

class CarRacingEnv(gym.Env):
    metadata = {"render_modes": ["human", "rgb_array"], "render_fps": 60}

    def __init__(self, render_mode=None):
        super(CarRacingEnv, self).__init__()
        
        self.render_mode = render_mode
        self.width = 800
        self.height = 600
        
        # Load track
        try:
            self.track_surface = pygame.image.load("track.png")
            self.track_array = pygame.surfarray.array3d(self.track_surface)
        except:
            # Fallback if track doesn't exist yet
            self.track_surface = pygame.Surface((self.width, self.height))
            self.track_surface.fill((255, 255, 255))
            self.track_array = pygame.surfarray.array3d(self.track_surface)
            print("Warning: track.png not found. Please run track_maker.py first.")

        # Load car image
        try:
            self.car_img = pygame.image.load("car.png")
            self.car_img = pygame.transform.scale(self.car_img, (30, 15))
        except:
            self.car_img = pygame.Surface((30, 15), pygame.SRCALPHA)
            self.car_img.fill((255, 0, 0))
            print("Warning: car.png not found, using red rectangle.")

        # Action space: [Steering (-1 to 1), Acceleration (0 to 1)]
        # We'll simplify: Discrete actions for easier training initially? 
        # No, let's use Continuous for "real" driving or Discrete for simplicity.
        # User asked for "Car learns by itself", usually PPO + Continuous is good.
        # But Discrete is often faster to learn for simple games.
        # Let's go with Discrete: 0: Do nothing, 1: Left, 2: Right, 3: Accelerate, 4: Brake
        self.action_space = spaces.Discrete(5)
        
        # Observation space: 5 Raycasts distances
        self.observation_space = spaces.Box(low=0, high=1000, shape=(5,), dtype=np.float32)
        
        self.window = None
        self.clock = None
        
        self.car_pos = [400, 300] # Start middle
        self.car_angle = 0
        self.car_speed = 0
        self.max_speed = 5
        
    def reset(self, seed=None, options=None):
        super().reset(seed=seed)
        
        # Find Start Line (Green pixels: 0, 255, 0)
        start_pixels = []
        # Scan for Green
        # Note: track_array is [x, y, c]
        # Green is roughly [0, 255, 0]
        # We check for high Green and low Red/Blue
        
        # Optimization: Don't scan every pixel every reset if possible, but for now it's fine
        # Or we can cache it. Let's scan once or just scan.
        
        # Let's try to find green pixels
        # We can use numpy for speed
        # condition: R < 50, G > 200, B < 50
        mask = (self.track_array[:, :, 1] > 200) & (self.track_array[:, :, 0] < 50) & (self.track_array[:, :, 2] < 50)
        start_indices = np.argwhere(mask)
        
        if len(start_indices) > 0:
            # Pick center of start line
            center_idx = len(start_indices) // 2
            self.car_pos = list(start_indices[center_idx])
            # Ensure float for smooth movement
            self.car_pos = [float(self.car_pos[0]), float(self.car_pos[1])]
        else:
            # Fallback to random white if no green found
            found = False
            for i in range(2000):
                x = np.random.randint(50, self.width - 50)
                y = np.random.randint(50, self.height - 50)
                if self._is_valid(x, y):
                    self.car_pos = [x, y]
                    found = True
                    break
            if not found:
                 self.car_pos = [400, 300]

        self.car_angle = 0
        self.car_speed = 0
        self.steps_since_reset = 0
        
        observation = self._get_obs()
        info = {}
        return observation, info

    def step(self, action):
        self.steps_since_reset += 1
        
        # Action logic
        # 0: Nothing, 1: Left, 2: Right, 3: Accel, 4: Brake
        if action == 1:
            self.car_angle -= 5
        elif action == 2:
            self.car_angle += 5
        elif action == 3:
            self.car_speed += 0.2
        elif action == 4:
            self.car_speed -= 0.2
            
        # Friction
        self.car_speed *= 0.95
        
        # Cap speed
        self.car_speed = np.clip(self.car_speed, -2, self.max_speed)
        
        # Move car
        rad = math.radians(self.car_angle)
        self.car_pos[0] += math.cos(rad) * self.car_speed
        self.car_pos[1] += math.sin(rad) * self.car_speed
        
        # Check collision or Finish Line or Coin
        crashed = False
        finished = False
        
        # Check validity
        if not self._is_valid(self.car_pos[0], self.car_pos[1]):
            crashed = True
        
        # Check Finish Line (Green)
        # Only count if we have moved away from start (e.g. > 200 steps)
        if self.steps_since_reset > 200:
            try:
                color = self.track_array[int(self.car_pos[0]), int(self.car_pos[1])]
                if color[1] > 200 and color[0] < 50 and color[2] < 50:
                    finished = True
            except:
                pass
        
        # Check Coin (Yellow: R>200, G>200, B<50)
        coin_collected = False
        try:
            cx, cy = int(self.car_pos[0]), int(self.car_pos[1])
            color = self.track_array[cx, cy]
            if color[0] > 200 and color[1] > 200 and color[2] < 50:
                coin_collected = True
                # Remove coin (set to White)
                # We need to clear a small area to ensure we don't pick it up again immediately
                # and to visually remove it
                r = 15 # Radius
                # Update array
                self.track_array[cx-r:cx+r, cy-r:cy+r] = (255, 255, 255)
                # Update visual surface
                pygame.draw.circle(self.track_surface, (255, 255, 255), (cx, cy), r)
        except:
            pass
            
        # Calculate Reward
        reward = 0
        if crashed:
            reward = -100
        elif finished:
            reward = 1000 # Big reward for finishing lap
        else:
            # Reward for moving fast
            reward = self.car_speed * 1.0
            if coin_collected:
                reward += 500 # Bonus for coin!
            
        terminated = crashed or finished
        truncated = False
        
        observation = self._get_obs()
        info = {}
        
        if self.render_mode == "human":
            self.render()
            
        return observation, reward, terminated, truncated, info
    
    def _is_valid(self, x, y):
        if x < 0 or x >= self.width or y < 0 or y >= self.height:
            return False
        # Check pixel color (White or Green is safe, Black/Orange is wall)
        try:
            color = self.track_array[int(x), int(y)]
            # Valid if White-ish OR Green-ish OR Yellow-ish
            # Black is roughly (0,0,0). Orange is (255, 165, 0).
            # We fail if it is DARK (Black) OR ORANGE.
            
            # Check for Orange (High Red, Medium Green, Low Blue)
            # Yellow is (255, 255, 0) -> High Red, High Green.
            # Orange is (255, 165, 0) -> High Red, Med Green.
            
            # If Red is high and Green is high, it's Yellow (Safe)
            if color[0] > 200 and color[1] > 200:
                return True
            
            # If Red is high and Green is medium, it's Orange (Crash)
            if color[0] > 200 and color[1] > 100 and color[1] < 200 and color[2] < 50:
                return False # Hit a cone!
                
            # Check for Black (Wall)
            if color[0] < 50 and color[1] < 50 and color[2] < 50: 
                return False
                
            return True
        except:
            return False

    def _get_obs(self):
        # Raycasting
        rays = []
        angles = [-60, -30, 0, 30, 60]
        
        for angle in angles:
            cast_angle = self.car_angle + angle
            rad = math.radians(cast_angle)
            dist = 0
            max_dist = 200
            
            for d in range(max_dist):
                check_x = self.car_pos[0] + math.cos(rad) * d
                check_y = self.car_pos[1] + math.sin(rad) * d
                if not self._is_valid(check_x, check_y):
                    dist = d
                    break
                dist = d
            
            rays.append(dist)
            
        return np.array(rays, dtype=np.float32)

    def render(self):
        if self.window is None:
            pygame.init()
            self.window = pygame.display.set_mode((self.width, self.height))
            self.clock = pygame.time.Clock()
            
        self.window.blit(self.track_surface, (0, 0))
        
        # Draw car
        rotated_car = pygame.transform.rotate(self.car_img, -self.car_angle)
        rect = rotated_car.get_rect(center=(int(self.car_pos[0]), int(self.car_pos[1])))
        self.window.blit(rotated_car, rect.topleft)
        
        pygame.event.pump()
        pygame.display.flip()
        self.clock.tick(self.metadata["render_fps"])

    def close(self):
        if self.window is not None:
            pygame.quit()
