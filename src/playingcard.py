from . import card
Card = card.Card

SUITS = ('c', 'd', 'h', 's')
SUITVALUES = {'c': 1, 'd': 2, 'h': 3, 's': 4}
FACECARDS = {'T': 10, 'J': 11, 'Q': 12, 'K': 13, 'A': 14, 'Z': 15}
RANKS = dict({str(x): x for x in range(2, 10)}, **FACECARDS)


class PlayingCard(Card):
    """ Manages an instance of a PlayingCard, which has a rank and suit."""
    def __init__(self, rank, suit):
        if rank not in RANKS:
            raise ValueError('Corrupt card construction - {} is not a valid rank!'.format(rank))
        if suit not in SUITS:
            raise ValueError('Corrupt card construction - {} is not a valid suit!'.format(suit))
        Card.__init__(self, rank + suit)

        self.rank = rank
        self.suit = suit

    def __gt__(self, other):
        """ Returns True if this card's rank is greater than the other card, False otherwise. """
        return RANKS[self.rank] > RANKS[other.rank]

    def __lt__(self, other):
        """ Returns True if this card's rank is lesser than the other card, False otherwise. """
        return RANKS[self.rank] < RANKS[other.rank]

    def val(self):
        """ Returns the value of the Cards rank. """
        return RANKS[self.rank]
