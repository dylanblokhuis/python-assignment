import socket


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
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP)
        server.bind(('127.0.0.1', self.port))
        server.listen(5)
        print(f'Started chatroom server: \"{self.name}\" on port {self.port}')
        return server
