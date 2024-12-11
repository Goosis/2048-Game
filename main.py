import json
import pygame
from logics import *
import sys

# Define colors
COLOR_TEXT = (255, 127, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (130, 130, 130)
RED = (255, 0, 0)  # For error messages

# Load high scores from a file
def load_high_scores(filename="high_scores.json"):
    try:
        with open(filename, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return [{"name": "None", "score": 0} for _ in range(3)]
    except json.JSONDecodeError:
        print("Error: high_scores.json is corrupted. Creating a new file.")
        return [{"name": "None", "score": 0} for _ in range(3)]

# Save high scores to a file
def save_high_scores(high_scores, filename="high_scores.json"):
    try:
        with open(filename, "w") as file:
            json.dump(high_scores, file)
    except IOError:
        print("Error: Failed to save the high scores.")

# Update high scores if the player's score is high enough
def update_high_scores(name, score, high_scores):
    high_scores.append({"name": name, "score": score})
    high_scores.sort(key=lambda x: x["score"], reverse=True)
    return high_scores[:3]

# This function allows the player to input their name. If the input is empty, it shows an error message
def get_player_name(screen):
    font = pygame.font.SysFont("simsun", 48)
    info_font = pygame.font.SysFont("simsun", 32)
    error_font = pygame.font.SysFont("simsun", 24)
    input_box = pygame.Rect(150, 300, 500, 50)
    color_inactive = pygame.Color('lightskyblue3')
    color_active = pygame.Color('dodgerblue2')
    color = color_inactive
    active = False
    text = ""
    error_message = ""
    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if input_box.collidepoint(event.pos):
                    active = not active
                else:
                    active = False
                color = color_active if active else color_inactive
            if event.type == pygame.KEYDOWN:
                if active:
                    if event.key == pygame.K_RETURN:
                        if len(text.strip()) == 0:
                            error_message = "Nickname cannot be empty. Please try again."
                        else:
                            return text
                    elif event.key == pygame.K_BACKSPACE:
                        text = text[:-1]
                    else:
                        text += event.unicode

        screen.fill(WHITE)
        info_text = info_font.render("Please enter your nickname:", True, BLACK)
        screen.blit(info_text, (150, 250))  # Display instruction above input box
        txt_surface = font.render(text, True, BLACK)
        width = max(500, txt_surface.get_width() + 10)
        input_box.w = width
        screen.blit(txt_surface, (input_box.x + 5, input_box.y + 5))
        pygame.draw.rect(screen, color, input_box, 2)

        # Show error message if input is empty
        if error_message:
            error_text = error_font.render(error_message, True, RED)
            screen.blit(error_text, (150, 370))

        pygame.display.flip()
        clock.tick(30)

pygame.init()

# Player enters their name before starting the game
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Enter Your Name")
player_name = get_player_name(screen)

# Initialize game grid
mas = [
    [0, 0, 0, 0],
    [0, 0, 0, 0],
    [0, 0, 0, 0],
    [0, 0, 0, 0],
]

# Colors for blocks
COLORS = {
    0: (130, 130, 130),
    2: (255, 255, 255),
    4: (255, 255, 128),
    8: (255, 255, 0),
    16: (255, 235, 255),
    32: (255, 235, 128),
    64: (255, 235, 0),
    128: (255, 135, 255),
    256: (255, 135, 200),
}

# Grid settings
BlOCKS = 4
SIZE_BLOCK = 110
MARGIN = 10
WIDTH = BlOCKS * SIZE_BLOCK + (BlOCKS + 1) * MARGIN + 250
HEIGHT = WIDTH + 110
TITLE_REC = pygame.Rect(0, 0, WIDTH, 110)
score = 0

mas[1][2] = 2
mas[3][0] = 4

# Load high scores
high_scores = load_high_scores()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("2048")

# This function draws the game interface, including the grid, score, and high scores
def draw_interface(score, delta=0, high_scores=[]):
    screen.fill(WHITE)
    pygame.draw.rect(screen, WHITE, TITLE_REC)

    font = pygame.font.SysFont("stxingkai", 70)
    font_score = pygame.font.SysFont("simsun", 48)
    font_delta = pygame.font.SysFont("simsun", 32)
    font_top = pygame.font.SysFont("simsun", 30)

    text_score = font_score.render("Score", True, COLOR_TEXT)
    text_score_value = font_score.render(f"{score}", True, COLOR_TEXT)
    screen.blit(text_score, (20, 35))
    screen.blit(text_score_value, (175, 35))
    if delta > 0:
        text_delta = font_delta.render(f"+{delta}", True, COLOR_TEXT)
        screen.blit(text_delta, (170, 65))

    # Draw the black rectangle behind the game grid
    pygame.draw.rect(screen, BLACK, (
        MARGIN,
        SIZE_BLOCK + MARGIN,
        WIDTH - 250 - 2 * MARGIN,
        BlOCKS * SIZE_BLOCK + (BlOCKS - 1) * MARGIN
    ))

    # Display high scores
    text_top = font_top.render("Top Scores", True, COLOR_TEXT)
    screen.blit(text_top, (WIDTH - 230, 20))
    for idx, entry in enumerate(high_scores, start=1):
        name_text = font_top.render(f"{idx}. {entry['name']} - {entry['score']}", True, COLOR_TEXT)
        screen.blit(name_text, (WIDTH - 230, 20 + idx * 40))

    pretty_print(mas)
    for row in range(BlOCKS):
        for column in range(BlOCKS):
            value = mas[row][column]
            w = column * SIZE_BLOCK + (column + 1) * MARGIN
            h = row * SIZE_BLOCK + (row + 1) * MARGIN + SIZE_BLOCK
            pygame.draw.rect(screen, COLORS[value], (w, h, SIZE_BLOCK, SIZE_BLOCK))

            if value != 0:
                text = font.render(f'{value}', True, BLACK)
                font_w, font_h = text.get_size()
                text_x = w + (SIZE_BLOCK - font_w) / 2
                text_y = h + (SIZE_BLOCK - font_h) / 2
                screen.blit(text, (text_x, text_y))

draw_interface(score, high_scores=high_scores)
pygame.display.update()

# Main game loop
while is_zero_in_mas(mas) or can_move(mas):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            high_scores = update_high_scores(player_name, score, high_scores)
            save_high_scores(high_scores)
            pygame.quit()
            sys.exit(0)

        elif event.type == pygame.KEYDOWN:
            delta = 0
            if event.key == pygame.K_LEFT:
                mas, delta = move_left(mas)
            elif event.key == pygame.K_RIGHT:
                mas, delta = move_right(mas)
            elif event.key == pygame.K_UP:
                mas, delta = move_up(mas)
            elif event.key == pygame.K_DOWN:
                mas, delta = move_down(mas)
            score += delta

            empty = get_empty_list(mas)
            if empty:
                random.shuffle(empty)
                random_num = empty.pop()
                x, y = get_index_from_number(random_num)
                mas = insert_2_or_4(mas, x, y)
                draw_interface(score, delta, high_scores)
                pygame.display.update()

# If no more moves, show Game Over
font_game_over = pygame.font.SysFont("simsun", 72)
text_game_over = font_game_over.render("Game Over", True, RED)
screen.blit(text_game_over, (WIDTH // 3, HEIGHT // 2))
pygame.display.update()
pygame.time.wait(3000)  # Wait for 3 seconds before closing

# Update high scores and save after the game ends
high_scores = update_high_scores(player_name, score, high_scores)
save_high_scores(high_scores)
pygame.quit()
