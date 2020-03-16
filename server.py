import threading
import pickle
import os
import socket
import time
from chatroom import Chatroom
from typing import List

chatrooms_pkl_path = 'storage/chatrooms.pkl'


class Server:
    chatrooms: List[Chatroom] = []

    def __init__(self):
        self.fetch_existing_chatrooms()

    def fetch_existing_chatrooms(self):
        # check if file is not empty
        if os.path.getsize(chatrooms_pkl_path) > 0:
            # get chatrooms from pickle
            with open(chatrooms_pkl_path, 'rb') as chatroom_pkl:
                self.set_chatrooms(pickle.load(chatroom_pkl))
        else:
            # since there are no chatrooms we need to create one
            with open(chatrooms_pkl_path, 'wb') as output:
                # we define port as 0 to get a random open one
                chatroom = Chatroom('First chatroom')
                chatrooms = self.get_chatrooms()
                self.set_chatrooms(chatrooms.append(chatroom))
                # chatroom1 = Chatroom('Second chatroom')
                # chatrooms.append(chatroom1)
                pickle.dump(chatrooms, output, pickle.HIGHEST_PROTOCOL)

    def start_main_server(self):
        # main server for a client to fetch available chatrooms
        main_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP)
        main_server.bind(('0.0.0.0', 1234))
        main_server.listen()
        print("Starting main server on port 1234")

        while True:
            client_socket, address = main_server.accept()
            client_socket.send(bytes(pickle.dumps(self.get_chatrooms())))
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
        chatroom.start()

    while True:
        try:
            time.sleep(3)
        except KeyboardInterrupt:
            print("Shutting down...")
            exit(0)


