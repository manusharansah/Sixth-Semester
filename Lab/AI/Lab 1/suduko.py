import pygame
import time

# --- Configuration ---
SCREEN_SIZE = 540  # Must be divisible by 9
GRID_SIZE = SCREEN_SIZE // 9
DELAY = 0.05       # Speed of animation (0.01 is fast, 0.1 is slow)

# --- Colors ---
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (200, 200, 200)
BLUE = (50, 50, 255)    # Initial fixed numbers
GREEN = (0, 200, 0)     # Tentatively placed numbers
RED = (255, 0, 0)       # Backtracking (Error/Reset)
CYAN = (0, 255, 255)    # Currently testing

# --- A Sample Sudoku Board (0 = Empty) ---
board = [
    [7, 8, 0, 4, 0, 0, 1, 2, 0],
    [6, 0, 0, 0, 7, 5, 0, 0, 9],
    [0, 0, 0, 6, 0, 1, 0, 7, 8],
    [0, 0, 7, 0, 4, 0, 2, 6, 0],
    [0, 0, 1, 0, 5, 0, 9, 3, 0],
    [9, 0, 4, 0, 6, 0, 0, 0, 5],
    [0, 7, 0, 3, 0, 0, 0, 1, 2],
    [1, 2, 0, 0, 0, 7, 4, 0, 0],
    [0, 4, 9, 2, 0, 6, 0, 0, 7]
]

# Keep a copy of the original board to color-code fixed numbers differently
original_board = [row[:] for row in board]

# --- Pygame Setup ---
pygame.init()
screen = pygame.display.set_mode((SCREEN_SIZE, SCREEN_SIZE))
pygame.display.set_caption("Sudoku Backtracking Solver")
font = pygame.font.SysFont('Arial', 35, bold=True)

def draw_grid(current_r=None, current_c=None, color=None):
    screen.fill(WHITE)
    
    # Draw Lines
    for i in range(10):
        # Thick lines for 3x3 boxes
        thickness = 4 if i % 3 == 0 else 1
        pygame.draw.line(screen, BLACK, (0, i * GRID_SIZE), (SCREEN_SIZE, i * GRID_SIZE), thickness)
        pygame.draw.line(screen, BLACK, (i * GRID_SIZE, 0), (i * GRID_SIZE, SCREEN_SIZE), thickness)

    # Draw Numbers
    for r in range(9):
        for c in range(9):
            val = board[r][c]
            if val != 0:
                # Determine text color
                if original_board[r][c] != 0:
                    text_color = BLUE  # Fixed original numbers
                elif r == current_r and c == current_c:
                    text_color = color # The number we are currently changing
                else:
                    text_color = GREEN # Solved (so far) numbers

                text = font.render(str(val), True, text_color)
                # Center the text
                x_pos = c * GRID_SIZE + (GRID_SIZE // 2 - text.get_width() // 2)
                y_pos = r * GRID_SIZE + (GRID_SIZE // 2 - text.get_height() // 2)
                screen.blit(text, (x_pos, y_pos))

    pygame.display.update()
    pygame.event.pump()

def find_empty(bo):
    for r in range(9):
        for c in range(9):
            if bo[r][c] == 0:
                return (r, c)  # Row, Col
    return None

def is_valid(bo, num, pos):
    # Check Row
    for i in range(9):
        if bo[pos[0]][i] == num and pos[1] != i:
            return False

    # Check Column
    for i in range(9):
        if bo[i][pos[1]] == num and pos[0] != i:
            return False

    # Check 3x3 Box
    box_x = pos[1] // 3
    box_y = pos[0] // 3

    for i in range(box_y*3, box_y*3 + 3):
        for j in range(box_x*3, box_x*3 + 3):
            if bo[i][j] == num and (i, j) != pos:
                return False

    return True

def solve_sudoku():
    # 1. Find an empty spot
    find = find_empty(board)
    if not find:
        return True  # No empty spots left = Solved!
    
    row, col = find

    # 2. Try numbers 1 through 9
    for i in range(1, 10):
        
        # VISUAL: Show we are testing number 'i' (Cyan)
        board[row][col] = i
        draw_grid(row, col, CYAN)
        # time.sleep(DELAY/2) # Optional tiny delay for testing phase

        # 3. Check Constraints
        if is_valid(board, i, (row, col)):
            
            # Valid so far! Visualize as Green
            draw_grid(row, col, GREEN)
            time.sleep(DELAY)

            # 4. Recurse
            if solve_sudoku():
                return True

            # --- BACKTRACKING ---
            # If we return here, the path failed. Reset to 0.
            # VISUAL: Show RED flash before removing
            draw_grid(row, col, RED)
            time.sleep(DELAY)
            board[row][col] = 0
            
        else:
            # If invalid immediately, reset (so we don't leave bad numbers)
            board[row][col] = 0
    
    return False

def main():
    running = True
    solved = False
    
    draw_grid() # Initial draw

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not solved:
                    if solve_sudoku():
                        print("Solved!")
                        draw_grid() # Final update
                    else:
                        print("Unsolvable.")
                    solved = True

    pygame.quit()

if __name__ == "__main__":
    main()