# Import necessary libraries
import pygame
import sys
import math
import random

# Initialize pygame and set up the screen
pygame.init()
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Simple pew-pew")
clock = pygame.time.Clock()

# Define the Player class
class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.radius = 20

    def draw(self):
        # Draw the player as a red circle
        pygame.draw.circle(screen, (255, 0, 0), (self.x, self.y), self.radius)

    def move(self, dx, dy):
        # Move the player within the screen boundaries
        new_x = self.x + dx
        new_y = self.y + dy
        if 0 <= new_x <= width:
            self.x = new_x
        if 0 <= new_y <= height:
            self.y = new_y

    def shoot(self, mouse_x, mouse_y):
        # Calculate the angle between the player and the mouse cursor
        dx = mouse_x - self.x
        dy = mouse_y - self.y
        angle = math.atan2(dy, dx)
        # Create a new bullet with the calculated angle
        bullet = Bullet(self.x, self.y, angle)
        bullets.append(bullet)

# Define the Bullet class
class Bullet:
    def __init__(self, x, y, angle):
        self.x = x
        self.y = y
        self.radius = 5
        self.speed = 10
        self.dx = self.speed * math.cos(angle)
        self.dy = self.speed * math.sin(angle)

    def draw(self):
        # Draw the bullet as a green circle
        pygame.draw.circle(screen, (0, 255, 0), (int(self.x), int(self.y)), self.radius)

    def update(self):
        # Update the bullet's position based on its velocity
        self.x += self.dx
        self.y += self.dy

# Define the Enemy class
class Enemy:
    def __init__(self):
        self.radius = 15
        self.x = random.randint(width + self.radius, width + 100)
        self.y = random.randint(0, height)
        self.speed = random.randint(1, 4)
        side = random.randint(0, 3)  # 0: top, 1: right, 2: bottom, 3: left
        # Randomly spawn enemies at different sides of the screen
        if side == 0:
            self.x = random.randint(0, width)
            self.y = random.randint(-100, -self.radius)
        elif side == 1:
            self.x = random.randint(width + self.radius, width + 100)
            self.y = random.randint(0, height)
        elif side == 2:
            self.x = random.randint(0, width)
            self.y = random.randint(height + self.radius, height + 100)
        else:
            self.x = random.randint(-100, -self.radius)
            self.y = random.randint(0, height)

    def draw(self):
        # Draw the enemy as a blue circle
        pygame.draw.circle(screen, (0, 0, 255), (self.x, self.y), self.radius)

    def update(self, player_x, player_y):
        # Move the enemy towards the player
        dx = player_x - self.x
        dy = player_y - self.y
        distance = math.sqrt(dx ** 2 + dy ** 2)
        if distance != 0:
            self.x += self.speed * dx / distance
            self.y += self.speed * dy / distance

