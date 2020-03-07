class User:
    name: str
    socket: object
    address: str
    messages: list

    def __init__(self, name, socket, address):
        self.name = name
        self.socket = socket
        self.address = address
