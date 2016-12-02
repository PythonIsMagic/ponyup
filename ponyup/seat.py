"""
  " Seats manage Players, chip stack, and Hands.
  """
from ponyup import hand


class Seat(object):
    """ Defines a Seat object that occupies a Table.  """
    def __init__(self, num):
        self.NUM = num  # Need to set the seat number in the table.
        self.player = None
        # Set the hand to a new empty Hand
        self.hand = hand.Hand()
        self.stack = 0

    def __str__(self):
        if self.player is None:
            return 'Open Seat'
        else:
            return str(self.player)

    def __eq__(self, other):
        """ Compares this seat to another seat and returns True if all attributes
            match.
        """
        if self.player != other.player:
            return False
        elif self.stack != other.stack:
            return False
        elif self.NUM != other.NUM:
            return False
        else:
            return True

    def sitdown(self, player):
        """ Takes a Player and sets them in this seat if not occupied. """
        if not self.vacant():
            raise Exception('The seat is currently occupied!')
        else:
            self.player = player
            self.hand = hand.Hand()

    def standup(self):
        """ Remove the Player from this seat and refund their money. """
        # Give their chips back
        self.player.deposit(self.stack)
        self.stack = 0
        p = self.player
        self.player = None
        return p

    def vacant(self):
        return self.player is None

    def occupied(self):
        return self.player is not None

    def has_hand(self):
        """ Returns True if the player at this seat currently has a Hand, False otherwise """
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
        """ Award the given amount of chips to the current players stack. """
        self.check_amount(amount)
        self.stack += amount

    def bet(self, amt):
        """ Removes the given amount from the players stack and returns it as an integer. """
        self.check_amount(amt)
        if amt > self.stack:
            amt = self.stack
        self.stack -= amt
        return amt

    def fold(self):
        """ Removes all the cards in the hand and returns them as a list. """
        copy = self.hand.cards[:]
        self.hand.cards = []
        return copy


def check_amount(amt):
    if amt <= 0:
        raise ValueError('Bet amount must be a positive number!')
