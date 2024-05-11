import pygame
import sys
import subprocess
import os

pygame.init()


# Set up the screen
WIDTH, HEIGHT = 600, 400
screen_width, screen_height = pygame.display.Info().current_w, pygame.display.Info().current_h
window_x=screen_width-WIDTH-50
window_y=40
os.environ['SDL_VIDEO_WINDOW_POS'] = f"{window_x},{window_y}"

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Enter Your Name")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)

# Fonts
font = pygame.font.SysFont("algerian", 35)

user_text = ""

def get_user_input():
    active = True
    global user_text

    while active:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    active = False
                elif event.key == pygame.K_BACKSPACE:
                    user_text = user_text[:-1]
                else:
                    user_text += event.unicode

        screen.fill(WHITE)

        # Render text
        text_surface = font.render("Enter Your Name: " , True, BLACK)
        text_rect = text_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2-50))
        #pygame.draw.rect(screen, GRAY, text_rect.inflate(10, 5))
        screen.blit(text_surface, text_rect)

        # Render user input
        user_surface = font.render(user_text, True, BLACK)
        user_rect = user_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 30))
        pygame.draw.rect(screen, GRAY, user_rect.inflate(10, 5))
        screen.blit(user_surface, user_rect)

        pygame.display.flip()

    return user_text


# Main loop
def main():
    user_name = get_user_input()
    print("User Name:", user_name)
    pygame.quit()
    #subprocess.run(["python", "GamePlayer1.py", user_name])
    subprocess.run(["python", "GamePlayer2.py", user_name])  # Pass the username as an argument to main.py
    sys.exit()  # Ensure that the program exits completely


if __name__ == "__main__":
    main()
