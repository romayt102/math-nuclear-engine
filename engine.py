import os

class Engine:
    def __init__(self):
        pass

    def cls(self):
        os.system('cls' if os.name == 'nt' else 'clear')