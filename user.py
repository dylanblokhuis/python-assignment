class User:
    name: str = ""
    client_socket = None
    address: str = ""
    messages: list = []

    def __init__(self, name, client_socket, address):
        self.name = name
        self.client_socket = client_socket
        self.address = address
