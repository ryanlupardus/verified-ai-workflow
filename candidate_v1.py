"""First AI-drafted implementation for the cart exercise."""


class Cart:
    def __init__(self):
        self.items = {}
        self.sessions = []

    def put(self, item, quantity):
        if len(item) != 1 or item not in "abcdefghijklmnopqrstuvwxyz":
            raise ValueError("Expected one lowercase letter")
        if type(quantity) is not int or not 0 <= quantity <= 9:
            raise ValueError("Quantity must be an integer from 0 to 9")
        self.items[item] = quantity

    def begin(self):
        self.sessions.append(self.items)

    def finish(self, save):
        if type(save) is not bool:
            raise TypeError("Expected a boolean")
        if not self.sessions:
            raise RuntimeError("No open session")
        prior = self.sessions.pop()
        if not save:
            self.items = prior

    def export(self):
        return self.items.copy()

    def read(self, item):
        return self.items.get(item)
