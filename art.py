from colors import Colors

"""
naam: Dylan Blokhuis
datum: 27 maart 2020
leerlijn: Python
"""


class Art:
    string: str

    def __init__(self, string):
        self.string = string

    def title(self):
        line = '----------------------- \n'
        return line + f'{Colors.BLUE}{self.string}{Colors.ENDC}\n' + line

    def with_color(self):
        return f'{Colors.BLUE}{self.string}{Colors.ENDC}'
