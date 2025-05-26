#!/usr/bin/env python3
import curses
import random
import time
import sys

def draw_border(stdscr, height, width):
    """Draw a border around the game area."""
    # Draw horizontal lines (top and bottom)
    for i in range(width - 1):  # Avoid the bottom-right corner
        stdscr.addch(0, i, curses.ACS_HLINE)
        if i < width - 1:  # Avoid the bottom-right corner
            try:
                stdscr.addch(height - 1, i, curses.ACS_HLINE)
            except curses.error:
                pass  # Ignore errors for bottom-right corner
    
    # Draw vertical lines (left and right)
    for i in range(height - 1):  # Avoid the bottom-right corner
        stdscr.addch(i, 0, curses.ACS_VLINE)
        if i < height - 1:  # Avoid the bottom-right corner
            try:
                stdscr.addch(i, width - 1, curses.ACS_VLINE)
            except curses.error:
                pass  # Ignore errors
    
    # Add corners (safely)
    stdscr.addch(0, 0, curses.ACS_ULCORNER)
    stdscr.addch(0, width - 1, curses.ACS_URCORNER)
    stdscr.addch(height - 1, 0, curses.ACS_LLCORNER)
    
    # Safely handle the bottom-right corner
    try:
        stdscr.addch(height - 1, width - 1, curses.ACS_LRCORNER)
    except curses.error:
        pass  # Ignore error for bottom-right corner

