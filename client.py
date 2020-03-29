import socket
import pickle
from question_prompter import QuestionPrompter
import time
from threading import Thread

BUFFER = 4096

"""
naam: Dylan Blokhuis
datum: 23 februari 2020
leerlijn: Python
"""


def fetch_chatrooms(main_server):
    while True:
        main_server_msg = main_server.recv(BUFFER)
        try:
            data = pickle.loads(main_server_msg)
            return data
        except EOFError:
            pass


def choose_chatroom(main_server):
    chatrooms = fetch_chatrooms(main_server)
    join_option = {
        "name": "Create a new chatroom",
        "port": 0
    }
    chatrooms.insert(0, join_option)

    chosen_chatroom = QuestionPrompter(
        list(map(lambda question: question['name'], chatrooms))
    ).prompt("Which chatroom would you like to join?")

    for chatroom in chatrooms:
        if chatroom['name'] == chosen_chatroom:
            if chatroom['port'] == 0:
                return False
            else:
                return chatroom['port']


def create_chatroom(main_server, name):
    main_server.send(name.encode('utf-8'))
    while True:
        main_server_msg = main_server.recv(BUFFER)
        try:
            port = main_server_msg.decode("utf-8")
            return int(port)
        except EOFError:
            pass


class Client:
    user_name: str

    def __init__(self, name):
        self.user_name = name

    def connect(self, port: int):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP)
        server.connect(('0.0.0.0', port))
        server.send(self.get_user_name().encode("utf-8"))

        thread = Thread(target=self.__receive, args=[server])
        thread.daemon = True
        thread.start()

        self.__prompt(server)

    def __receive(self, server):
        while True:
            try:
                msg = server.recv(BUFFER)
                print(msg.decode("utf-8"))
            except:
                continue

    def __prompt(self, server):
        while True:
            try:
                payload = input()
                if payload:
                    if payload == '!quit':
                        server.close()
                        exit(0)
                        break
                    server.send(payload.encode("utf-8"))
            except KeyboardInterrupt:
                server.close()
                exit(0)
                break

    def get_user_name(self):
        return self.user_name


if __name__ == '__main__':
    user_name = input("Whats your username? \n> ")
    # main server to fetch chatrooms or other options
    main_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP)
    main_server.connect(('0.0.0.0', 1234))
    client = Client(user_name)

    has_chosen_chatroom = choose_chatroom(main_server)

    if has_chosen_chatroom:
        main_server.close()
        client.connect(has_chosen_chatroom)
    else:
        chatroom_name = input("What do you want your chatroom to be called?\n> ")
        port = create_chatroom(main_server, chatroom_name)
        main_server.close()
        client.connect(port)

    while True:
        try:
            # 100% cpu usage woo
            # time.sleep(.1)
            time.sleep(3)
        except KeyboardInterrupt:
            print("Shutting down...")
            exit(0)
