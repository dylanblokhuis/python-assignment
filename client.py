import socket
import pickle
import utils

user_name = input("Whats your username? \n> ")


def get_chatrooms():
    main_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP)
    main_server.connect(('127.0.0.1', 1234))
    while True:
        main_server_msg = main_server.recv(4096)
        try:
            return pickle.loads(main_server_msg)
        except EOFError:
            pass


chatrooms = get_chatrooms()
answer = utils.prompt("Which chatroom would you like to join?", list(map(lambda question: question.name, chatrooms)))

selected_chatroom = object
for chatroom in chatrooms:
    if chatroom.name == answer:
        selected_chatroom = chatroom

print(f'Joining: {selected_chatroom.name}')
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP)
server.connect(('0.0.0.0', selected_chatroom.port))
server.send(user_name.encode("utf-8"))
payload = ""

while True:
    msg = server.recv(2048)
    print(msg.decode("utf-8"))

    while True:

        try:
            payload = input(f'{user_name}> ')
        except KeyboardInterrupt:
            server.close()
            break

        if payload == 'quit':
            server.close()
            break
        server.send(payload.encode("utf-8"))
