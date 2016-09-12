from __future__ import print_function
import betting
import colors
import console
import deck
import handhistory


class Round():
    def __init__(self, session):
        """
        Initialize the next round of Poker.
        """
        self.gametype = session.gametype
        self.label = session.label
        self.blinds = session.blinds
        self.streets = session.streets
        self._table = session._table
        self.hero = session.hero
        self.street = 0
        self.pot = 0

        self.muck = []
        self.d = deck.Deck()
        self.d.shuffle(17)  # Shuffle 17 times for good measure.
        self.DECKSIZE = len(self.d)

        #  Remember starting stacks of all players
        self.starting_stacks = self._table.stackdict()

        self.check_integrity_pre()

        self.hh = handhistory.HandHistory(self)

    def __str__(self):
        """
        Return info about the current round.
        """
        return console.display_table(self._table, self.hero)

    def show_pot(self):
        _str = 'Pot: '
        _str += colors.color('${}'.format(self.pot), 'yellow')
        return _str.rjust(84)

    def deal_cards(self, qty, faceup=False, handreq=False):
        """
        Deal the specified quantity of cards to each player. If faceup is True, the cards are
        dealt face-up, otherwise they are face-down.
        """
        for i in range(qty):
            for s in self._table:
                if handreq and not s.has_hand():
                    continue
                c = self.d.deal()
                if faceup is True:
                    c.hidden = False
                    self.log('{} was dealt [{}]'.format(s.player, c), echo=False)
                s.hand.add(c)

    def show_cards(self):
        """
        Unhides all player hands and returns a string that shows all the player hands.
        """
        _str = ''
        for s in self._table.get_players(hascards=True):
            s.hand.unhide()
            line = '{} shows {}\n'.format(str(s), str(s.hand))
            _str += line
        return _str

    def sortcards(self):
        """
        Sort all cards in all players hands.
        """
        for s in self._table:
            s.hand.sort()

    def muck_all_cards(self):
        """
        Muck all player hands, and muck the contents of the deck.
        """
        # Clear hands
        for s in self._table:
            self.muck.extend(s.fold())
        # Add the remainder of the deck
        while len(self.d) > 0:
            self.muck.append(self.d.deal())

    def post_antes(self):
        """
        All players bet the ante amount and it's added to the pot.
        """
        actions = ''
        for s in self._table:
            actions += '{} posts ${} ante.\n'.format(s, self.blinds.ANTE)
            self.pot += s.bet(self.blinds.ANTE)

        self.log(actions, echo=False)
        return actions

    def post_blinds(self):
        """
        Gets the small and big blind positions from the table and makes each player bet the
        appropriate mount to the pot. Returns a string describing what the blinds posted.
        """
        if self._table.TOKENS['D'] == -1:
            raise Exception('Button has not been set yet!')

        if len(self._table.get_players()) < 2:
            raise ValueError('Not enough players to play!')
            exit()
        sb = self._table.seats[self._table.TOKENS['SB']]
        bb = self._table.seats[self._table.TOKENS['BB']]

        # Bet the SB and BB amounts and add to the pot
        self.pot += sb.bet(self.blinds.SB)
        self.pot += bb.bet(self.blinds.BB)
        actions = ''
        actions += '{} posts ${}\n'.format(sb, self.blinds.SB)
        actions += '{} posts ${}'.format(bb, self.blinds.BB)

        self.log(actions, echo=False)
        return actions

    def invested(self, seat):
        """
        Return the difference between the players current stack-size and the amount at the
        start of the round.
        """
        return self.starting_stacks[seat.NUM] - seat.stack

    def get_allins(self):
        """
        Returns a list of all stack sizes that went all-in this round.
        """

        return [self.starting_stacks[s.NUM] for s in self._table if s.has_chips() is False]

    def make_sidepots(self, allins):
        """
        Sidepot is how much the given stack size(s) can win.  Takes in a list of all-in
        stack-size amounts and returns a dictionary of pot:stacksize pairs that show what
        sidepots are available and what stack size is required to win it.
        """
        POTS = {}

        for stacksize in sorted(allins):
            if stacksize in POTS:
                continue

            sidepot = self.calc_sidepot(stacksize)
            # Adjust the sidepot
            # The sidepot is what is leftover after taking off the next-lesser sidepot.
            if len(POTS) == 0:
                POTS[stacksize] = sidepot
            else:
                #  last_sidepot = POTS[max(POTS)]
                POTS[stacksize] = sidepot - sum(POTS.values())
        return POTS

    def calc_sidepot(self, stacksize):
        """
        Calculates the maximum value a stacksize can win from the current pot.
        """
        sidepot = 0
        for s in self._table:
            # Get the players total invested amount over the round
            i = self.invested(s)

            # If stacksize is less than invested, they can only win the stacksize.
            if stacksize <= i:
                sidepot += stacksize
            elif stacksize > i:
                # if their stacksize is more than invested, they can win the entire invested
                # amount.
                sidepot += i
        return sidepot

    def process_sidepots(self, sidepots):
        """
        Calculates which players are eligible to win which portions of the pot.
        Returns a dictionary of pot shares and player lists.
        """
        leftovers = self.pot
        shares = {}
        # If there are no sidepots, then there is no stacksize requirement to win the main pot.
        if len(sidepots) == 0:
            required_stack = 0
        else:
            required_stack = max(sidepots) + 1

        while len(sidepots) > 0:
            # Work up from the lowest stack to the highest.
            stack = min(sidepots)
            pot = sidepots[stack]
            leftovers -= pot

            # Determine which players can win this share of the pot.
            shares[pot] = self.eligible_for_pot(stack)

            # Move onto the next sidepot.
            sidepots.pop(stack)

        # Award what is leftover after the sidepots.
        if leftovers > 0:
            # required_stack lets anyone above the allin threshold win the leftovers.
            shares[leftovers] = self.eligible_for_pot(required_stack)
        return shares

    def get_eligible(self, stack_req):
        """
        Returns a list of seats that have the minimum starting stack size.
        """
        cardholders = self._table.get_players(hascards=True)
        return [s for s in cardholders if self.starting_stacks[s.NUM] >= stack_req]

    def eligible_for_pot(self, stack_required):
        """
        Makes a list of the players who qualify the given stack size and who have (or tie) the
        best hand of all cardholding players.
        """
        eligible_players = self.get_eligible(stack_required)
        best_hand = self.best_hand_val(eligible_players)
        return [s.NUM for s in eligible_players if s.hand.value() == best_hand]

    def best_hand_val(self, seats):
        """
        Determine the best handvalue within the given player group.
        """
        best = 0
        for s in seats:
            if s.hand.value() > best:
                best = s.hand.value()
        return best

    def split_pot(self, winners, amt):
        """
        Adds the specified pot amount to the players chips.  If there are multiple winners,
        they must split the pot If there is a remainder amount, we give it to the next left of
        the BTN.  (ie: Usually the SB)
        """
        award_dict = {}
        if len(winners) > 1:
            share = int(amt / len(winners))
            remainder = amt % len(winners)
        else:
            share = amt
            remainder = 0

        for w in winners:
            award_dict[w] = share

        if remainder > 0:
            first_after_btn = self._table.next_player(self._table.btn, hascards=True)
            r_winner = self._table.seats[first_after_btn].NUM
            award_dict[r_winner] += remainder
        return award_dict

    def showdown(self):
        """
        Compare all the hands of players holding cards and determine the winner(s). Awards each
        winner the appropriate amount.
        """
        self.log('Showdown!', decorate=True)
        self.log(self.show_cards())

        allins = self.get_allins()
        stack_shares = self.make_sidepots(allins)
        sidepots = self.process_sidepots(stack_shares)

        if not self.valid_sidepots(sidepots):
            raise Exception('Sidepots are not valid - they do not total the pot amount!')

        if len(sidepots) > 1:
            for i, s in enumerate(sidepots):
                self.log('Sidepot #{}: ${}'.format(i+1, s))

        award_txt = self.process_awards(sidepots)
        self.log(award_txt)

    def process_awards(self, award_dict):
        """
        Takes in the dictionary of awards/seats and awards each player their share. Uses
        split pot to correctly split up ties.
        """
        _str = ''
        for sidepot, winners in award_dict.items():
            for i, amt in self.split_pot(winners, sidepot).items():
                seat = self._table.seats[i]
                _str += '{} wins with a {}: {}\n'.format(
                    str(seat.player),
                    str(seat.hand.rank()),
                    str(seat.hand.desc())
                )
                _str += self.award_pot(seat, amt)
        return _str

    def award_pot(self, seat, amt):
        """
        Adds the specified amount to a players stack. Returns a string describing who won what.
        """
        seat.win(amt)
        return '{:} wins ${}\n'.format(str(seat.player), amt)

    def next_street(self):
        """
        Advanced the street counter by one.
        """
        if self.street >= len(self.streets):
            raise Exception('The last street has been reached on this game!')
        else:
            self.street += 1

    def valid_sidepots(self, sidepots):
        """
        Verifies that all sidepots add up to the current pot amount. If the sum of the sidepots
        equals the pot, returns True. Otherwise returns False.
        """
        total = 0
        for s in sidepots:
            total += s
        if total != self.pot:
            return False
        else:
            return True

    def check_integrity_pre(self):
        """
        Verify that the game elements are set up correctly.
        """
        # Check that the deck is full.
        if len(self.d) != self.DECKSIZE:
            return False
        # Check that the muck is empty.
        if len(self.muck) != 0:
            return False
        # Check that no players have cards.
        if len(self._table.get_players(hascards=True)) > 0:
            return False
        # Check that the pot is 0.
        if self.pot != 0:
            return False
        return True

    def check_integrity_post(self):
        """
        Verify that the game elements have been cleaned up correctly and that all cards are
        accounted for.
        """
        # Check that all cards have been used up.
        if len(self.d) != 0:
            return False
        # Check that the muck is the same size as the original starting deck.
        if len(self.muck) != self.DECKSIZE:
            return False
        # Check that all players have folded.
        if len(self._table.get_players(hascards=True)) > 0:
            return False
        # The sum of all sidepots should equal the potsize.

        return True

    def clear_broke_players(self):
        broke_players = self._table.get_broke_players()
        _str = ''
        for seat in broke_players:
            #  self._table.seats.remove(seat)
            seat.standup()
            _str += '{} left the table with no money!\n'.format(seat.player)

        # Log players leaving
        return _str

    def cleanup(self):
        self.muck_all_cards()
        self.hh.log(self.clear_broke_players())

        if not self.check_integrity_post():
            raise Exception('Integrity of game could not be verified after round was complete!')

    def one_left(self):
        cardholders = self._table.get_players(hascards=True)
        if len(cardholders) == 1:
            return cardholders.pop()
        else:
            return None

    def betting_over(self):
        """
        Checks the players and sees if any valid bettors are left to duke it out. If no more
        than 1 is left, the betting is over. Returns True if there is no more betting, False
        otherwise.
        """
        hands = len(self._table.get_players(hascards=True))
        broke = len(self._table.get_broke_players())
        if hands - broke <= 1:
            return True
        else:
            return False

    def position(self, seat, postflop=False):
        """
        Returns how many seats from the button the seat is.
        """
        # Raise an exception if the button is not set

        if postflop:
            seats = self._table.get_players(hascards=True)
        else:
            seats = self._table.get_players()

        return len(seats) - seats.index(seat) - 1

    def betting_round(self):
        """
        Run through a round of betting. Returns a victor if it exists.
        """
        print(self)
        br = betting.BettingRound(self)

        for p in br:
            o = br.player_decision(p)
            br.process_option(o)
            act_str = br.action_string(o)
            print(betting.spacing(br.level()) + act_str)

            # Log every action
            self.hh.log(act_str)

        print(self.show_pot())           # Display pot

    def found_winner(self):
        victor = self.one_left()
        if victor is None:
            self.next_street()
            return False
        else:
            # One player left, award them the pot!
            oneleft = 'Only one player left!'.rjust(70)
            print(colors.color(oneleft, 'LIGHTBLUE'))

            awardtext = self.award_pot(victor, self.pot)
            self.log(awardtext)
            return True

    def discard(self, seat, c):
        """
        Takes the card from the seat's hand and transfers it to the muck. Returns True if the
        operation was successful, False if it didn't.
        """
        self.muck.append(seat.hand.discard(c))

    def log(self, txt, echo=True, decorate=False):
        if decorate:
            txt = self.decorate(txt)
        if echo:
            print(txt)
        self.hh.log(txt)

    def decorate(self, text):
        return '\n~~/) ' + text + ' (\~~'
        # /)(\ (\/)
        #  self.text += '~~(\ ' + text + ' /)~~'
