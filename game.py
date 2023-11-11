import pygame
import sys
import pygame.time as timer
import random
import time 

pygame.init()

# Screen settings
WIDTH, HEIGHT = 1000, 750
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong With Gun")

game_state = "menu"  # Initial game state

def main_menu():
    global game_state, game_mode

    # Define button dimensions and positions based on screen size
    button_width = 200
    button_height = 50
    button_x = (WIDTH - button_width) // 2
    singleplayer_button = pygame.Rect(button_x, 200, button_width, button_height)
    multiplayer_button = pygame.Rect(button_x, 300, button_width, button_height)
    exit_button = pygame.Rect(button_x, 400, button_width, button_height)

    while game_state == "menu":
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if singleplayer_button.collidepoint(mouse_pos):
                    game_mode = "singleplayer"
                    game_state = "playing"  # Transition to the game
                elif multiplayer_button.collidepoint(mouse_pos):
                    game_mode = "multiplayer"
                    game_state = "playing"  # Transition to the game
                elif exit_button.collidepoint(mouse_pos):
                    pygame.quit()
                    sys.exit()  # Exit the game

        screen.fill((0, 0, 0))

        # Draw the centered buttons
        pygame.draw.rect(screen, (0, 128, 0), singleplayer_button)  # "Singleplayer" button
        pygame.draw.rect(screen, (128, 0, 0), multiplayer_button)   # "Multiplayer" button
        pygame.draw.rect(screen, (128, 128, 128), exit_button)      # "Exit" button

        font = pygame.font.Font(None, 36)
        singleplayer_text = font.render("Singleplayer", True, (255, 255, 255))
        multiplayer_text = font.render("Multiplayer", True, (255, 255, 255))
        exit_text = font.render("Exit", True, (255, 255, 255))

        screen.blit(singleplayer_text, (button_x + 30, 210))
        screen.blit(multiplayer_text, (button_x + 35, 310))
        screen.blit(exit_text, (button_x + 70, 410))

        player_score = 0
        opponent_score = 0

        pygame.display.flip()

# Initialize game setup
game_mode = "singleplayer"  # Set the initial game mode
game_state = "menu"  # Set the initial game state
paused = False  # Initialize the paused state
pause_time = 0  # Initialize the time when the game was paused
pause_duration = 1000  # 1000 milliseconds = 1 second

# Bullet variables
BULLET_WIDTH, BULLET_HEIGHT = 30, 12
bullet_speed = 2
max_ammo = 3
player_ammo = 0
opponent_ammo = 0
player_bullets = []
opponent_bullets = []

# Clock to control the frame rate
clock = pygame.time.Clock()

# Fire rate and cooldown
fire_rate = 45  # Number of frames between shots
player_cooldown = 0 
opponent_cooldown = 0

# Initialize scores
player_score = 0
opponent_score = 0

# Colors
WHITE = (255, 255, 255)

# Paddle settings
PADDLE_WIDTH, PADDLE_HEIGHT = 10, 100
PADDLE_SPEED = 1
# Bullet icon image
bullet_icon = pygame.Surface((BULLET_HEIGHT, BULLET_WIDTH))
bullet_icon.fill(WHITE)

# Ball settings
BALL_SIZE = 20
BALL_SPEED_X, BALL_SPEED_Y = 1, 1

# Randomize initial ball direction
ball_speed_x = BALL_SPEED_X
ball_speed_y = BALL_SPEED_Y

# Initialize paddle positions
player_paddle = pygame.Rect(50, HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)
opponent_paddle = pygame.Rect(WIDTH - 50 - PADDLE_WIDTH, HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)