# Create the player object
player = Player(width // 2, height // 2)

# Initialize lists to store bullets and enemies
bullets = []
enemies = []

# Initialize game state variables
game_over = False
paused = False
score = 0
menu = True
how_to_play = False

# Create a font for displaying text
font = pygame.font.SysFont(None, 24)

# Main game loop
while True:
    for event in pygame.event.get():
        # Handle quit event to exit the game
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # Handle events in the main menu
        if menu:
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if width // 2 - 50 <= mouse_x <= width // 2 + 50:
                    if height // 2 - 20 <= mouse_y <= height // 2 + 10:
                        # Play button clicked, start the game
                        menu = False
                    elif height // 2 + 30 <= mouse_y <= height // 2 + 60:
                        # Exit button clicked, quit the game
                        pygame.quit()
                        sys.exit()
                    elif height // 2 + 80 <= mouse_y <= height // 2 + 110:
                        # How to Play button clicked, show instructions
                        how_to_play = True

        # Handle events during the game
        if not game_over and not paused and not menu:
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                player.shoot(mouse_x, mouse_y)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    # Pause the game when ESC key is pressed
                    paused = True

        # Handle events after the game is over
        if game_over and event.type == pygame.MOUSEBUTTONUP:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            if width // 2 - 50 <= mouse_x <= width // 2 + 50 and height // 2 + 40 <= mouse_y <= height // 2 + 90:
                # Retry button clicked, reset the game
                player = Player(width // 2, height // 2)
                bullets = []
                enemies = []
                game_over = False
                score = 0
            elif width // 2 - 50 <= mouse_x <= width // 2 + 50 and height // 2 - 30 <= mouse_y <= height // 2 + 20:
                # Exit button clicked, quit the game
                pygame.quit()
                sys.exit()

        # Handle events when the game is paused
        if paused and event.type == pygame.MOUSEBUTTONUP:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            if width // 2 - 50 <= mouse_x <= width // 2 + 50 and height // 2 - 30 <= mouse_y <= height // 2 + 20:
                # Resume button clicked, unpause the game
                paused = False
            elif width // 2 - 90 <= mouse_x <= width // 2 + 90 and height // 2 + 30 <= mouse_y <= height // 2 + 80:
                # Exit to Menu button clicked, go back to the main menu
                menu = True
                paused = False
                player = Player(width // 2, height // 2)
                bullets = []
                enemies = []
                game_over = False
                score = 0

        # Handle events in the How to Play instructions screen
        if how_to_play and event.type == pygame.MOUSEBUTTONUP:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            if width - 80 <= mouse_x <= width - 20 and 20 <= mouse_y <= 80:
                # Back button clicked, go back to the main menu
                how_to_play = False
                menu = True

    # Main menu screen
    if menu:
        screen.fill((0, 0, 0))
        # Draw menu title and buttons
        menu_title_text = font.render("Simple pew-pew", True, (255, 255, 255))
        menu_title_text_rect = menu_title_text.get_rect(center=(width // 2, height // 2 - 100))
        screen.blit(menu_title_text, menu_title_text_rect)

        play_button_rect = pygame.Rect(width // 2 - 50, height // 2 - 20, 100, 30)
        pygame.draw.rect(screen, (0, 255, 0), play_button_rect)
        play_button_text = font.render("Play", True, (0, 0, 0))
        play_button_text_rect = play_button_text.get_rect(center=play_button_rect.center)
        screen.blit(play_button_text, play_button_text_rect)

        exit_button_rect = pygame.Rect(width // 2 - 50, height // 2 + 30, 100, 30)
        pygame.draw.rect(screen, (255, 0, 0), exit_button_rect)
        exit_button_text = font.render("Exit", True, (0, 0, 0))
        exit_button_text_rect = exit_button_text.get_rect(center=exit_button_rect.center)
        screen.blit(exit_button_text, exit_button_text_rect)

        how_to_play_button_rect = pygame.Rect(width // 2 - 80, height // 2 + 80, 160, 30)
        pygame.draw.rect(screen, (0, 0, 255), how_to_play_button_rect)
        how_to_play_button_text = font.render("How to Play", True, (0, 0, 0))
        how_to_play_button_text_rect = how_to_play_button_text.get_rect(center=how_to_play_button_rect.center)
        screen.blit(how_to_play_button_text, how_to_play_button_text_rect)

    # Main game screen
    elif not game_over and not paused:
        # Handle player movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            player.move(0, -5)
        if keys[pygame.K_a]:
            player.move(-5, 0)
        if keys[pygame.K_s]:
            player.move(0, 5)
        if keys[pygame.K_d]:
            player.move(5, 0)

        # Clear the screen
        screen.fill((0, 0, 0))

        # Draw the player
        player.draw()

        # Update and draw bullets, and handle bullet-enemy collisions
        for bullet in bullets:
            bullet.update()
            bullet.draw()

            if bullet.x < 0 or bullet.x > width or bullet.y < 0 or bullet.y > height:
                bullets.remove(bullet)

            for enemy in enemies:
                distance = math.sqrt((enemy.x - bullet.x) ** 2 + (enemy.y - bullet.y) ** 2)
                if distance < enemy.radius + bullet.radius:
                    enemies.remove(enemy)
                    bullets.remove(bullet)
                    score += 1
                    break

        # Update and draw enemies, and check for player-enemy collisions
        for enemy in enemies:
            enemy.update(player.x, player.y)
            enemy.draw()

            if math.sqrt((enemy.x - player.x) ** 2 + (enemy.y - player.y) ** 2) < enemy.radius + player.radius:
                game_over = True

        # Randomly spawn new enemies
        if random.randint(1, 50) < 2:
            enemy = Enemy()
            enemies.append(enemy)

    # Game over screen
    if game_over:
        # Draw game over text and options
        game_over_rect = pygame.Rect(width // 2 - 100, height // 2 - 100, 200, 200)
        pygame.draw.rect(screen, (255, 255, 255), game_over_rect)
        font = pygame.font.SysFont(None, 36)
        game_over_text = font.render("Game Over", True, (0, 0, 0))
        game_over_text_rect = game_over_text.get_rect(center=(width // 2, height // 2 - 85))
        screen.blit(game_over_text, game_over_text_rect)

        retry_rect = pygame.Rect(width // 2 - 50, height // 2 + 40, 100, 50)
        pygame.draw.rect(screen, (0, 255, 0), retry_rect)
        retry_text = font.render("Retry", True, (0, 0, 0))
        retry_text_rect = retry_text.get_rect(center=retry_rect.center)
        screen.blit(retry_text, retry_text_rect)

        exit_rect = pygame.Rect(width // 2 - 50, height // 2 - 70, 100, 50)
        pygame.draw.rect(screen, (255, 0, 0), exit_rect)
        exit_text = font.render("Exit", True, (0, 0, 0))
        exit_text_rect = exit_text.get_rect(center=exit_rect.center)
        screen.blit(exit_text, exit_text_rect)

        exit_menu_rect = pygame.Rect(width // 2 - 90, height // 2 - 15, 180, 50)
        pygame.draw.rect(screen, (0, 0, 255), exit_menu_rect)
        exit_menu_text = font.render("Exit to Menu", True, (0, 0, 0))
        exit_menu_text_rect = exit_menu_text.get_rect(center=exit_menu_rect.center)
        screen.blit(exit_menu_text, exit_menu_text_rect)

        if retry_rect.collidepoint(pygame.mouse.get_pos()):
            pygame.draw.rect(screen, (0, 200, 0), retry_rect, 3)
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Retry button clicked, reset the game
                player = Player(width // 2, height // 2)
                bullets = []
                enemies = []
                game_over = False
                score = 0
        if exit_rect.collidepoint(pygame.mouse.get_pos()):
            pygame.draw.rect(screen, (200, 0, 0), exit_rect, 3)
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Exit button clicked, quit the game
                pygame.quit()
                sys.exit()
        if exit_menu_rect.collidepoint(pygame.mouse.get_pos()):
            pygame.draw.rect(screen, (0, 0, 200), exit_menu_rect, 3)
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Exit to main menu button clicked, go back to the main menu
                menu = True
                player = Player(width // 2, height // 2)
                bullets = []
                enemies = []
                game_over = False
                score = 0

    # Pause screen
    if paused:
        # Draw pause window
        pause_rect = pygame.Rect(width // 2 - 100, height // 2 - 100, 200, 200)
        pygame.draw.rect(screen, (255, 255, 255), pause_rect)
        font = pygame.font.SysFont(None, 36)
        pause_text = font.render("Game Paused", True, (0, 0, 0))
        pause_text_rect = pause_text.get_rect(center=(width // 2, height // 2 - 50))
        screen.blit(pause_text, pause_text_rect)

        resume_rect = pygame.Rect(width // 2 - 50, height // 2 - 30, 100, 50)
        pygame.draw.rect(screen, (0, 255, 0), resume_rect)
        resume_text = font.render("Resume", True, (0, 0, 0))
        resume_text_rect = resume_text.get_rect(center=resume_rect.center)
        screen.blit(resume_text, resume_text_rect)

        exit_menu_rect = pygame.Rect(width // 2 - 90, height // 2 + 30, 180, 50)
        pygame.draw.rect(screen, (0, 0, 255), exit_menu_rect)
        exit_menu_text = font.render("Exit to Menu", True, (0, 0, 0))
        exit_menu_text_rect = exit_menu_text.get_rect(center=exit_menu_rect.center)
        screen.blit(exit_menu_text, exit_menu_text_rect)

        if resume_rect.collidepoint(pygame.mouse.get_pos()):
            pygame.draw.rect(screen, (0, 200, 0), resume_rect, 3)
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Resume button clicked, unpause the game
                paused = False
        if exit_menu_rect.collidepoint(pygame.mouse.get_pos()):
            pygame.draw.rect(screen, (0, 0, 200), exit_menu_rect, 3)
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Exit to main menu button clicked, go back to the main menu
                menu = True
                player = Player(width // 2, height // 2)
                bullets = []
                enemies = []
                game_over = False
                score = 0

    # Display the score during the game (not in the menu or other screens)
    if not menu:
        score_text = font.render(f"Score: {score}", True, (255, 255, 255))
        screen.blit(score_text, (10, 10))

    # How to Play instructions screen
    if how_to_play:
        screen.fill((0, 0, 0))  # Display black background

        # Draw How to Play instructions
        how_to_play_text = font.render("How to Play:", True, (255, 255, 255))
        how_to_play_text_rect = how_to_play_text.get_rect(center=(width // 2, height // 2))
        screen.blit(how_to_play_text, how_to_play_text_rect)

        move_text = font.render("W,A,S,D keys to move up, down, left, right.", True, (255, 255, 255))
        move_text_rect = move_text.get_rect(center=(width // 2, height // 2 + 20))
        screen.blit(move_text, move_text_rect)

        aim_text = font.render("Move mouse to aim.", True, (255, 255, 255))
        aim_text_rect = aim_text.get_rect(center=(width // 2, height // 2 + 50))
        screen.blit(aim_text, aim_text_rect)

        shoot_text = font.render("Left click or right click to shoot.", True, (255, 255, 255))
        shoot_text_rect = shoot_text.get_rect(center=(width // 2, height // 2 + 80))
        screen.blit(shoot_text, shoot_text_rect)

        # Draw back button to go back to the main menu
        back_rect = pygame.Rect(20, 20, 100, 30)
        pygame.draw.rect(screen, (0, 0, 0), back_rect)
        back_text = font.render("Back", True, (255, 255, 255))
        back_text_rect = back_text.get_rect(center=back_rect.center)
        screen.blit(back_text, back_text_rect)

        if back_rect.collidepoint(pygame.mouse.get_pos()):
            pygame.draw.rect(screen, (255, 255, 255), back_rect, 3)
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Back button clicked, go back to the main menu
                how_to_play = False
                menu = True

    # Update the display and control the frame rate
    pygame.display.flip()
    clock.tick(60)
