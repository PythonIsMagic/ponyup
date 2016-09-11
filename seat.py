import hand


class Seat():
    def __init__(self, num):
        self.NUM = num  # Need to set the seat number in the table.
        self.player = None
        # Set the hand to a new empty Hand
        self.hand = hand.Hand()
        self.stack = 0

    def __str__(self):
        return str(self.player)

    def sitdown(self, player):
        # Set the player
        if not self.is_empty():
            raise Exception('The seat is currently occupised!')
        else:
            self.player = player
            self.hand = hand.Hand()

    def standup(self):
        # If no player is sitting, raise an exception
        if self.player is None:
            raise Exception('There is no player to stand up from this seat!')

        # Give their chips back
        self.player.deposit(self.stack)
        self.stack = 0
        p = self.player
        self.player = None
        return p

    def is_empty(self):
        return self.player is None

    def has_hand(self):
        if self.hand is None:
            return False
        else:
            return len(self.hand) > 0

    def has_chips(self):
        return self.stack > 0

    def buy_chips(self, amount):
        if amount > self.player.bank:
            raise ValueError('Player cannot buy more chips than they can afford!')
        self.stack += self.player.withdraw(amount)

    def win(self, amount):
        self.check_amount(amount)
        self.stack += amount

    def bet(self, amt):
        self.check_amount(amt)
        if amt > self.stack:
            amt = self.stack
        self.stack -= amt
        return amt

    def fold(self):
        """
        Removes all the cards in the hand and returns them as a list.
        """
        copy = self.hand.cards[:]
        self.hand.cards = []
        return copy

    def check_amount(self, amt):
        if amt <= 0:
            raise ValueError('Bet amount must be a positive number!')
