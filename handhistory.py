import datetime

"""
Hand history logger. Logs the actions that take place during a round of poker.

For a normal hand history file, we will start with a header:
        * PonyupPoker Poker Game
        * Game ID#
        * Table name,
        * stakes,
        * Game type
        * time,
        * date
        * Seats, names, stack sizes

Full Tilt Poker Game #108180711: Table Pilot - $1/$2 - Limit Hold'em - 12:11:53 ET - 2009/02/24
"""
LOGDIR = 'logs/'


class HandHistory():
    def __init__(self, _round):
        self.dt = datetime.datetime
        self.r = _round
        self.text = ''
        self.write_header()
        self.write_player_list()
        self.filename = self.generate_filename()

    def generate_filename(self):
        stakes = '${}-${}'.format(self.r.blinds.SMBET, self.r.blinds.SMBET * 2)
        filename = 'HH_{}_-_{}_{}_{}(Pony Bits)'.format(
            self.dt.now().strftime('%Y%m%d'),
            self.r._table.name,
            self.r.gametype,
            stakes
        )
        return LOGDIR + filename

    def write_header(self):
        date = self.dt.today()
        time = self.dt.now().strftime('%Y-%m-%d %H:%M:%S')
        header = 'PonyUp Poker Game ID# {}: Table {} - {} - {} - {}\n'.format(
            self.r.gameid,
            self.r._table.name,
            self.r.blinds.stakes(),
            self.r.gametype,
            time,
            date)
        self.text += header

    def button(self):
        self.text += 'Seat {} has the button.\n'.format(self.r._table.TOKENS['D'])

    def write_player_list(self):
        self.text += self.r._table.player_listing()

    def write_tokens(self):
        # Note who has the button, SB, BB, bringin, etc.
        pass

    def log(self, text):
        self.text += text + '\n'

    def write_to_file(self):
        with open(self.filename, 'a') as f:
            for l in self.text:
                f.write(l)


def decorate(text):
    return '\n~~/) ' + text + ' (\~~'
    # /)(\ (\/)
    #  self.text += '~~(\ ' + text + ' /)~~'
