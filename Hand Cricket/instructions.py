import pygame
import sys

pygame.init()
pygame.font.init()

# Set up window dimensions
width = 800
height = 600
win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Hand Cricket - Game Instructions")

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Load background image
background_image = pygame.image.load("background.jpg").convert()
background_image = pygame.transform.scale(background_image, (width, height))

# Define font
font = pygame.font.SysFont("comicsans", 40)

def draw_text(text, color, x, y):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=(x, y))
    win.blit(text_surface, text_rect)

def instructions_screen():
    run = True

    while run:
        win.fill(WHITE)
        win.blit(background_image, (0, 0))

        draw_text("Hand Cricket - Game Instructions", BLACK, width // 2, 50)

        instructions = [
            "1. Hand Cricket is a two-player game where each player takes turns as a batsman and a bowler.",
            "2. The goal for the batsman is to score runs, while the bowler tries to get the batsman out.",
            "3. To play, the bowler chooses a number between 1 and 6 (representing a cricket ball),",
            "   and the batsman also selects a number between 1 and 6 (representing the batsman's hand).",
            "4. If the bowler's number matches the batsman's number, the batsman is out.",
            "5. If the numbers do not match, the batsman scores the runs equal to the number chosen by the batsman.",
            "6. The game continues with players switching roles after each over (6 balls).",
            "7. The winner is determined based on the total runs scored.",
            "8. Have fun playing Hand Cricket!"
        ]

        y_offset = 150
        for text in instructions:
            draw_text(text, BLACK, width // 2, y_offset)
            y_offset += 40

        draw_text("Press ESC or click anywhere to go back to the menu.", GREEN, width // 2, height - 100)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                run = False

# Run the instructions screen
instructions_screen()
