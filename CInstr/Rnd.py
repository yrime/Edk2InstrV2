import random

class Rnd:
    def __init__(self):
        self.i = random.randint(0, 0xffffffff)

    def rand(self):
        self.i += (3 + self.i * 2)
        self.i %= 0xffffffff
        return self.i