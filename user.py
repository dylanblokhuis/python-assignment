import socket


class User:
    name: str = ""
    client_socket: socket.socket
    address: str = ""
    messages: list = []

    def __init__(self, name, client_socket, address):
        self.name = name
        self.client_socket = client_socket
        self.address = address
