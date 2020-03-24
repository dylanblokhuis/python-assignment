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

    def get_name(self):
        return self.name

    def get_client_socket(self):
        return self.client_socket

    def get_address(self):
        return self.address

    def get_messages(self):
        return self.messages

    def set_messages(self, messages):
        self.messages = messages

