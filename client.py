import socket
import pickle
from question_prompter import QuestionPrompter
import time
from threading import Thread

BUFFER = 4096


def fetch_chatrooms():
    main_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP)
    main_server.connect(('0.0.0.0', 1234))
    while True:
        main_server_msg = main_server.recv(BUFFER)
        try:
            data = pickle.loads(main_server_msg)
            main_server.close()
            return data
        except EOFError:
            pass


class Client:
    user_name: str

    def __init__(self, name):
        self.user_name = name

    def __connect(self, port: int):
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
                        self.choose_chatroom()
                        break
                    server.send(payload.encode("utf-8"))
            except KeyboardInterrupt:
                server.close()
                exit(0)
                break

    def choose_chatroom(self):
        chatrooms = fetch_chatrooms()
        chosen_chatroom = QuestionPrompter(
            list(map(lambda question: question['name'], chatrooms))
        ).prompt("Which chatroom would you like to join?")

        for chatroom in chatrooms:
            if chatroom['name'] == chosen_chatroom:
                self.__connect(chatroom['port'])

    def get_user_name(self):
        return self.user_name


if __name__ == '__main__':
    user_name = input("Whats your username? \n> ")
    client = Client(user_name)
    client.choose_chatroom()

    while True:
        try:
            # 100% cpu usage woo
            # time.sleep(.1)
            time.sleep(3)
        except KeyboardInterrupt:
            print("Shutting down...")
            exit(0)
