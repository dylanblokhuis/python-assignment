import threading
import pickle
import socket
import time
from chatroom import Chatroom
from typing import List
from storage import Storage

chatrooms_pkl_path = 'storage/chatrooms.pkl'

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
            chatroom1 = Chatroom('Second chatroom')

            chatrooms = self.get_chatrooms()
            chatrooms.append(chatroom)
            chatrooms.append(chatroom1)
            self.set_chatrooms(chatrooms)
            storage.set_data(chatrooms)

    def start_main_server(self):
        # main server for a client to fetch available chatrooms
        main_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        main_server.bind(('0.0.0.0', 1234))
        main_server.listen()
        print("Starting main server on port 1234")

        while True:
            client_socket, address = main_server.accept()
            # create another thread for each client
            self.__new_main_server_client(client_socket, address)

    def __new_main_server_client(self, client_socket, address):
        def no_socket_in_pickle(item):
            return {
                "name": item.name,
                "port": item.port
            }

        _chatrooms = list(map(no_socket_in_pickle, self.get_chatrooms()))

        client_socket.send(bytes(pickle.dumps(_chatrooms)))
        client_socket.close()

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
        thread = threading.Thread(target=chatroom.start)
        thread.daemon = True
        thread.start()

    while True:
        try:
            time.sleep(3)
        except KeyboardInterrupt:
            print("Shutting down...")
            exit(0)
