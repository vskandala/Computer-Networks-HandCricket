import math
import sys
import pygame
import subprocess
from network import Network
import os

from Player2 import user_text as player2
from Player1 import user_text

os.environ['SDL_VIDEO_WINDOW_POS'] = '0,70'

pygame.init()
pygame.font.init()
pygame.time.set_timer(pygame.USEREVENT + 1, 2000)  # 2000 milliseconds (2 seconds)

player1 = sys.argv[1]
winner_text = ""

width = 600
height = 600
win = pygame.display.set_mode((width, height))
pygame.display.set_caption("player1")
background_image = pygame.image.load("Hand cricket.jpg").convert()


class Button:
    def __init__(self, text, x, y, color, hover_color, default_color):
        self.text = text
        self.x = x
        self.y = y
        self.color = color
        self.hover_color = hover_color
        self.default_color = default_color
        self.width = 100
        self.height = 70
        self.radius = 10
        self.visible = True
        self.clicked_color = (100, 100, 100)
        self.clicked = False
        self.hovered = False

    def draw(self, win):
        if self.visible:
            if self.clicked:
                pygame.draw.rect(win, self.clicked_color, (self.x, self.y, self.width, self.height),
                                 border_radius=self.radius)
            elif self.hovered:
                pygame.draw.rect(win, self.hover_color, (self.x, self.y, self.width, self.height),
                                 border_radius=self.radius)
            else:
                pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height),
                                 border_radius=self.radius)

            font = pygame.font.SysFont("comicsans", 30)
            text = font.render(self.text, 1, (0, 0, 0))
            win.blit(text, (self.x + round(self.width / 2) - round(text.get_width() / 2),
                            self.y + round(self.height / 2) - round(text.get_height() / 2)))

    def click(self, pos):
        if self.visible:
            x1 = pos[0]
            y1 = pos[1]
            if self.x <= x1 <= self.x + self.width and self.y <= y1 <= self.y + self.height:
                self.clicked = True
                self.color = self.clicked_color
                return True
        return False

    def reset(self):
        self.clicked = False
        self.color = self.default_color
        self.draw(win)

    def hover(self, pos):
        if self.visible:
            x1 = pos[0]
            y1 = pos[1]
            if self.x <= x1 <= self.x + self.width and self.y <= y1 <= self.y + self.height:
                self.hovered = True
            else:
                self.hovered = False
                self.clicked = False


def resize_image(background_image1, width, height):
    pass

role_change_msg = ""
role_change_msg1=""
show_role_change = False


