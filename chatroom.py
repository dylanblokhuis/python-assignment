import socket
from threading import Thread
from user import User


class Chatroom:
    name: str
    slug: str
    port: int
    users: list
    commands: list

    def __init__(self, name, port):
        self.name = name
        self.port = port

    def start(self):
        thread = Thread(target=self.new_server)
        thread.daemon = True
        thread.start()

    def new_server(self):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP)
        server.bind(('127.0.0.1', self.port))
        server.listen(5)
        print(f'Started chatroom server: \"{self.name}\" on port {self.port}')

        while True:
            client_socket, address = server.accept()
            self.new_client(client_socket, address)

    def new_client(self, client_socket, address):
        client_socket.send(bytes(f'Welcome to {self.name}', "utf-8"))

        while True:
            message = client_socket.recv(2048)
            try:
                if message:
                    print(f'{address} - {message.decode("utf-8")}')
                else:
                    print("Closing client connection")
                    break
            except:
                continue

        client_socket.close()
