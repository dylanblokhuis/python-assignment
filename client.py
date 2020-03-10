import socket
import pickle
import utils
import time
import sys
from threading import Thread

BUFFER = 4096

user_name = input("Whats your username? \n> ")


def get_chatrooms():
    main_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP)
    main_server.connect(('127.0.0.1', 1234))
    while True:
        main_server_msg = main_server.recv(BUFFER)
        try:
            data = pickle.loads(main_server_msg)
            main_server.close()
            return data
        except EOFError:
            pass


def prompt(server):
    while True:
        try:
            payload = input(f'{user_name}> ')
            if payload:
                if payload == 'quit':
                    server.close()
                    break
                server.send(payload.encode("utf-8"))
        except KeyboardInterrupt:
            server.close()
            break


def receive_messages(server):
    while True:
        try:
            msg = server.recv(BUFFER)
            print(msg.decode("utf-8"))

            thread = Thread(target=prompt, args=[server])
            thread.daemon = True
            thread.start()
        except:
            continue


def join_chatroom(chatroom):
    print(f'Joining: {chatroom.name}')
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP)
    server.connect(('0.0.0.0', chatroom.port))
    server.setblocking(False)
    server.send(user_name.encode("utf-8"))

    thread = Thread(target=receive_messages, args=[server])
    thread.daemon = True
    thread.start()


chatrooms = get_chatrooms()
answer = utils.prompt("Which chatroom would you like to join?", list(map(lambda question: question.name, chatrooms)))

for chatroom in chatrooms:
    if chatroom.name == answer:
        join_chatroom(chatroom)

while True:
    try:
        # 100% cpu usage woo
        # time.sleep(.1)
        time.sleep(3)
    except KeyboardInterrupt:
        print("Shutting down...")
        exit(0)
