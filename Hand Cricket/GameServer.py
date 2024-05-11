import socket
from _thread import *
import pickle
from game import Game

server = "127.0.0.1"
port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    str(e)

s.listen(5)
print("Waiting for a connection, Server Started")

connected = set()
games = {}
idCount = 0


def threaded_client(conn, p, gameId):
    global idCount
    conn.send(str.encode(str(p)))

    reply = ""
    while True:
        try:
            data = conn.recv(4096).decode()

            if gameId in games:
                game = games[gameId]

                if not data:
                    break
                else:
                    if data == "reset":
                        game.resetWent()
                    elif data == "score":
                        print("no pblem")
                        print("game.done_bat[0] = ", game.done_bat[0], "and game.done_bat[0] =", game.done_bat[1])
                        if game.done_bat[0] == 1 and game.bothWent():
                            print("2nd player as batsman")
                            game.score[1] = game.batsman(1, 0, game.score[1])
                            print("completed1")
                        elif game.bothWent():
                            print("1nd player as batsman")
                            game.score[0] = game.batsman(0, 1, game.score[0])
                            print("completed2")
                        game.resetWent()
                    elif data != "get":
                        game.play(p, data)

                    conn.sendall(pickle.dumps(game))
            else:
                break
        except:
            break

    print("Lost connection")
    try:
        del games[gameId]
        print("Closing Game", gameId)
    except:
        pass
    idCount -= 1
    conn.close()


while True:
    conn, addr = s.accept()
    print("Connected to:", addr)

    idCount += 1
    p = 0
    gameId = (idCount - 1) // 2
    print(idCount)
    if idCount % 2 == 1:
        games[gameId] = Game(gameId)
        print("Creating a new game...")
    else:
        print("2nd connected")
        games[gameId].ready = True
        p = 1

    start_new_thread(threaded_client, (conn, p, gameId))
