import pygame
import time

# --- Configuration ---
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600
GRID_SIZE = 30
COLS = SCREEN_WIDTH // GRID_SIZE
ROWS = SCREEN_HEIGHT // GRID_SIZE

# --- Animation Speeds (Adjusted for visibility) ---
MOVE_DELAY = 0.03      # Speed of exploring forward
RETREAT_DELAY = 0.08   # Speed of moving backward (Slower to show the path failing)
DEAD_END_DELAY = 0.15  # Pause when hitting a wall

# --- Colors ---
WHITE = (255, 255, 255)       # Empty Path
BLACK = (0, 0, 0)             # Wall
GREY = (50, 50, 50)           # Grid lines
BLUE = (0, 0, 255)            # Start/End Markers

# --- STATE COLORS ---
CYAN = (0, 255, 255)          # HEAD: "I am here right now"
RED = (255, 0, 0)             # ACTIVE PATH: "I am testing this path"
YELLOW = (255, 255, 0)        # DEAD END: "I am stuck!"
GREEN = (0, 255, 0)           # SUCCESS: "I found the exit!"

# *** CHANGED TO HIGH CONTRAST MAGENTA ***
# This color marks paths that were tried and failed.
FAILED_PATH_COLOR = (200, 0, 200) 


# --- The Maze Layout ---
maze = [
    [0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
    [0, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 0],
    [0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0],
    [0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
    [1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0],
    [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
    [0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 0],
    [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0],
    [0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1, 1, 1, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1],
    [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0], 
    [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
    [0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0],
    [0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
    [0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0] 
]

ROWS = len(maze)
COLS = len(maze[0])
SCREEN_HEIGHT = ROWS * GRID_SIZE
SCREEN_WIDTH = COLS * GRID_SIZE

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Maze Solver: Purple = Failed Path History")

def draw_grid():
    for row in range(ROWS):
        for col in range(COLS):
            val = maze[row][col]
            color = WHITE if val == 0 else BLACK
            rect = (col * GRID_SIZE, row * GRID_SIZE, GRID_SIZE, GRID_SIZE)
            pygame.draw.rect(screen, color, rect)
            pygame.draw.rect(screen, GREY, rect, 1)

def update_cell(r, c, color):
    rect = (c * GRID_SIZE, r * GRID_SIZE, GRID_SIZE, GRID_SIZE)
    pygame.draw.rect(screen, color, rect)
    pygame.draw.rect(screen, GREY, rect, 1)
    pygame.display.update()
    pygame.event.pump()

def solve_maze(r, c):
    # Base Checks
    if r < 0 or c < 0 or r >= ROWS or c >= COLS:
        return False
    if maze[r][c] == 1 or maze[r][c] == 2:
        return False

    # 1. VISUAL: Move Head (Cyan)
    update_cell(r, c, CYAN)
    time.sleep(MOVE_DELAY)

    # 2. Check Goal
    if r == ROWS - 1 and c == COLS - 1:
        update_cell(r, c, GREEN)
        return True

    # 3. Mark as Active Path (Red) and Visited (2)
    maze[r][c] = 2 
    update_cell(r, c, RED) 

    # 4. Explore Neighbors
    directions = [(r + 1, c), (r, c + 1), (r - 1, c), (r, c - 1)]

    for next_r, next_c in directions:
        if solve_maze(next_r, next_c):
            update_cell(r, c, GREEN)
            return True
        
        # VISUAL: We returned from a failed neighbor.
        # Briefly show the head back at this intersection (Cyan)
        update_cell(r, c, CYAN)
        time.sleep(RETREAT_DELAY)
        # Re-color to Red to show we are still processing this cell
        update_cell(r, c, RED)

    # --- 5. FAILURE LOGIC ---
    # If we get here, every single neighbor failed.
    # This entire path segment is a DEAD END.
    
    # Flash Yellow to show "STUCK"
    update_cell(r, c, YELLOW)
    time.sleep(DEAD_END_DELAY)

    # *** Turn Deep Purple (Failed Path) ***
    # This color will REMAIN on the screen so you can see the history
    update_cell(r, c, FAILED_PATH_COLOR)
    time.sleep(RETREAT_DELAY) 
    
    return False

def main():
    run = True
    solved = False
    screen.fill(BLACK)
    
    draw_grid()
    pygame.display.update()
    
    update_cell(0, 0, BLUE)
    update_cell(ROWS-1, COLS-1, BLUE)

    print("Press SPACE to start.")
    print("Red = Active, Purple = Failed/Discarded Path")

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not solved:
                    solve_maze(0, 0)
                    solved = True

    pygame.quit()

if __name__ == "__main__":
    main()