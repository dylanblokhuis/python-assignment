"""
naam: Dylan Blokhuis
datum: 24 maart 2020
leerlijn: Python
"""


class Command:
    name: str
    invokes: None

    def __init__(self, name, invokes):
        self.name = name
        self.invokes = invokes

    def get_name(self):
        return self.name

    def get_invokes(self):
        return self.invokes

    def invoke(self):
        return self.invokes()
