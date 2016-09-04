import player
import table


"""
Table factory.
"""
STARTINGCHIPS = 1000
STEP = 100


class BobTable(table.Table):
    def __init__(self, seats):
        super().__init__(seats)

        for i, s in enumerate(self.seats):
            self.add_player(i, player.Player('bob{}'.format(i), 'CPU'))
            self.seats[i].chips = STARTINGCHIPS
            #  s.chips = STARTINGCHIPS


class SteppedStackTable(table.Table):
    def __init__(self, seats):
        super().__init__(seats)

        for i, s in enumerate(self.seats):
            self.add_player(i, player.Player('bob{}'.format(i), 'CPU'))
            self.seats[i].chips = STEP * (i + 1)
