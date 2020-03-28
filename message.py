"""
naam: Dylan Blokhuis
datum: 24 maart 2020
leerlijn: Python
"""


class Message:
    message: str

    def __init__(self, string: str):
        self.message = string

    def is_command(self):
        if self.get_message()[0] == '!':
            return True
        else:
            return False

    def get_message(self):
        return self.message
