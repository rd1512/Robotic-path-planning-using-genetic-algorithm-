import pygame
import math

# Define the window size
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# Define the obstacles
obstacles = [(300, 300), (200, 200), (400, 400), (500, 200), (600, 300)]

# Define the path
path = [(100, 100), (281, 65), (96, 249), (638, 173), (166, 331), (700, 500)]

def calculate_distance(point1, point2):
    x1, y1 = point1
    x2, y2 = point2
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

# Define the occupancy matrix
occupancy_matrix = [[False for x in range(WINDOW_WIDTH)] for y in range(WINDOW_HEIGHT)]
for obstacle in obstacles:
    occupancy_matrix[obstacle[1]][obstacle[0]] = True

# Define obstacle rectangles
obstacle_rects = []
for obstacle in obstacles:
    obstacle_rect = pygame.Rect(obstacle[0]-20, obstacle[1]-20, 50, 50)
    obstacle_rects.append(obstacle_rect)

# Set up the game window
pygame.init()
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Avoid Obstacle Line")

# Draw the obstacles
for obstacle in obstacles:
    pygame.draw.circle(screen, WHITE, obstacle, 20)
    pygame.draw.circle(screen, BLACK, obstacle, 18)

# Define a function to check for obstacle avoidance
def check_collision(start, end):
    line_rect = pygame.draw.line(screen, RED, start, end, 5)
    for obstacle_rect in obstacle_rects:
        if line_rect.colliderect(obstacle_rect):
            print("Line intersects with obstacle. Generating new point...")
            return True
    return False


# Draw the initial path
for i in range(len(path)-1):
    start_point = path[i]
    end_point = path[i+1]
    if check_collision(start_point, end_point):
        pygame.draw.line(screen, RED, start_point, end_point, 5)


# Update the display
pygame.display.update()

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

for i in range(len(path)-1):
    best_path_length = sum([calculate_distance(path[i], path[i + 1]) for i in range(len(path) - 1)])
print(best_path_length)

# Quit the game
pygame.quit()