def show_game_over(stdscr, height, width, score):
    """Display game over message."""
    game_over_text = "GAME OVER!"
    score_text = f"Final Score: {score}"
    retry_text = "Press 'r' to play again or 'q' to quit"
    
    # Clear the screen
    stdscr.clear()
    
    # Display game over message with colors if available
    try:
        stdscr.addstr(height // 2 - 2, (width - len(game_over_text)) // 2, game_over_text, curses.color_pair(3) | curses.A_BOLD)
        stdscr.addstr(height // 2, (width - len(score_text)) // 2, score_text, curses.color_pair(4) | curses.A_BOLD)
        stdscr.addstr(height // 2 + 2, (width - len(retry_text)) // 2, retry_text, curses.color_pair(2))
    except:
        # Fallback if color fails
        stdscr.addstr(height // 2 - 2, (width - len(game_over_text)) // 2, game_over_text)
        stdscr.addstr(height // 2, (width - len(score_text)) // 2, score_text)
        stdscr.addstr(height // 2 + 2, (width - len(retry_text)) // 2, retry_text)
    stdscr.refresh()

def show_countdown(stdscr, height, width):
    """Display a countdown before starting the game."""
    for count in range(3, 0, -1):
        stdscr.clear()
        count_text = f"Starting in {count}..."
        stdscr.addstr(height // 2, (width - len(count_text)) // 2, count_text, curses.color_pair(3) | curses.A_BOLD)
        stdscr.refresh()
        time.sleep(1)

def show_instructions(stdscr, height, width):
    """Display game instructions."""
    title = "SNAKE GAME"
    instructions = [
        "Use arrow keys to move the snake",
        "Eat food (◆) to grow and increase your score",
        "Avoid hitting the walls or yourself",
        "Press 'q' to quit anytime",
        "The snake speeds up as your score increases",
        "",
        "Press any key to start"
    ]
    
    # Clear the screen
    stdscr.clear()
    
    # Display title with color
    stdscr.addstr(height // 4, (width - len(title)) // 2, title, curses.color_pair(2) | curses.A_BOLD)
    
    # Display instructions with color
    for i, line in enumerate(instructions):
        attr = curses.A_NORMAL
        if i == len(instructions) - 1:  # Highlight the "Press any key" instruction
            attr = curses.color_pair(3) | curses.A_BOLD
        stdscr.addstr(height // 4 + 3 + i, (width - len(line)) // 2, line, attr)
    
    # Draw a box around instructions
    box_height = len(instructions) + 4
    box_width = max(len(line) for line in instructions) + 4
    box_y = height // 4 + 1
    box_x = (width - box_width) // 2

    # Draw the box
    for y in range(box_height):
        for x in range(box_width):
            if (y == 0 and x == 0) or (y == 0 and x == box_width - 1) or \
               (y == box_height - 1 and x == 0) or (y == box_height - 1 and x == box_width - 1):
                # Corners
                char = '+'
            elif y == 0 or y == box_height - 1:
                # Top and bottom borders
                char = '-'
            elif x == 0 or x == box_width - 1:
                # Left and right borders
                char = '|'
            else:
                continue  # Skip interior of the box
            
            try:
                stdscr.addch(box_y + y, box_x + x, char, curses.color_pair(1))
            except curses.error:
                pass
    
    stdscr.refresh()
    stdscr.getch()  # Wait for user input

def main(stdscr):
    # Clear screen completely
    stdscr.clear()
    stdscr.refresh()
    
    # Set up curses
    try:
        curses.curs_set(0)  # Hide cursor
    except:
        pass  # Some terminals don't support cursor visibility
        
    stdscr.timeout(100)  # Set input timeout (controls game speed)
    stdscr.keypad(True)  # Enable special keys (like arrows)
    
    # Brief pause to ensure terminal is ready
    time.sleep(0.1)
    
    # Initialize colors
    try:
        curses.start_color()
        curses.use_default_colors()
        curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLUE)     # Border color
        curses.init_pair(2, curses.COLOR_GREEN, -1)                    # Snake color
        curses.init_pair(3, curses.COLOR_RED, -1)                      # Food color
        curses.init_pair(4, curses.COLOR_YELLOW, -1)                   # Score color
        has_colors = True
    except:
        has_colors = False
    
    # Get screen dimensions
    height, width = stdscr.getmaxyx()
    
    # Check if terminal is big enough
    if height < 10 or width < 30:
        stdscr.clear()
        stdscr.addstr(0, 0, "Terminal too small. Please resize to at least 30x10.")
        stdscr.refresh()
        stdscr.getch()
        return
    
    # Game area dimensions (accounting for borders)
    game_height = height - 2
    game_width = width - 2
    
    # Ensure screen is clear before starting
    stdscr.clear()
    stdscr.refresh()
    
    # Show instructions
    show_instructions(stdscr, height, width)
    
    # Show countdown
    show_countdown(stdscr, height, width)
    
    while True:
        # Initialize game variables
        snake = [(game_height // 2, game_width // 4)]  # Snake starting position
        food = None
        direction = curses.KEY_RIGHT  # Initial direction
        score = 0
        speed_factor = 1.0
        game_over = False
        
        # Initialize food position
        while food is None:
            potential_food = (
                random.randint(1, game_height - 2),
                random.randint(1, game_width - 2)
            )
            if potential_food not in snake:
                food = potential_food
        
        # Game loop
        while not game_over:
            try:
                # Check if terminal size changed
                new_height, new_width = stdscr.getmaxyx()
                if new_height != height or new_width != width:
                    # Update dimensions
                    height, width = new_height, new_width
                    game_height = height - 2
                    game_width = width - 2
                    
                    # Check if new size is big enough
                    if height < 10 or width < 30:
                        stdscr.clear()
                        try:
                            stdscr.addstr(0, 0, "Terminal too small. Please resize to at least 30x10.")
                        except curses.error:
                            pass  # Handle case where even this message won't fit
                        stdscr.refresh()
                        time.sleep(2)
                        continue
                    
                    # Redraw the screen with new dimensions
                    stdscr.clear()
                    stdscr.refresh()
                    
                    # Ensure snake and food are within new boundaries
                    # Move snake if it's outside the new boundaries
                    new_snake = []
                    for y, x in snake:
                        if y >= game_height - 1:
                            y = game_height - 2
                        if x >= game_width - 1:
                            x = game_width - 2
                        new_snake.append((y, x))
                    snake = new_snake
                    
                    # Ensure food is within new boundaries
                    if food:
                        food_y, food_x = food
                        if food_y >= game_height - 1 or food_x >= game_width - 1:
                            # Regenerate food within new boundaries
                            food = None
                            while food is None:
                                potential_food = (
                                    random.randint(1, game_height - 2),
                                    random.randint(1, game_width - 2)
                                )
                                if potential_food not in snake:
                                    food = potential_food
            except curses.error:
                # Handle any curses errors during terminal size checking
                pass
            
            # Set game speed based on score
            timeout = int(100 / speed_factor)
            stdscr.timeout(timeout)
            
            # Get user input
            key = stdscr.getch()
            
            # Handle key presses
            if key == ord('q'):
                return  # Exit game
            elif key in [curses.KEY_UP, curses.KEY_DOWN, curses.KEY_LEFT, curses.KEY_RIGHT]:
                # Prevent 180-degree turns (can't go directly opposite current direction)
                if (key == curses.KEY_UP and direction != curses.KEY_DOWN) or \
                   (key == curses.KEY_DOWN and direction != curses.KEY_UP) or \
                   (key == curses.KEY_LEFT and direction != curses.KEY_RIGHT) or \
                   (key == curses.KEY_RIGHT and direction != curses.KEY_LEFT):
                    direction = key
            
            # Calculate new head position based on direction
            head_y, head_x = snake[0]
            if direction == curses.KEY_UP:
                head_y -= 1
            elif direction == curses.KEY_DOWN:
                head_y += 1
            elif direction == curses.KEY_LEFT:
                head_x -= 1
            elif direction == curses.KEY_RIGHT:
                head_x += 1
            
            # Check for collisions with walls
            if head_y <= 0 or head_y >= game_height - 1 or head_x <= 0 or head_x >= game_width - 1:
                game_over = True
                continue
            
            # Check for collisions with self
            new_head = (head_y, head_x)
            if new_head in snake:
                game_over = True
                continue
            
            # Add new head to snake
            snake.insert(0, new_head)
            
            # Check if food eaten
            if new_head == food:
                # Generate new food
                while True:
                    potential_food = (
                        random.randint(1, game_height - 2),
                        random.randint(1, game_width - 2)
                    )
                    if potential_food not in snake:
                        food = potential_food
                        break
                
                # Increase score and speed
                score += 10
                if score % 50 == 0:
                    speed_factor += 0.2
            else:
                # Remove tail if food wasn't eaten
                snake.pop()
            
            # Clear screen
            stdscr.clear()
            
            # Draw border with color if available
            draw_border(stdscr, height, width)
            
            # Draw a small hint about controls at the bottom
            controls_hint = "← ↑ → ↓: Move | q: Quit"
            try:
                stdscr.addstr(height - 1, 2, controls_hint, curses.A_DIM)
            except curses.error:
                pass  # Ignore errors if we can't display the controls hint
            
            # Check if terminal supports Unicode (do this once outside the loop)
            use_unicode = sys.stdout.encoding.lower().startswith(('utf', 'utf-8'))
            
            # Draw snake
            for i, (y, x) in enumerate(snake):
                # Skip drawing if at the bottom-right corner
                if y == height - 1 and x == width - 1:
                    continue
                
                # Determine character to use
                if i == 0:  # Head
                    char = '█' if use_unicode else 'O'
                    attr = curses.color_pair(2) | curses.A_BOLD if has_colors else curses.A_NORMAL
                else:  # Body
                    char = '▒' if use_unicode else 'o'
                    attr = curses.color_pair(2) if has_colors else curses.A_NORMAL
                
                # Safely draw the character
                try:
                    stdscr.addch(y, x, char, attr)
                except curses.error:
                    pass  # Ignore errors (e.g., when trying to draw at bottom-right)
            
            # Draw food (safely)
            if food:
                # Skip drawing if food is at the bottom-right corner
                if not (food[0] == height - 1 and food[1] == width - 1):
                    # Determine food character
                    food_char = '◆' if use_unicode else '*'
                    food_attr = curses.color_pair(3) | curses.A_BOLD if has_colors else curses.A_NORMAL
                    
                    # Safely draw the food
                    try:
                        stdscr.addch(food[0], food[1], food_char, food_attr)
                    except curses.error:
                        pass  # Ignore errors
            
            # Draw score
            score_text = f"Score: {score}"
            # Make sure we don't write too close to the edge
            score_pos = max(0, min(width - len(score_text) - 1, width - 2))
            
            # Determine score attributes
            score_attr = curses.color_pair(4) | curses.A_BOLD if has_colors else curses.A_NORMAL
            
            # Safely draw the score
            try:
                stdscr.addstr(0, score_pos, score_text, score_attr)
            except curses.error:
                # Fallback to drawing without attributes if there's an error
                try:
                    stdscr.addstr(0, score_pos, score_text)
                except curses.error:
                    pass  # Ignore if we can't draw the score at all
            
            # Refresh screen
            stdscr.refresh()
        
        # Game over, show message and wait for input
        show_game_over(stdscr, height, width, score)
        
        # Wait for 'r' to restart or 'q' to quit
        while True:
            key = stdscr.getch()
            if key == ord('q'):
                return  # Exit game
            elif key == ord('r'):
                break  # Restart game

def safe_addch(stdscr, y, x, char, attr=curses.A_NORMAL):
    """Safely add a character to the screen, handling potential errors."""
    # Skip the bottom-right corner which often causes issues
    if y == curses.LINES - 1 and x == curses.COLS - 1:
        return
    
    try:
        stdscr.addch(y, x, char, attr)
    except curses.error:
        pass  # Ignore errors
if __name__ == "__main__":
    # Use curses.wrapper for safer terminal handling
    try:
        # Let curses.wrapper handle initialization and cleanup
        curses.wrapper(main)
    except KeyboardInterrupt:
        # Handle Ctrl+C gracefully
        pass
    except curses.error as e:
        # Handle curses errors
        print(f"Curses error occurred: {e}")
        print("This might be due to terminal size issues.")
    except Exception as e:
        # Handle any other exceptions
        print(f"Unexpected error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        # Print exit message
        print("Thanks for playing Snake!")

