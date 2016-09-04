import unittest
import betting
import testtools


class TestBetting(unittest.TestCase):
    """
    Setup a session and round, with a table filled with 6 players.
    """
    def setUp(self, level=1, players=6):
        g = testtools.draw5_session(level, players)
        g._table.move_button()
        self.assertEqual(g._table.TOKENS['D'], 0)  # verify the button is 0
        self.r = g.new_round()
        self.r.deal_cards(5)
        self.r.post_blinds()

    """
    Tests for play()
    """

    """
    Tests for player_decision(p)
    """
    # This module kind of depends on the strategy, but we can probably rely on the fact that
    # they will fold/check absolute trash and raise incredibly strong hands(ie: royal flush).
    # We'll assume that the street is 1 and the betlevel is 1.

    # If a player is allin, return the Allin option
    def test_playerdecision_allin_returnsAllinOption(self):
        self.setUp(players=2)
        self.br = betting.BettingRound(self.r)
        bettor = self.br.get_bettor()
        bettor.bet(bettor.chips)
        expected = "ALLIN"
        result = self.br.player_decision(bettor).name
        self.assertEqual(expected, result)

    # Holds a royal flush, raises.
    # Holds junk hand, checks the BB.

    """
    Tests for process_option(option)
    """
    # CHECK - bet level is same
    # CHECK - Players chips stay the same
    # FOLD - player doesn't have cards
    # FOLD - Players chips stay the same
    # BET - bet level is raised by one
    # BET - Players chips are diminished by the bet amount
    # RAISE - bet level is raised by one
    # RAISE - Players chips are diminished by the raiseamount
    # CHECK - bet level is same
    # COMPLETE - Players chips are diminished by the bet amount

    """
    Tests for get_options(cost)
    """

    """
    Tests for set_bettor_and_closer()
    """
    # 6 players. Predraw. BTN=0, SB=1, BB=2. closer=2, bettor=3
    def test_setbettorandcloser_6plyr_predraw(self):
        closer, bettor = 2, 3
        self.br = betting.BettingRound(self.r)
        self.assertEqual(closer, self.br.closer)
        self.assertEqual(bettor, self.br.bettor)

    # 6 players. Postdraw. BTN=0, SB=1, BB=2. closer=0, bettor=1
    def test_setbettorandcloser_6plyr_postdraw(self):
        closer, bettor = 0, 1
        self.r.next_street()
        self.br = betting.BettingRound(self.r)
        self.assertEqual(closer, self.br.closer)
        self.assertEqual(bettor, self.br.bettor)

    # 2 players. Predraw. BTN/SB=0, BB=1. closer=1, bettor=0
    def test_setbettorandcloser_2plyr_predraw(self):
        self.setUp(players=2)
        closer, bettor = 1, 0
        self.br = betting.BettingRound(self.r)
        self.assertEqual(closer, self.br.closer)
        self.assertEqual(bettor, self.br.bettor)

    # 2 players. Postdraw. BTN/SB=0, BB=1. closer=0, bettor=1
    def test_setbettorandcloser_2plyr_postdraw(self):
        self.setUp(players=2)
        closer, bettor = 0, 1
        self.r.next_street()
        self.br = betting.BettingRound(self.r)
        self.assertEqual(closer, self.br.closer)
        self.assertEqual(bettor, self.br.bettor)

    """
    Tests for set_level
    """

    """
    Tests for set_betsize(self):
    """
    # FiveCardDraw: street 1, BB=2, betsize = 2
    def test_setbetsize_street1_betsize2(self):
        self.setUp()
        self.br = betting.BettingRound(self.r)
        expected = 2
        result = self.br.betsize
        self.assertEqual(expected, result)

    # FiveCardDraw: street 2, BB=2, betsize = 4
    def test_setbetsize_street2_betsize4(self):
        self.setUp()
        self.r.next_street()
        self.br = betting.BettingRound(self.r)
        expected = 4
        result = self.br.betsize
        self.assertEqual(expected, result)

    """
    Tests for set_stacks(self):
    """
    def test_setstacks_predraw_fullstacks(self):
        self.setUp(players=2)
        self.br = betting.BettingRound(self.r)
        expected = {'bob0': 1000, 'bob1': 1000}
        result = self.br.stacks
        self.assertEqual(expected, result)

    def test_setstacks_postdraw_stacksminusblinds(self):
        self.setUp(players=2)
        self.r.next_street()
        self.br = betting.BettingRound(self.r)
        expected = {'bob0': 999, 'bob1': 998}
        result = self.br.stacks
        self.assertEqual(expected, result)

    """
    Tests for get_bettor()
    """
    # 6 players, new table. Preflop. BTN=0, SB=1, BB=2. bettor should be 3.
    def test_getbettor_6plyr_predraw_returnsseat3(self):
        bettor = 3
        self.br = betting.BettingRound(self.r)
        expected = self.r._table.seats[bettor]
        result = self.br.get_bettor()
        self.assertEqual(expected, result)

    # 6 players, new table. Postdraw. BTN=0, SB=1, BB=2. bettor should be 1.
    def test_getbettor_6plyr_postdraw_returnsseat1(self):
        bettor = 1
        self.r.next_street()
        self.br = betting.BettingRound(self.r)
        expected = self.r._table.seats[bettor]
        result = self.br.get_bettor()
        self.assertEqual(expected, result)

    # 2 players, new table. Predraw. BTN/SB=0, BB=1. bettor should be 0.
    def test_getbettor_2plyr_predraw_returnsseat0(self):
        self.setUp(players=2)
        bettor = 0
        self.br = betting.BettingRound(self.r)
        expected = self.r._table.seats[bettor]
        result = self.br.get_bettor()
        self.assertEqual(expected, result)

    # 2 players, new table. Postdraw. BTN/SB=0, BB=1. bettor should be 1.
    def test_getbettor_2plyr_postdraw_returnsseat1(self):
        self.setUp(players=2)
        bettor = 1
        self.r.next_street()
        self.br = betting.BettingRound(self.r)
        expected = self.r._table.seats[bettor]
        result = self.br.get_bettor()
        self.assertEqual(expected, result)

    """
    Tests for get_closer()
    """
    # 6 players, new table. Predraw. BTN=0, SB=1, BB=2. closer should be 2.
    def test_getcloser_6plyr_predraw_returnsseat2(self):
        closer = 2
        self.br = betting.BettingRound(self.r)
        expected = self.r._table.seats[closer]
        result = self.br.get_closer()
        self.assertEqual(expected, result)

    # 6 players, new table. Postdraw. BTN=0, SB=1, BB=2. closer should be 0.
    def test_getcloser_6plyr_postdraw_returnsseat0(self):
        closer = 0
        self.r.next_street()
        self.br = betting.BettingRound(self.r)
        expected = self.r._table.seats[closer]
        result = self.br.get_closer()
        self.assertEqual(expected, result)

    # 2 players, new table. Predraw. BTN/SB=0, BB=1. closer should be 1.
    def test_getcloser_2plyr_predraw_returnsseat1(self):
        self.setUp(players=2)
        closer = 1
        self.br = betting.BettingRound(self.r)
        expected = self.r._table.seats[closer]
        result = self.br.get_closer()
        self.assertEqual(expected, result)

    # 2 players, new table. Postdraw. BTN/SB=0, BB=1. closer should be 0.
    def test_getcloser_2plyr_postdraw_returnsseat0(self):
        self.setUp(players=2)
        closer = 0
        self.r.next_street()
        self.br = betting.BettingRound(self.r)
        expected = self.r._table.seats[closer]
        result = self.br.get_closer()
        self.assertEqual(expected, result)

    """
    Tests for invested(player)
    """
    # Player bet 100 during the round.
    def test_invested_playerbet100_returns100(self):
        self.setUp(players=2)
        self.br = betting.BettingRound(self.r)
        bettor = self.br.get_bettor()
        bettor.bet(99)
        expected = 100
        result = self.br.invested(bettor)
        self.assertEqual(expected, result)

    """
    Tests for cost(self, amt_invested)
    """
    # Street 1: Bet = 2. Player hasn't put any money in. Cost = 2.
    def test_cost_UTG_predraw_callfor2_costs2(self):
        self.br = betting.BettingRound(self.r)
        invested = self.br.invested(self.br.get_bettor())
        expected = 2
        result = self.br.cost(invested)
        self.assertEqual(expected, result)

    # Street 1: Bet = 2. Bettor is SB, put in 1. Cost = 1.
    def test_cost_SB_predraw_complete_costs1(self):
        self.setUp(players=2)
        self.br = betting.BettingRound(self.r)
        invested = self.br.invested(self.br.get_bettor())
        expected = 1
        result = self.br.cost(invested)
        self.assertEqual(expected, result)

    # Street 2: Bet = 2. Bettor is BB, Cost = 0.
    def test_cost_BB_openbetting_costs0(self):
        self.setUp(players=2)
        self.r.next_street()
        self.br = betting.BettingRound(self.r)
        invested = self.br.invested(self.br.get_bettor())
        expected = 0
        result = self.br.cost(invested)
        self.assertEqual(expected, result)

    """
    # Tests for next_bettor()
    """
    # 6 players, street 1: Current bettor=3, next should be 4
    def test_nextbettor_6players_street1_returnsPlayer4(self):
        self.br = betting.BettingRound(self.r)
        self.br.next_bettor()
        expected = 4
        result = self.br.bettor
        self.assertEqual(expected, result)

    # 6 players, street 2: Current bettor=1, next should be 2
    def test_nextbettor_6players_street2_returnsPlayer2(self):
        self.r.next_street()
        self.br = betting.BettingRound(self.r)
        self.br.next_bettor()
        expected = 2
        result = self.br.bettor
        self.assertEqual(expected, result)

    # 2 players, street 1: Current bettor=0, next should be 1
    def test_nextbettor_2players_street1_returnsPlayer1(self):
        self.setUp(players=2)
        self.br = betting.BettingRound(self.r)
        self.br.next_bettor()
        expected = 1
        result = self.br.bettor
        self.assertEqual(expected, result)

    # 2 players, street2: Current bettor=1, next should be 0
    def test_nextbettor_2players_street2_returnsPlayer0(self):
        self.setUp(players=2)
        self.r.next_street()
        self.br = betting.BettingRound(self.r)
        self.br.next_bettor()
        expected = 0
        result = self.br.bettor
        self.assertEqual(expected, result)

    """
    Tests for done()
    """
    def test_done_2playersacted_returnsTrue(self):
        self.setUp(players=2)
        self.br = betting.BettingRound(self.r)
        expected = True
        self.br.next_bettor()  # 0 -> 1
        result = self.br.done()
        self.assertEqual(expected, result)

    def test_done_BBnotacted_returnsFalse(self):
        self.setUp(players=2)
        self.br = betting.BettingRound(self.r)
        expected = False
        result = self.br.done()
        self.assertEqual(expected, result)

    """
    Tests for action_stright(action)
    """
    # Bet
    # Raise
    # Call
    # Fold
    # Allin

################################################################################
    """
    Tests for calc_odds(bet ,pot)
    """
    # bet cannot be negative
    def test_calcodds_negbet_raiseEx(self):
        self.assertRaises(ValueError, betting.calc_odds, -10, 10)

    # pot cannot be negative
    def test_calcodds_negpot_raiseEx(self):
        self.assertRaises(ValueError, betting.calc_odds, 10, -10)

    # bet = 5, pot = 10, we are getting 2-to-1 odds.
    def test_init_0cardspassed_length0(self):
        expected = 2.0
        result = betting.calc_odds(5, 10)
        self.assertEqual(expected, result)

    """
    Tests for menu()
    """

    """
    Tests for spacing()
    """

    """
    Tests for one_left()
    """
    def test_oneleft_allhavecards_returnsNone(self):
        expected = None
        result = betting.one_left(self.r._table)
        self.assertEqual(expected, result)
