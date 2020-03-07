class User:
    name: str
    socket_address: str
    messages: list

    def __init__(self, name, socket_address):
        self.name = name
        self.socket_address = socket_address
