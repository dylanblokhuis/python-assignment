import threading
import pickle
import socket
import time
from chatroom import Chatroom
from typing import List
from storage import Storage

chatrooms_pkl_path = 'storage/chatrooms.pkl'
BUFFER = 4096

"""
naam: Dylan Blokhuis
datum: 23 februari 2020
leerlijn: Python
"""


class Server:
    chatrooms: List[Chatroom] = []

    def __init__(self):
        self.__fetch_existing_chatrooms()

    def __fetch_existing_chatrooms(self):
        storage = Storage(chatrooms_pkl_path)

        data = storage.get_data()
        if data:
            self.set_chatrooms(data)
        else:
            chatroom = Chatroom('First chatroom')

            chatrooms = self.get_chatrooms()
            chatrooms.append(chatroom)
            self.set_chatrooms(chatrooms)
            self.save_chatrooms()

    def save_chatrooms(self):
        storage = Storage(chatrooms_pkl_path)
        for chatroom in self.get_chatrooms():
            chatroom.set_users([])

        storage.set_data(self.get_chatrooms())

    def start_main_server(self):
        # main server for a client to fetch available chatrooms
        try:
            main_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            main_server.bind(('0.0.0.0', 1234))
            main_server.listen()
            print("Starting main server on port 1234")
        except Exception as ex:
            print(f'Port 1234 has already been used, please setup another in the server.py and client.py\n'
                  f'Expection: {ex}')
            exit(0)

        while True:
            client_socket, address = main_server.accept()
            # create another thread for each client
            self.__new_main_server_client(client_socket, address)

            try:
                chatroom_name = client_socket.recv(BUFFER).decode("utf-8")
                if chatroom_name == "":
                    continue

                chatroom = Chatroom(chatroom_name)
                port = chatroom.start()

                chatrooms = self.get_chatrooms()
                chatrooms.append(chatroom)
                self.set_chatrooms(chatrooms)
                # send the client the port for it to connect to
                client_socket.send(bytes(f'{port}', 'utf-8'))
                client_socket.close()
            except EOFError as ex:
                print(ex)

    def __new_main_server_client(self, client_socket, address):
        def no_socket_in_pickle(item):
            return {
                "name": item.name,
                "port": item.port
            }

        _chatrooms = list(map(no_socket_in_pickle, self.get_chatrooms()))

        client_socket.send(bytes(pickle.dumps(_chatrooms)))

    def get_chatrooms(self):
        return self.chatrooms

    def set_chatrooms(self, _chatrooms):
        self.chatrooms = _chatrooms


if __name__ == '__main__':
    server = Server()

    chatrooms = server.get_chatrooms()

    thread = threading.Thread(target=server.start_main_server)
    thread.daemon = True
    thread.start()

    for chatroom in chatrooms:
        chatroom.start()

    # maybe disable
    while True:
        try:
            time.sleep(3)
        except KeyboardInterrupt:
            server.save_chatrooms()

            exit(0)
