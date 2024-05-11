import socket
import threading

HOST = '127.0.0.1'
PORT = 8080

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))

clients = []

def broadcast(message, sender):
    for client in clients:
        if client != sender:
            client.send(message)

def handle_client(client):
    while True:
        try:
            message = client.recv(1024)
            broadcast(message, client)  # Pass sender as an argument
        except:
            clients.remove(client)
            client.close()
            break

def start_server():
    server.listen()
    print(f'Server is listening on {HOST}:{PORT}')
    while True:
        client, address = server.accept()
        print(f'Connected with {address}')
        clients.append(client)
        thread = threading.Thread(target=handle_client, args=(client,))
        thread.start()

if __name__ == "__main__":
    # Start the server in a separate thread
    server_thread = threading.Thread(target=start_server)
    server_thread.start()
