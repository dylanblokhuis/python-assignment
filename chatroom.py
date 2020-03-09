import socket
from threading import Thread
from user import User
from typing import List


class Chatroom:
    name: str
    slug: str
    port: int
    users: List[User] = []
    commands: list

    def __init__(self, name):
        self.name = name

    def start(self):
        thread = Thread(target=self.new_socket)
        thread.daemon = True
        thread.start()

    def broadcast(self, message, _from):
        for user in self.users:
            user.client_socket.send(f'[{_from}]: {message}'.encode("utf-8"))

    def new_socket(self):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind(('0.0.0.0', 0))
        server.listen()
        self.port = server.getsockname()[1]

        print(f'Started chatroom server: \"{self.name}\" on port {self.port}')
        # TODO: each chatroom is now a thread, but each connection is not a thread
        while True:
            client_socket, address = server.accept()
            self.new_client(client_socket, address)

    def new_client(self, client_socket, address):
        client_socket.send(f'Welcome to {self.name}\n'.encode("utf-8"))
        user_name = client_socket.recv(2048).decode("utf-8")
        user = User(user_name, client_socket, address)

        self.users.append(user)
        self.broadcast(f'{user.name} joined the chat!', 'SERVER')

        while True:
            message = user.client_socket.recv(2048)
            try:
                if message:
                    print(message.decode("utf-8"))
                    self.broadcast(message.decode("utf-8"), user.name)
                else:
                    self.users.remove(user)
                    user.client_socket.close()
                    print("Closing client connection")
                    break
            except:
                continue
