import os, pygame
from CNF import *
pygame.init()

# Set up the screen
WIDTH, HEIGHT = 600, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Sudoku")
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SOURCE = os.path.dirname(BASE_DIR)
MAP  = os.path.join(SOURCE, "MAP")
map_file = os.path.join(MAP, f"map.txt")

# Define some colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

def read_map(filename):
    try:
        with open(filename, 'r') as f:
            # Read the dimensions
            dimensions = f.readline().strip().split()
            rows, cols = int(dimensions[0]), int(dimensions[1])
            
            # Read the map
            map_data = []
            for _ in range(rows):
                row = list(map(int, f.readline().strip().split()))
                map_data.append(row)
            
            return Map(rows, cols, map_data)
    except FileNotFoundError:
        print("File not found.")
        return None
# Function to draw the grid
def draw_grid(map_data):
    cell_size = WIDTH // map_data.cols
    for i in range(map_data.rows):
        for j in range(map_data.cols):
            pygame.draw.rect(screen, WHITE, (j * cell_size, i * cell_size, cell_size, cell_size), 1)
            # Draw numbers
            number = map_data.data[i][j]
            if number != 0:
                font = pygame.font.Font(None, 36)
                text = font.render(str(number), True, WHITE)
                text_rect = text.get_rect(center=(j * cell_size + cell_size // 2, i * cell_size + cell_size // 2))
                screen.blit(text, text_rect)
# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Fill the background
    screen.fill(BLACK)

    # Draw the grid
    map_data = read_map(map_file)
    draw_grid(map_data)
    solution = solve_sudoku(map_data)
    if solution:
        print("Sudoku Solution:")
        for row in solution:
            print(row)
    else:
        print("No solution found.")
    # Update the display
    pygame.display.update()

pygame.quit()
