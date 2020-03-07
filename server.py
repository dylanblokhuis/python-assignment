import threading
import pickle
import os
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
        chatroom = Chatroom('First chatroom', 0)
        chatrooms.append(chatroom)
        pickle.dump(chatrooms, output, pickle.HIGHEST_PROTOCOL)


def new_user(client_socket, address):
    client_socket.send(bytes("Welcome to the club", "utf-8"))

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


for chatroom in chatrooms:
    server = chatroom.start()
    while True:
        client_socket, address = server.accept()
        thread = threading.Thread(target=new_user(client_socket, address))
        thread.start()
        thread.join()