def redrawWindow(wind, game, p, game_over=False, out_message=""):
    global role_change_msg,role_change_msg1, show_role_change, winner_text
    new_background_image = pygame.image.load("batting.jpg").convert()
    wind.fill((200, 175, 250))
    if not game.connected():
        win.fill((255, 255, 255))
        font = pygame.font.SysFont("comicsans", 45)
        text1 = font.render(f"Welcome {player1}", 1, (0, 0, 0))
        text2 = font.render("Waiting for Player 2...", 1, (0, 0, 0))
        text1_rect = text1.get_rect(center=(width / 2, height / 2 - text1.get_height()))
        text2_rect = text2.get_rect(center=(width / 2, height / 2 + text2.get_height()))
        wind.blit(text1, text1_rect)
        wind.blit(text2, text2_rect)
    else:
        player_role_text = ""
        if p == 1 and game.done_bat[0] == 1:
            player_role_text = "Batsman"
            show_role_change = True
            role_change_msg = ".Opponent is out."
            role_change_msg1 = "Now, you are now the Batsman!"
        elif p == 0 and game.done_bat[0] == 1:
            player_role_text = "Bowler"
            show_role_change = True
            role_change_msg = "Opponent is out."
            role_change_msg1 = "Now, you are now the Bowler!"
        elif p == 1:
            player_role_text = "Bowler"
        elif p == 0:
            player_role_text = "Batsman"

        font = pygame.font.SysFont("comicsans", 40)
        show_role_change = True
        player_name_text = font.render(f"{player1} ({player_role_text})", 1, (0, 0, 0))
        player_name_rect = player_name_text.get_rect(center=(width // 2, 50))
        wind.blit(player_name_text, player_name_rect)

        if show_role_change:
            role_change_text = font.render(role_change_msg, True, (0, 0, 128))
            role_change_text1=font.render(role_change_msg1, True, (0, 0, 128))
            role_change_rect = role_change_text.get_rect(midbottom=(width // 2 , 320))
            role_change_rect1 = role_change_text1.get_rect(midbottom=(width // 2 , 360))
            wind.blit(role_change_text, role_change_rect)
            wind.blit(role_change_text1, role_change_rect1)
            role_change_msg = ""
            role_change_msg1 = ""
            show_role_change = False

        font = pygame.font.SysFont("comicsans", 40)
        player1_score_text = font.render(f"Your score:", 1, (0, 0, 0))
        player2_score_text = font.render(f"Opponent score:", 1, (0, 0, 0))

        player1_score_val = font.render(str(game.get_player_score(0)), 1, (0, 0, 0))
        player2_score_val = font.render(str(game.get_player_score(1)), 1, (0, 0, 0))

        player_scores_rect1 = pygame.Rect(60, 100, 340, 50)
        player_scores_rect2 = pygame.Rect(60, 150, 340, 50)

        pygame.draw.rect(wind, (255, 255, 255), player_scores_rect1.inflate(10, 10), border_radius=10)
        pygame.draw.rect(wind, (255, 255, 255), player_scores_rect2.inflate(10, 10), border_radius=10)

        wind.blit(player1_score_text, player_scores_rect1)
        wind.blit(player2_score_text, player_scores_rect2)

        player1_score_pos = (player_scores_rect1.right - player1_score_val.get_width() - 5,
                             player_scores_rect1.top + (
                                     player_scores_rect1.height - player1_score_val.get_height()) // 2)
        player2_score_pos = (player_scores_rect2.right - player2_score_val.get_width() - 5,
                             player_scores_rect2.top + (
                                     player_scores_rect2.height - player2_score_val.get_height()) // 2)

        wind.blit(player1_score_val, player1_score_pos)
        wind.blit(player2_score_val, player2_score_pos)

        turn_text = ""
        if game.bothWent():
            if p == 1:
                turn_text = f"Opponent's turn"
            else:
                turn_text = f" Your turn"
        else:
            if game.p1Went and p == 0:
                turn_text = f"Opponent's turn"
            elif game.p2Went and p == 1:
                turn_text = f" Your turn"
            else:
                turn_text = f"Your turn"

        turn_msg = font.render(turn_text, True, (0, 0, 0))
        turn_rect = turn_msg.get_rect(midtop=(width // 2 - 35, player_scores_rect2.bottom ))
        wind.blit(turn_msg, turn_rect)

        for btn in btns:
            btn.draw(wind)
        chat_btn.draw(win)

    if game_over:
        wind.fill((200, 175, 250))
        font = pygame.font.SysFont("comicsans", 40)
        game_over_text = font.render("Game Over!", 1, (255, 0, 0))
        win.blit(game_over_text, (width // 2 - game_over_text.get_width() // 2, 250))

        if game.get_player_score(0) > game.get_player_score(1):
            winner_text = font.render("Hurray!! You won. Congratulations", 1, (0, 0, 128))
        elif game.get_player_score(0) < game.get_player_score(1):
            winner_text = font.render("You lost. Better luck next time!", 1, (0, 0, 128))
        else:
            winner_text = font.render("Its a tie.Wanna Try Again??", 1, (0, 0, 128))

        win.blit(winner_text, (0, 100))

        player1_final_score_text = font.render(f"Your Final Score: {game.get_player_score(0)}", 1, (0, 0, 0))
        player2_final_score_text = font.render(f"Opponents Final Score: {game.get_player_score(1)}", 1, (0, 0, 0))
        win.blit(player1_final_score_text, (width // 2 - player1_final_score_text.get_width() // 2, 300))
        win.blit(player2_final_score_text, (width // 2 - player2_final_score_text.get_width() // 2, 350))

        exit_btn.visible = True
        chat_btn.visible = False

        exit_btn.draw(win)
        chat_btn.draw(win)

    if out_message:
        out_font = pygame.font.SysFont("comicsans", 40)
        out_text = out_font.render(out_message, 1, (255, 0, 0))
        out_rect = out_text.get_rect(center=(width // 2, height // 2))
        wind.blit(out_text, out_rect)

    pygame.display.update()


btns = [
    Button("1", 90, 370, (255, 255, 255), (200, 200, 200), (255, 255, 255)),
    Button("2", 200, 370, (255, 255, 255), (200, 200, 200), (255, 255, 255)),
    Button("3", 310, 370, (255, 255, 255), (200, 200, 200), (255, 255, 255)),
    Button("4", 90, 460, (255, 255, 255), (200, 200, 200), (255, 255, 255)),
    Button("5", 200, 460, (255, 255, 255), (200, 200, 200), (255, 255, 255)),
    Button("6", 310, 460, (255, 255, 255), (200, 200, 200), (255, 255, 255)),
]

chat_btn = Button("Chat", width - 170, 90, (255, 255, 255), (200, 200, 200), (255, 255, 255))
exit_btn = Button("Exit", width // 2 + 20, 450, (255, 0, 0), (200, 0, 0), (255, 0, 0))

def reset_ui_elements():
    chat_btn.visible = True
    exit_btn.visible = False

def main():
    global show_role_change
    run = True
    clock = pygame.time.Clock()
    n = Network()
    player = int(n.getP())
    print("You are player", player)
    game_over = False
    show_role_change = False

    while run:
        clock.tick(60)
        try:
            game = n.send("get")
        except:
            run = False
            print("Couldn't get game")
            break

        if game.bothWent():
            redrawWindow(win, game, player)
            pygame.time.delay(500)
            try:
                game = n.send("score")
            except:
                run = False
                print("Couldn't get game for score")
                break

        if game.done_bat[0] and game.done_bat[1] or (
                game.get_player_score(1) > game.get_player_score(0) and not game.done_bat[1]):
            game_over = True
            redrawWindow(win, game, player, game_over)
            try:
                game = n.send("reset")
            except:
                run = False
                print("Couldn't get game")
                break

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if game_over:
                    if exit_btn.click(pos):
                        run = False
                        pygame.quit()
                else:
                    for btn in btns:
                        if btn.click(pos) and game.connected():
                            if player == 0:
                                if not game.p1Went:
                                    n.send(btn.text)
                                    btn.color = btn.clicked_color
                                    btn.color = btn.default_color
                                    print(btn.text)
                            else:
                                if not game.p2Went:
                                    n.send(btn.text)
                                    btn.color = btn.clicked_color
                                    btn.color = btn.default_color
                                    print(btn.text)
                    if chat_btn.click(pos):
                        print("Chat clicked!")
                        subprocess.Popen(["python", "chatClient1.py"])
                        if show_role_change:
                             role_change_msg = ""
                             show_role_change = False
            elif event.type == pygame.MOUSEMOTION:
                pos = pygame.mouse.get_pos()
                for btn in btns:
                    btn.hover(pos)

        redrawWindow(win, game, player, game_over)


def menu_screen():
    run = True
    clock = pygame.time.Clock()

    while run:
        clock.tick(5)
        win.fill((255, 255, 255))
        font = pygame.font.SysFont("comicsans", 50)
        text = font.render("Click to Play!", 1, (0, 0, 0))
        win.blit(text, (220, 10))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                run = False
            if event.type == pygame.USEREVENT + 1:
                out_message = ""
        win.blit(background_image, [70, 100])

        pygame.display.update()

    main()


while True:
    menu_screen()

if __name__ == "__main__":
    main()
