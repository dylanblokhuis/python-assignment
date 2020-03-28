import socket
from art import Art
from threading import Thread
from user import User
from command import Command
from typing import List
from message import Message

BUFFER = 4096

"""
naam: Dylan Blokhuis
datum: 7 maart 2020
leerlijn: Python
"""


class Chatroom:
    name: str
    port: int
    users: List[User] = []
    commands: List[Command] = []

    def __init__(self, name):
        self.name = name

    def start(self):
        # clean properties for a safer thread
        self.set_users([])
        self.set_commands([])

        self.default_commands()
        self.__new_socket()

    def broadcast(self, message, _from):
        for user in self.get_users():
            try:
                user.client_socket.send(f'[{_from}]: {message}'.encode("utf-8"))
            except Exception as ex:
                print(f'Expection occured in broadcast: {ex}')
                user.client_socket.close()
                users = self.get_users()
                users.remove(user)
                self.set_users(users)

    def __new_socket(self):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind(('0.0.0.0', 0))
        server.listen()
        self.set_port(server.getsockname()[1])

        print(f'Started chatroom server: \"{self.get_name()}\" on port {self.get_port()}')
        while True:
            client_socket, address = server.accept()
            # create another thread for each client
            thread = Thread(target=self.__new_client, args=(client_socket, address))
            thread.daemon = True
            thread.start()

    def __new_client(self, client_socket, address):
        print(f'Connection established with {address}')

        user_name = client_socket.recv(BUFFER).decode("utf-8")
        user = User(user_name, client_socket, address)

        user.get_client_socket().send(
            f'Welcome to the server, {user.get_name()}\nYou can leave the server by using the !quit command'.encode(
                "utf-8"))
        for command in self.get_commands():
            if command.name == "commands":
                user.get_client_socket().send(bytes(command.invoke(), 'utf-8'))

        users = self.get_users()
        users.append(user)
        self.set_users(users)

        self.broadcast(f'{user.get_name()} joined the chat!', 'SERVER')

        while True:
            try:
                message = user.get_client_socket().recv(BUFFER)

                if message:
                    decoded_message = Message(message.decode("utf-8"))
                    user_messages = user.get_messages()
                    user_messages.append(decoded_message.get_message())
                    user.set_messages(user_messages)

                    if decoded_message.is_command():
                        for command in self.get_commands():
                            if command.get_name() == decoded_message.get_message()[1:]:
                                user.get_client_socket().send(bytes(command.invoke(), 'utf-8'))
                    else:
                        self.broadcast(decoded_message.get_message(), user.get_name())

            except Exception as ex:
                print(f'Expection occurred in __new_client: {ex}')
                break

        user.get_client_socket().close()
        users = self.get_users()
        users.remove(user)
        self.set_users(users)
        print("Closing client connection")

    def default_commands(self):
        users_command = Command("users", self.format_users)
        commands_command = Command("commands", self.format_commands)

        commands = self.get_commands()
        commands.append(users_command)
        commands.append(commands_command)
        self.set_commands(commands)

    def format_users(self):
        user_names = map(lambda user: f'{user.get_address()} - {user.name} \n', self.get_users())

        return Art("List of users").title() + ''.join(user_names)

    def format_commands(self):
        commands = map(lambda command: f'!{command.name} \n', self.get_commands())

        return Art("Available commands").title() + ''.join(commands)

    def get_name(self):
        return self.name

    def get_port(self):
        return self.port

    def set_port(self, port):
        self.port = port

    def get_users(self):
        return self.users

    def set_users(self, users):
        self.users = users

    def get_commands(self):
        return self.commands

    def set_commands(self, commands):
        self.commands = commands
