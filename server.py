import threading
import pickle
import os
import socket
import time
from chatroom import Chatroom

chatrooms_pkl_path = 'storage/chatrooms.pkl'
chatrooms = []

# check if file is not empty
if os.path.getsize(chatrooms_pkl_path) > 0:
    # get chatrooms from pickle
    with open(chatrooms_pkl_path, 'rb') as chatroom_pkl:
        chatrooms = pickle.load(chatroom_pkl)
else:
    # since there are no chatrooms we need to create one
    with open(chatrooms_pkl_path, 'wb') as output:
        # we define port as 0 to get a random open one
        chatroom = Chatroom('First chatroom', 23528)
        chatrooms.append(chatroom)
        chatroom1 = Chatroom('Second chatroom', 39284)
        chatrooms.append(chatroom1)
        pickle.dump(chatrooms, output, pickle.HIGHEST_PROTOCOL)


def start_main_server():
    # main server for a client to fetch available chatrooms
    main_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP)
    main_server.bind(('127.0.0.1', 1234))
    main_server.listen(5)
    print("Starting main server on port 1234")

    while True:
        client_socket, address = main_server.accept()
        client_socket.send(bytes(pickle.dumps(chatrooms)))
        client_socket.close()


thread = threading.Thread(target=start_main_server)
thread.daemon = True
thread.start()

for chatroom in chatrooms:
    chatroom.start()

while True:
    try:
        time.sleep(.1)
    except KeyboardInterrupt:
        print("Shutting down...")
        exit(0)