# Initialize ball position
ball = pygame.Rect(WIDTH // 2 - BALL_SIZE // 2, HEIGHT // 2 - BALL_SIZE // 2, BALL_SIZE, BALL_SIZE)
ball_speed_x, ball_speed_y = BALL_SPEED_X, BALL_SPEED_Y

def handle_input():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()


def move_paddles():
    global player_paddle, opponent_paddle, ball, paddle_speed

    keys = pygame.key.get_pressed()
    
    if keys[pygame.K_w] and player_paddle.top > 0:
        player_paddle.y -= PADDLE_SPEED
    if keys[pygame.K_s] and player_paddle.bottom < HEIGHT:
        player_paddle.y += PADDLE_SPEED

    if game_mode == "singleplayer":
        if opponent_paddle.centery < ball.centery:
            # Move the opponent paddle down
            opponent_paddle.y += PADDLE_SPEED
        elif opponent_paddle.centery > ball.centery:
            # Move the opponent paddle up
            opponent_paddle.y -= PADDLE_SPEED
    else:
        # Control the opponent's paddle using keyboard input (for multiplayer)
        opponent_scripted = False
        if keys[pygame.K_p] and opponent_paddle.top > 0:
            opponent_paddle.y -= PADDLE_SPEED
        if keys[pygame.K_l] and opponent_paddle.bottom < HEIGHT:
            opponent_paddle.y += PADDLE_SPEED
    
    
def move_ball():
    global ball_speed_x, ball_speed_y, player_score, opponent_score, paused, pause_time, player_ammo, opponent_ammo
    while ball_speed_y==0:
        ball_speed_y = random.uniform(-1.5, 1.5)

    if not paused:
        ball.x += ball_speed_x
        ball.y += ball_speed_y

        # Ball collision with paddles
        if ball.colliderect(player_paddle) or ball.colliderect(opponent_paddle):
            ball_speed_x *= -1
            if ball_speed_y > 0:
                ball_speed_y = random.uniform(1,1.5)
            else:
                ball_speed_y = -random.uniform(1,1.5)
                 
        # Ball collision with top and bottom edges
        if ball.top <= 0 or ball.bottom >= HEIGHT:
            ball_speed_y *= -1

    # Ball out of bounds (player scores a point)
    if ball.left >= WIDTH:
        # Player scores a point
        player_score += 1
        player_ammo += 2
        paused = True
        pause_time = pygame.time.get_ticks()

        # Reset ball position
        ball.x = WIDTH // 2 - BALL_SIZE // 2
        ball.y = HEIGHT // 2 - BALL_SIZE // 2

        # Reset ball speed
        ball_speed_x = BALL_SPEED_X * -1
        ball_speed_y = BALL_SPEED_Y * -1

    elif ball.right <= 0:
        # Opponent scores a point
        opponent_score += 1
        opponent_ammo += 2
        paused = True
        pause_time = pygame.time.get_ticks()

        # Reset ball position
        ball.x = WIDTH // 2 - BALL_SIZE // 2
        ball.y = HEIGHT // 2 - BALL_SIZE // 2

        # Reset ball speed
        ball_speed_x = BALL_SPEED_X
        ball_speed_y = BALL_SPEED_Y
 

def handle_shooting():
    global player_bullets, opponent_bullets, bullet_speed, bullets, bullet, player_ammo, opponent_ammo, bullet_icon, player_cooldown, opponent_cooldown

    keys = pygame.key.get_pressed()

     # Shooting mechanics for the player
    if keys[pygame.K_x] and player_ammo > 0 and player_cooldown==0:
        player_bullet = pygame.Rect(player_paddle.x + BULLET_WIDTH, player_paddle.y + player_paddle.height // 2 - BULLET_HEIGHT // 2, BULLET_WIDTH, BULLET_HEIGHT)
        player_bullets.append(player_bullet)
        player_ammo -= 1
        player_cooldown = fire_rate

    # Shooting mechanics for the opponent (for demonstration purposes)
    if game_mode == "singleplayer":
        if opponent_paddle.y // 2 == player_paddle.y // 2 and opponent_ammo > 0 and opponent_cooldown==0:
            opponent_bullet = pygame.Rect(opponent_paddle.x - BULLET_WIDTH, opponent_paddle.y + opponent_paddle.height // 2 - BULLET_HEIGHT // 2, BULLET_WIDTH, BULLET_HEIGHT)
            opponent_bullets.append(opponent_bullet)
            opponent_ammo -= 1
            opponent_cooldown = fire_rate

    else:
        if keys[pygame.K_COMMA] and opponent_ammo > 0 and opponent_cooldown==0:
            opponent_bullet = pygame.Rect(opponent_paddle.x - BULLET_WIDTH, opponent_paddle.y + opponent_paddle.height // 2 - BULLET_HEIGHT // 2, BULLET_WIDTH, BULLET_HEIGHT)
            opponent_bullets.append(opponent_bullet)
            opponent_ammo -= 1
            opponent_cooldown = fire_rate

    # Move bullets
    player_bullets = [bullet for bullet in player_bullets if bullet.x > 0]
    for bullet in player_bullets:
        bullet.x += bullet_speed

    opponent_bullets = [bullet for bullet in opponent_bullets if bullet.x < WIDTH]
    for bullet in opponent_bullets:
        bullet.x -= bullet_speed

    # Bullet collision with paddles
    for bullet in player_bullets:
        if opponent_paddle.colliderect(bullet) and opponent_paddle.height>20:
            opponent_paddle.height -= 10  # Decrease opponent's paddle width on hit
            player_bullets.remove(bullet)

    for bullet in opponent_bullets:
        if player_paddle.colliderect(bullet) and player_paddle.height>20:
            player_paddle.height -= 10  # Decrease player's paddle width on hit
            opponent_bullets.remove(bullet)

    pygame.draw.rect(screen, WHITE, player_paddle)
    pygame.draw.rect(screen, WHITE, opponent_paddle)

    if player_cooldown > 0:
        player_cooldown -= 1

    if opponent_cooldown > 0:
        opponent_cooldown -= 1
        
    pygame.display.flip()


def draw_game(): 
    global player_bullets, opponent_bullets, bullet, player_ammo, opponent_ammo, bullet_icon
    screen.fill((0, 0, 0))  # Clear the screen
    pygame.draw.rect(screen, WHITE, player_paddle)
    pygame.draw.rect(screen, WHITE, opponent_paddle)
    pygame.draw.ellipse(screen, WHITE, ball)
    for bullet in player_bullets:
        pygame.draw.rect(screen, WHITE, bullet)
    for bullet in opponent_bullets:
        pygame.draw.rect(screen, WHITE, bullet)
    for i in range(player_ammo):
        screen.blit(bullet_icon, (10 + i * (BULLET_HEIGHT + 2), 10))
    for i in range(opponent_ammo):
        screen.blit(bullet_icon, (WIDTH - 10 - (i + 1) * (BULLET_HEIGHT + 2), 10))

    # Draw the scores
    font = pygame.font.Font(None, 36)
    player_score_text = font.render(str(player_score), True, WHITE)
    opponent_score_text = font.render(str(opponent_score), True, WHITE)
    screen.blit(player_score_text, (WIDTH // 4, 20))
    screen.blit(opponent_score_text, (3 * WIDTH // 4 - 36, 20))

    pygame.draw.aaline(screen, WHITE, (WIDTH / 2, 0), (WIDTH / 2, HEIGHT))

while True:
    if game_state == "menu":
        main_menu()
        player_score = 0
        opponent_score = 0
    elif game_state == "playing":
        handle_input()
        clock.tick(600)
        if not paused:
            move_paddles()
            move_ball()
            handle_shooting()
        draw_game()        
        if paused and pygame.time.get_ticks() - pause_time >= pause_duration:
            paused = False
            font = pygame.font.Font(None, 100)
            # Check for a winner
            if (player_score >= 11 and player_score >= opponent_score + 2):
                if game_mode == "singleplayer":
                    victory_text = font.render("Player Wins!", True, WHITE)
                else:
                    victory_text = font.render("Player1 Wins!", True, WHITE)
                screen.blit(victory_text, (300, HEIGHT // 2))
                pygame.display.flip()
                time.sleep(1)  # Pause for 1 second to show the victory screen
                game_state = "menu"  # Return to the main menu
            elif (opponent_score >= 11 and opponent_score >= player_score + 2):
                if game_mode == "singleplayer":
                    victory_text = font.render("Opponent Wins!", True, WHITE)
                    screen.blit(victory_text, (250, HEIGHT // 2)) 
                else:
                    victory_text = font.render("Player2 Wins!", True, WHITE)
                    screen.blit(victory_text, (300, HEIGHT // 2))   
                pygame.display.flip()
                time.sleep(1)  # Pause for 1 second to show the victory screen
                game_state = "menu"  # Return to the main menu
        pygame.display.flip()        