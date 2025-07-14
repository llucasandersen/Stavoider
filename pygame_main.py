import pygame
import random
import time
import google.generativeai as genai

WIDTH, HEIGHT = 600, 600
PLAYER_SIZE = 40
ASTEROID_SIZE = 30
GREEN_SIZE = 25

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
PURPLE = (160, 32, 240)

pygame.init()
pygame.mixer.init()

COUNTDOWN_SOUND = pygame.mixer.Sound("audios/countdown.mp3")
GAMEOVER_SOUND = pygame.mixer.Sound("audios/gameover.mp3")
MOVE_SOUND = pygame.mixer.Sound("audios/Move.mp3")
BACKGROUND_SOUND = pygame.mixer.Sound("audios/backroundnoise.mp3")
YOUWIN_SOUND = pygame.mixer.Sound("audios/youwin.mp3")

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Stavoider")
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 24)

# Configure Gemini API using the GEMINI_API_KEY environment variable
import os
API_KEY = os.environ.get("GEMINI_API_KEY")
if API_KEY:
    genai.configure(api_key=API_KEY)
    model = genai.GenerativeModel("gemini-1.5-pro-latest")
else:
    model = None

def draw_text(surface, text, size, x, y, colour=WHITE):
    fnt = pygame.font.SysFont("Arial", size)
    txt = fnt.render(text, True, colour)
    rect = txt.get_rect(center=(x, y))
    surface.blit(txt, rect)

def main_menu():
    while True:
        screen.fill(BLACK)
        draw_text(screen, "Stavoider", 50, WIDTH // 2, HEIGHT // 3)
        draw_text(screen, "Press ENTER to play", 30, WIDTH // 2, HEIGHT // 2)
        draw_text(screen, "Press ESC to quit", 20, WIDTH // 2, HEIGHT // 2 + 40)
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return True
                if event.key == pygame.K_ESCAPE:
                    return False
        clock.tick(60)

def create_asteroid(speed):
    x = random.randint(-WIDTH, -ASTEROID_SIZE)
    y = random.randint(0, HEIGHT - ASTEROID_SIZE)
    return pygame.Rect(x, y, ASTEROID_SIZE, ASTEROID_SIZE), speed

def create_green():
    x = random.randint(-WIDTH, -GREEN_SIZE)
    y = random.randint(0, HEIGHT - GREEN_SIZE)
    return pygame.Rect(x, y, GREEN_SIZE, GREEN_SIZE)

def countdown():
    COUNTDOWN_SOUND.play()
    for i in range(3, 0, -1):
        screen.fill(BLACK)
        draw_text(screen, str(i), 60, WIDTH // 2, HEIGHT // 2)
        pygame.display.flip()
        pygame.time.delay(1000)

def run_typing_game(score):
    if not model:
        return score, []

    prompt_parts = [{"text": f"Generate a sentence about dodging that is roughly {int(score) or 1} words long."}]
    try:
        response = model.generate_content(prompt_parts)
        challenge = response.text.strip()
    except Exception:
        challenge = "dodge the hurdles swiftly!"

    wrapped = []
    while len(challenge) > 40:
        wrapped.append(challenge[:40])
        challenge = challenge[40:]
    wrapped.append(challenge)

    entry = ""
    start = time.time()
    time_limit = len(challenge.split()) * 2.0
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return score, []
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if entry.strip().lower() == challenge.lower() and time.time() - start <= time_limit:
                        return score + 5, []
                    else:
                        return score, []
                elif event.key == pygame.K_BACKSPACE:
                    entry = entry[:-1]
                else:
                    entry += event.unicode

        screen.fill(BLACK)
        yoff = HEIGHT // 3
        for line in wrapped:
            draw_text(screen, line, 24, WIDTH // 2, yoff)
            yoff += 30
        draw_text(screen, entry, 24, WIDTH // 2, HEIGHT // 2 + 80)
        draw_text(screen, f"Time left: {int(time_limit - (time.time() - start))}", 20, WIDTH // 2, HEIGHT // 2 + 120)
        pygame.display.flip()
        clock.tick(60)

def game_loop():
    player = pygame.Rect(WIDTH // 2, HEIGHT // 2, PLAYER_SIZE, PLAYER_SIZE)
    asteroids = [create_asteroid(2 + i * 0.05) for i in range(10)]
    green = create_green()
    score = 0
    slowdown = 0
    BACKGROUND_SOUND.play(-1)
    running = True
    countdown()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            player.x -= 5
            MOVE_SOUND.play()
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            player.x += 5
            MOVE_SOUND.play()
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            player.y -= 5
            MOVE_SOUND.play()
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            player.y += 5
            MOVE_SOUND.play()
        player.clamp_ip(screen.get_rect())

        for rect, speed in asteroids:
            rect.x += speed - slowdown
            if rect.x > WIDTH:
                rect.x = -ASTEROID_SIZE
                rect.y = random.randint(0, HEIGHT - ASTEROID_SIZE)
            if rect.colliderect(player):
                GAMEOVER_SOUND.play()
                return score
        green.x += 2
        if green.x > WIDTH:
            green = create_green()
        if green.colliderect(player):
            score, _ = run_typing_game(score)
            slowdown += score / 50
            if asteroids:
                asteroids.pop()
            green = create_green()

        score += 0.02
        screen.fill(BLACK)
        pygame.draw.rect(screen, PURPLE, player)
        for rect, _ in asteroids:
            pygame.draw.rect(screen, RED, rect)
        pygame.draw.rect(screen, GREEN, green)
        draw_text(screen, f"Score: {int(score)}", 20, 60, 20)
        pygame.display.flip()
        clock.tick(60)
    return score

def game_over(score):
    YOUWIN_SOUND.play()
    while True:
        screen.fill(BLACK)
        draw_text(screen, "Game Over", 50, WIDTH // 2, HEIGHT // 3)
        draw_text(screen, f"Score: {int(score)}", 30, WIDTH // 2, HEIGHT // 2)
        draw_text(screen, "Press ENTER to play again", 20, WIDTH // 2, HEIGHT // 2 + 50)
        draw_text(screen, "ESC to exit", 20, WIDTH // 2, HEIGHT // 2 + 80)
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return True
                if event.key == pygame.K_ESCAPE:
                    return False
        clock.tick(60)

def main():
    while True:
        if not main_menu():
            break
        score = game_loop()
        if not game_over(score):
            break
    pygame.quit()

if __name__ == "__main__":
    main()
