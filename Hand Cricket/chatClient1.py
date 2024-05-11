import socket
import sys
import threading
import pygame
from pygame.locals import *
import os

os.environ['SDL_VIDEO_WINDOW_POS'] = '0,70'

class ChatClient:
    def __init__(self, host, port,player_name):
        self.host = host
        self.port = port
        self.player_name = player_name

        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((self.host, self.port))

        pygame.init()
        self.screen = pygame.display.set_mode((600, 550))  # Updated window size
        pygame.display.set_caption(f"Chat Client - {self.player_name}")

        self.font = pygame.font.Font(None, 24)
        self.text_color = (0, 0, 0)  # Black font color
        self.background_color = (200, 200, 200)  # Light gray background color

        self.chat_messages = []
        self.user_input = ""

        self.receive_thread = threading.Thread(target=self.receive_messages)
        self.receive_thread.start()

        self.running = True
        self.main_loop()

    def main_loop(self):
        clock = pygame.time.Clock()
        while self.running:
            clock.tick(60)
            self.handle_events()
            self.draw()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                self.running = False  # Set running flag to False to exit the main loop
            elif event.type == KEYDOWN:
                if event.key == K_RETURN:
                    self.send_message()
                elif event.key == K_BACKSPACE:
                    self.user_input = self.user_input[:-1]
                else:
                    self.user_input += event.unicode

    def draw(self):
        self.screen.fill(self.background_color)

        # Display chat messages from both clients
        y_offset = 20
        for message in self.chat_messages:
            nickname, content = message.split(": ", 1)
            text_surface = self.font.render(content, True, self.text_color)
            text_width = text_surface.get_width()

            if nickname == self.player_name:  # Align own messages to center
                if text_width > 600:
                    text_width = 600  # Limit message width to fit the window
                self.screen.blit(text_surface, (600 - text_width - 20, y_offset))
            else:  # Align messages from other clients to the left
                self.screen.blit(text_surface, (20, y_offset))

            y_offset += 20

            # Draw text input box with curved edges
            input_rect = pygame.Rect(50, 480, 490, 40)
            pygame.draw.rect(self.screen, (255, 255, 255), input_rect,
                             border_radius=20)  # Text box background with curves
            input_surface = self.font.render(f">> {self.user_input}", True, self.text_color)
            self.screen.blit(input_surface,
                             (input_rect.x + 5, input_rect.y + 5))  # Adjusted position for client text box

        pygame.display.flip()

    def send_message(self):
        if self.user_input:
            message = f"{self.player_name}: {self.user_input}"  # Include player's name in the message
            self.client.send(message.encode('utf-8'))
            self.chat_messages.append(message)  # Append own message to chat_messages
            self.user_input = ""

    def receive_messages(self):
        while True:
            try:
                message = self.client.recv(1024).decode('utf-8')
                if message:
                    self.chat_messages.append(message)  # Append received message to chat_messages
            except:
                self.client.close()
                break

# Pygame setup for client window
def draw_client_window():
    host = '127.0.0.1'
    port = 8080  # Updated port for chat server
    if len(sys.argv) > 1:
        player_name = sys.argv[1]
    else:
        player_name = "Player 1"
    chat_client = ChatClient(host, port, player_name)

if __name__ == "__main__":
    # Open the client Pygame window
    draw_client_window()
