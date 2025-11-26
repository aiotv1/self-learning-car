import pygame
import sys

# Settings
WIDTH, HEIGHT = 800, 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
ORANGE = (255, 165, 0)
YELLOW = (255, 255, 0)
BRUSH_SIZE = 30
CONE_SIZE = 10
COIN_SIZE = 10

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Draw Track! (L-Click: Road, O: Cone, Y: Coin, G: Start, R-Click: Erase)")
    
    canvas = pygame.Surface((WIDTH, HEIGHT))
    canvas.fill(BLACK)
    
    clock = pygame.time.Clock()
    drawing = False
    erasing = False
    drawing_start = False
    drawing_cone = False
    drawing_coin = False
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1: # Left click
                    keys = pygame.key.get_pressed()
                    if keys[pygame.K_g]:
                        drawing_start = True
                    elif keys[pygame.K_o]:
                        drawing_cone = True
                    elif keys[pygame.K_y]:
                        drawing_coin = True
                    else:
                        drawing = True
                elif event.button == 3: # Right click
                    erasing = True
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    drawing = False
                    drawing_start = False
                    drawing_cone = False
                    drawing_coin = False
                elif event.button == 3:
                    erasing = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    pygame.image.save(canvas, "track.png")
                    print("Track saved as track.png")
                    pygame.quit()
                    sys.exit()
                elif event.key == pygame.K_c:
                    canvas.fill(BLACK)

        # Drawing logic
        mouse_pos = pygame.mouse.get_pos()
        if drawing:
            pygame.draw.circle(canvas, WHITE, mouse_pos, BRUSH_SIZE)
        if drawing_start:
            pygame.draw.circle(canvas, GREEN, mouse_pos, BRUSH_SIZE)
        if drawing_cone:
            pygame.draw.circle(canvas, ORANGE, mouse_pos, CONE_SIZE)
        if drawing_coin:
            pygame.draw.circle(canvas, YELLOW, mouse_pos, COIN_SIZE)
        if erasing:
            pygame.draw.circle(canvas, BLACK, mouse_pos, BRUSH_SIZE)
        
        # Update screen
        screen.blit(canvas, (0, 0))
        pygame.display.flip()
        clock.tick(120)

if __name__ == "__main__":
    main()
