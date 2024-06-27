import pygame
from random import randrange

# Initialize Pygame
pygame.init()

WINDOW = 800
TILE_SIZE = 50
RANGE = (TILE_SIZE // 2, WINDOW - TILE_SIZE // 2, TILE_SIZE)
get_random_position = lambda: [randrange(*RANGE), randrange(*RANGE)]

snake = pygame.rect.Rect([0,0,TILE_SIZE - 2, TILE_SIZE - 2])
snake.center = get_random_position()
length = 1
segments = [snake.copy()]
snake_dir = (0,0)
time, time_step = 0, 170  # Adjusted time_step for smoother movement
food = snake.copy()
food.center = get_random_position()

# Load the apple image
apple_image = pygame.image.load('apple.png')
apple_image = pygame.transform.scale(apple_image, (TILE_SIZE, TILE_SIZE))

# Load snake head images
head_images = {
    'up': pygame.image.load('head_up.png'),
    'down': pygame.image.load('head_down.png'),
    'left': pygame.image.load('head_left.png'),
    'right': pygame.image.load('head_right.png')
}

# Load snake tail images
tail_images = {
    'up': pygame.image.load('tail_up.png'),
    'down': pygame.image.load('tail_down.png'),
    'left': pygame.image.load('tail_left.png'),
    'right': pygame.image.load('tail_right.png')
}

# Scale head and tail images to tile size
for key in head_images:
    head_images[key] = pygame.transform.scale(head_images[key], (TILE_SIZE, TILE_SIZE))
    tail_images[key] = pygame.transform.scale(tail_images[key], (TILE_SIZE, TILE_SIZE))

# Setup the screen
screen = pygame.display.set_mode([WINDOW]*2)
pygame.display.set_caption('Snake Game')
clock = pygame.time.Clock()

# Initialize the font
pygame.font.init()
font = pygame.font.Font(None, 36)

# Function to display score
def display_score(score):
    score_text = font.render(f"Score: {score}", True, (255, 255, 255))
    screen.blit(score_text, (10, 10))

# Function to draw the checkerboard background with lighter colors
def draw_checkerboard():
    colors = [(144, 238, 144), (173, 255, 47)]  # Lighter light green and lighter dark green
    for row in range(0, WINDOW, TILE_SIZE):
        for col in range(0, WINDOW, TILE_SIZE):
            color = colors[(row // TILE_SIZE + col // TILE_SIZE) % 2]
            pygame.draw.rect(screen, color, (col, row, TILE_SIZE, TILE_SIZE))

# Function to draw the snake head with images and the rest with rectangles
def draw_snake(segments, snake_dir):
    for i, segment in enumerate(segments):
        if i == 0:  # Head
            if snake_dir == (0, -TILE_SIZE):
                screen.blit(head_images['up'], segment.topleft)
            elif snake_dir == (0, TILE_SIZE):
                screen.blit(head_images['down'], segment.topleft)
            elif snake_dir == (-TILE_SIZE, 0):
                screen.blit(head_images['left'], segment.topleft)
            elif snake_dir == (TILE_SIZE, 0):
                screen.blit(head_images['right'], segment.topleft)
        elif i == len(segments) - 1:  # Tail
            tail_direction = get_tail_direction(segments[-2], segment)
            screen.blit(tail_images[tail_direction], segment.topleft)
        else:  # Body
            pygame.draw.rect(screen, (102, 102, 255), segment)  # Lighter blue color

# Function to get tail direction based on current and next segment
def get_tail_direction(current_segment, next_segment):
    if current_segment.left == next_segment.left and current_segment.top < next_segment.top:
        return 'down'
    elif current_segment.left == next_segment.left and current_segment.top > next_segment.top:
        return 'up'
    elif current_segment.top == next_segment.top and current_segment.left < next_segment.left:
        return 'right'
    elif current_segment.top == next_segment.top and current_segment.left > next_segment.left:
        return 'left'

# Function to display game over screen
def game_over_screen(score):
    game_over_font = pygame.font.Font(None, 72)
    game_over_text = game_over_font.render("Game Over", True, (255, 0, 0))
    score_text = font.render(f"Score: {score}", True, (255, 255, 255))
    restart_text = font.render("Press space to restart", True, (255, 255, 255))

    screen.blit(game_over_text, (WINDOW // 2 - game_over_text.get_width() // 2, WINDOW // 2 - game_over_text.get_height() // 2))
    screen.blit(score_text, (WINDOW // 2 - score_text.get_width() // 2, WINDOW // 2 + 20))
    screen.blit(restart_text, (WINDOW // 2 - restart_text.get_width() // 2, WINDOW // 2 + 60))

    pygame.display.flip()

# Function to restart the game
def restart_game():
    global snake, segments, snake_dir, length, score
    snake.center = get_random_position()
    length = 1
    segments = [snake.copy()]
    snake_dir = (0, 0)
    score = 0

score = 0
game_over = False

run = True

while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if not game_over:
                if event.key == pygame.K_UP and snake_dir != (0, TILE_SIZE):
                    snake_dir = (0, -TILE_SIZE)
                if event.key == pygame.K_DOWN and snake_dir != (0, -TILE_SIZE):
                    snake_dir = (0, TILE_SIZE)
                if event.key == pygame.K_LEFT and snake_dir != (TILE_SIZE, 0):
                    snake_dir = (-TILE_SIZE, 0)
                if event.key == pygame.K_RIGHT and snake_dir != (-TILE_SIZE, 0):
                    snake_dir = (TILE_SIZE, 0)
            else:
                if event.key == pygame.K_SPACE:
                    game_over = False
                    restart_game()

    if not game_over:
        draw_checkerboard()  # Draw the checkerboard background

        self_eating = pygame.Rect.collidelist(snake, segments[1:]) != -1  # Check collision with body only
        if snake.left < 0 or snake.right > WINDOW or snake.top < 0 or snake.bottom > WINDOW or self_eating:
            game_over = True

        if not game_over:
            if snake.center == food.center:
                food.center = get_random_position()
                score += 1  # Increase score when snake eats food
                # Add a new segment to the snake's body
                new_segment = segments[-1].copy()
                segments.append(new_segment)

            # Move snake and update segments
            new_head = snake.move(snake_dir)
            segments = [new_head] + segments[:-1]
            snake = new_head

            # Draw the apple image instead of a red rectangle
            screen.blit(apple_image, food.topleft)

            # Draw the snake with images for the head and tail, and rectangles for the body
            draw_snake(segments, snake_dir)

            # Display the score
            display_score(score)

    else:
        game_over_screen(score)

    pygame.display.flip()
    clock.tick(10)

pygame.quit()
