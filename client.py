import socket
import pickle
import utils
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

    def connect(self, port: int):
        print(f'Joining server on {port}')

        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP)
        server.connect(('0.0.0.0', port))
        server.send(self.get_user_name().encode("utf-8"))

        thread = Thread(target=self.receive, args=[server])
        thread.daemon = True
        thread.start()

        self.prompt(server)

    def receive(self, server):
        while True:
            try:
                msg = server.recv(BUFFER)
                print(msg.decode("utf-8"))
            except:
                continue

    def prompt(self, server):
        while True:
            try:
                payload = input()
                if payload:
                    if payload == 'quit':
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
    client = Client(user_name)

    chatrooms = fetch_chatrooms()
    chosen_chatroom = utils.prompt("Which chatroom would you like to join?",
                                   list(map(lambda question: question.name, chatrooms)))

    for chatroom in chatrooms:
        if chatroom.name == chosen_chatroom:
            client.connect(chatroom.port)

    while True:
        try:
            # 100% cpu usage woo
            # time.sleep(.1)
            time.sleep(3)
        except KeyboardInterrupt:
            print("Shutting down...")
            exit(0)
