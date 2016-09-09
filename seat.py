class Seat():
    def __init__(self, table):
        self.table = table
        self.player = None
        self.hand = None
        self.chips = 0

    def sitdown(self, player):
        # Check that this player isn't already at the table.

        # Set the player
        self.player = player

    def standup(self):
        # If no player is sitting, raise an exception
        if self.player is None:
            raise Exception('There is no player to stand up from this seat!')

        # Give their chips back
        self.player.add_chips(self.chips)
        self.chips = 0
        # Remove the player
        self.player = None

    def is_empty(self):
        return self.player is None

    def has_hand(self):
        pass

    def show_hand(self):
        pass

    def has_chips(self):
        pass

    def buy_chips(self, amount):
        self.chips += self.player.bet(amount)

    def bet(self, amount):
        pass

    def is_allin(self):
        pass

    def fold(self, c):
        pass
