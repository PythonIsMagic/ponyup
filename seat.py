class Seat():
    def __init__(self, player=None):
        self.player = None
        self.hand = None
        self.chips = 0

    def sitdown(self, player):
        self.player = player

    def standup(self, player):
        pass

    def is_empty(self):
        return self.player is None

    def has_hand(self):
        pass

    def show_hand(self):
        pass

    def has_chips(self):
        pass

    def buy_chips(self, amount):
        pass

    def bet(self, amount):
        pass

    def is_allin(self):
        pass

    def fold(self, c):
        pass