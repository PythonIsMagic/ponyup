import unittest
import betting
import pokerhands
import testtools


class TestBetting(unittest.TestCase):
    """
    Setup a session and round, with a table filled with 6 players.
    Default level is $2/$4.
    """
    def setUp(self, level=2, players=6, street=1):
        g = testtools.draw5_session(level, players)
        g._table.move_button()
        self.assertEqual(g._table.TOKENS['D'], 0)  # verify the button is 0
        self.r = g.new_round()

        for i in range(street - 1):  # Adjust which street to test.
            self.r.next_street()

        self.r.post_blinds()
        self.r.deal_cards(5)
        self.br = betting.BettingRound(self.r)

    def setUp_shorty(self, shortstack, level=2, players=6, street=1):
        g = testtools.draw5_session(level, players)
        # Sets seat 1(we'll use as the SB) as the short stack amount for easy testing.
        g._table.seats[1].chips = shortstack
        g._table.move_button()
        self.assertEqual(g._table.TOKENS['D'], 0)  # verify the button is 0
        self.r = g.new_round()

        for i in range(street - 1):  # Adjust which street to test.
            self.r.next_street()
        self.r.post_blinds()
        self.r.deal_cards(2)
        self.br = betting.BettingRound(self.r)

    def setUp_studGame(self, level=2, players=6, street=1):
        """
        Setup a 5 card stud game for testing.
        """
        g = testtools.stud5_session(level, players)
        self.r = g.new_round()

        for i in range(street - 1):  # Adjust which street to test.
            self.r.next_street()

        self.r.post_antes()
        testtools.deal_5stud_test_hands(self.r._table)
        self.br = betting.BettingRound(self.r)

    """
    Tests for __iter__()
    """
    # 6 player table: BTN=0, SB=1, BB=2
    def test_iter_1stplayer_returnsSeat3(self):
        player = next(self.br)
        expected = 3
        result = self.r._table.get_index(player)
        self.assertEqual(expected, result)

    # 6 player table: BTN=0, SB=1, BB=2
    def test_play_2ndplayer_returnsSeat4(self):
        next(self.br)
        player = next(self.br)
        expected = 4
        result = self.r._table.get_index(player)
        self.assertEqual(expected, result)

    def test_play_3rdplayer_returnsSeat5(self):
        next(self.br)
        next(self.br)
        player = next(self.br)
        expected = 5
        result = self.r._table.get_index(player)
        self.assertEqual(expected, result)

    """
    Tests for player_decision(p)
    """
    # This module kind of depends on the strategy, but we can probably rely on the fact that
    # they will fold/check absolute trash and raise incredibly strong hands(ie: royal flush).
    # We'll assume that the street is 1 and the betlevel is 1.

    # If a player is allin, return the Allin option
    def test_playerdecision_allin_returnsAllinOption(self):
        self.setUp(players=2)
        bettor = self.br.get_bettor()
        bettor.bet(bettor.chips)
        expected = "ALLIN"
        result = self.br.player_decision(bettor).name
        self.assertEqual(expected, result)

    # Holds a royal flush, raises.
    def test_playerdecision_royalflush_returnsRaise(self):
        self.setUp(players=2)
        bettor = self.br.get_bettor()
        bettor._hand.cards = pokerhands.make('royalflush')
        expected = "RAISE"
        result = self.br.player_decision(bettor).name
        self.assertEqual(expected, result)

    # Holds junk hand, checks the BB.
    def test_playerdecision_junk_returnsCheck(self):
        self.setUp(players=2)
        next(self.br)  # SB
        next(self.br)  # BB
        bettor = self.br.get_bettor()
        bettor._hand.cards = pokerhands.make('junk')
        expected = "CHECK"
        result = self.br.player_decision(bettor).name
        self.assertEqual(expected, result)

    # If they don't have cards - raise an Exception!
    def test_playerdecision_nocards_raiseException(self):
        self.setUp(players=2)
        bettor = self.br.get_bettor()
        bettor._hand.cards = None

        self.assertRaises(Exception, self.br.player_decision, bettor)

    """
    Tests for process_option(option)
    """
    # CHECK - Players chips stay the same
    def test_processoption_CHECK_playerchips_staysame(self):
        self.setUp(players=2, street=2)
        bettor = self.br.get_bettor()
        expected = bettor.chips
        self.br.process_option(betting.CHECK)

        result = bettor.chips
        self.assertEqual(expected, result)

    # CHECK - bet level is same
    def test_processoption_CHECK_bet_stayssame(self):
        self.setUp(players=2, street=2)
        expected = self.br.bet
        self.br.process_option(betting.CHECK)

        result = self.br.bet
        self.assertEqual(expected, result)

    # FOLD - player doesn't have cards
    def test_processoption_FOLD_playerhasnocards(self):
        self.setUp(players=2, street=2)
        bettor = self.br.get_bettor()
        self.assertTrue(bettor.has_cards())
        self.br.process_option(betting.FOLD)
        self.assertFalse(bettor.has_cards())

    # FOLD - Players chips stay the same
    def test_processoption_FOLD_playerchips_staysame(self):
        self.setUp(players=2, street=2)
        bettor = self.br.get_bettor()
        expected = bettor.chips
        self.br.process_option(betting.FOLD)

        result = bettor.chips
        self.assertEqual(expected, result)

    # FOLD - Bet stays the same
    def test_processoption_FOLD_bet_staysame(self):
        self.setUp(players=2, street=2)
        expected = self.br.bet
        self.br.process_option(betting.FOLD)

        result = self.br.bet
        self.assertEqual(expected, result)

    # BET - full bet, bet amount equals the bet size.
    def test_processoption_BET_fullbet_equalsbetsize(self):
        self.setUp(players=2, street=2)
        self.br.process_option(betting.Action('BET', cost=self.br.betsize))
        expected = self.br.betsize
        result = self.br.bet
        self.assertEqual(expected, result)

    # BET - Partial allin bet. Bet equals the allin amount.
    def test_processoption_BET_partialbet_equalsAllin(self):
        self.setUp_shorty(shortstack=3, street=2)
        self.assertTrue(self.br.bettor == 1)
        stack = self.br.get_bettor().chips
        self.br.process_option(betting.Action('BET', stack))
        result = self.br.bet
        self.assertEqual(stack, result)

    # BET - Cannot bet more than betsize, if betlevel = 0
    def test_processoption_BET_exceedsopenamount_raiseException(self):
        self.setUp_shorty(shortstack=8, street=2)
        self.assertTrue(self.br.bettor == 1)
        stack = self.br.get_bettor().chips
        action = betting.Action('BET', stack)
        self.assertRaises(Exception, self.br.process_option, action)

    # BET - Players chips are diminished by the bet amount
    def test_processoption_BET_playerchips_decreasebybetsize(self):
        self.setUp(players=2, street=2)
        p_chips = self.br.get_bettor().chips
        self.br.process_option(betting.Action('BET', cost=self.br.betsize))
        expected = self.br.betsize
        result = p_chips - self.br.get_bettor().chips
        self.assertEqual(expected, result)

    # If seat 1 makes a BET, closer resets to 0.
    def test_processoption_BET_1resetsCloserTo0(self):
        self.setUp(players=6, street=2)
        # Verify bettor position
        self.assertTrue(self.br.bettor == 1)
        self.br.process_option(betting.Action('BET', cost=self.br.betsize))
        expected = 0
        result = self.br.closer
        self.assertEqual(expected, result)

    # If seat 2 makes a BET, closer resets to 1.
    def test_processoption_BET_2resetsCloserTo1(self):
        self.setUp(players=6, street=2)
        # Verify bettor position
        self.br.bettor = 2
        self.br.process_option(betting.Action('BET', cost=self.br.betsize))
        expected = 1
        result = self.br.closer
        self.assertEqual(expected, result)

    # If seat 2 makes a partial BET, closer resets to 1.
    def test_processoption_BET_partial_2resetsCloserTo1(self):
        self.setUp(players=6, street=2)
        bet = 1
        self.br.bettor = 2
        self.br.process_option(betting.Action('BET', bet))
        expected = 1
        result = self.br.closer
        self.assertEqual(expected, result)

    # RAISE - Full raise: bet amount raised by one betsize
    # Seat 3 bets, seat 4 raises.
    def test_processoption_RAISE_full_equals2betsize(self):
        self.setUp(players=6, street=2)
        bet = 4
        next(self.br)  # Seat 3
        self.br.process_option(betting.Action('BET', bet))
        next(self.br)  # Seat 4
        self.br.process_option(betting.Action('RAISE', bet * 2))
        expected = bet * 2
        result = self.br.bet
        self.assertEqual(expected, result)

    def test_processoption_RAISE_3bet_equals3betsize(self):
        self.setUp(players=6, street=2)
        bet = 4
        next(self.br)  # Seat 3
        self.br.process_option(betting.Action('BET', bet))
        next(self.br)  # Seat 4
        self.br.process_option(betting.Action('RAISE', bet * 2))
        next(self.br)  # Seat 5
        self.br.process_option(betting.Action('RAISE', bet * 3))
        expected = bet * 3
        result = self.br.bet
        self.assertEqual(expected, result)

    # Seat 3 bets, seat 4 raises. Closer is 3.
    def test_processoption_RAISE_resetsCloser(self):
        self.setUp(players=6, street=2)
        bet = 4
        next(self.br)  # Seat 3
        self.br.process_option(betting.Action('BET', bet))
        next(self.br)  # Seat 4
        self.br.process_option(betting.Action('RAISE', bet * 2))
        expected = self.br.closer
        result = self.br.closer
        self.assertEqual(expected, result)

    def test_processoption_RAISE_partial(self):
        self.setUp(players=6, street=2)
        bet = 4
        next(self.br)  # Seat 3
        self.br.process_option(betting.Action('BET', bet))
        next(self.br)  # Seat 4
        self.br.process_option(betting.Action('RAISE', bet * 2))
        expected = self.br.closer
        result = self.br.closer
        self.assertEqual(expected, result)

    # COMPLETE - Players chips are diminished by the bet amount

    """
    Tests for get_options(cost)
    """
    # These tests are all $2/$4(blinds $1/$2). Assume full stacks for both players.
    # HU Preflop: SB can FOLD, CALL $1, RAISE $3
    def test_getoptions_HU_preflop_SB_FOLDCALLRAISE(self):
        self.setUp(players=2, street=1)
        p = next(self.br)  # Seat 0
        expected = ['c', 'f', 'r']
        options = self.br.get_options(p)
        result = sorted(list(options.keys()))
        self.assertEqual(expected, result)
        # Verify that the SB's cost to raise reflects the blind posted
        self.assertEqual(options['r'].cost, 3)

    # Helper method: HU situation where SB completes vs BB
    def sb_completes(self):
        self.setUp(players=2, street=1)
        next(self.br)  # Seat 0
        self.br.process_option(betting.Action('CALL', 1))
        next(self.br)  # Seat 1

    # Helper method: HU situation where SB raises vs BB
    def sb_raises(self):
        self.setUp(players=2, street=1)
        next(self.br)  # Seat 0
        self.br.process_option(betting.Action('RAISE', 3))
        next(self.br)  # Seat 1

    # HU Preflop: BB can CHECK, RAISE $2 (when SB completes)
    def test_getoptions_HU_BBpreflop_SBcompletes_CHECKRAISE(self):
        self.sb_completes()
        p = self.br.get_bettor()
        expected = ['c', 'r']
        options = self.br.get_options(p)
        result = sorted(list(options.keys()))
        self.assertEqual(expected, result)
        # Verify that the SB's cost to raise reflects the blind posted
        self.assertEqual(options['r'].cost, 2)

    # HU Preflop: BB can FOLD, CALL $2, RAISE $4 (when SB raises)
    def test_getoptions_HU_BBpreflop_SBraises_CALLFOLDRAISE(self):
        self.sb_raises()
        p = self.br.get_bettor()
        expected = ['c', 'f', 'r']
        options = self.br.get_options(p)
        result = sorted(list(options.keys()))
        self.assertEqual(expected, result)
        # Verify that the SB's cost to raise reflects the blind posted
        self.assertEqual(options['r'].cost, 4)

    # HU Preflop: SB can FOLD, CALL $2, RAISE $4 (when BB 3-bets)
    def test_getoptions_HU_SBpreflop_BB3bets_CALLFOLDRAISE(self):
        self.sb_raises()
        self.br.process_option(betting.Action('RAISE', 4))  # BB reraises
        next(self.br)  # Seat 0
        p = self.br.get_bettor()
        expected = ['c', 'f', 'r']
        options = self.br.get_options(p)
        result = sorted(list(options.keys()))
        self.assertEqual(expected, result)

    # HU Preflop: BB can FOLD, CALL $2 (when SB 4-bets - and caps)
    def test_getoptions_HU_BBpreflop_SB4bets_CALLFOLD(self):
        self.sb_raises()
        self.br.process_option(betting.Action('RAISE', 4))  # BB reraises
        next(self.br)  # Seat 0
        self.br.process_option(betting.Action('RAISE', 4))  # SB 4-bet caps
        next(self.br)  # Seat 1
        p = self.br.get_bettor()
        expected = ['c', 'f']
        options = self.br.get_options(p)
        result = sorted(list(options.keys()))
        self.assertEqual(expected, result)

    # HU Postflop: SB can CHECK or BET $4
    def test_getoptions_HU_SBpost_CHECKBET(self):
        self.setUp(players=2, street=2)
        p = self.br.get_bettor()
        expected = ['b', 'c']
        options = self.br.get_options(p)
        result = sorted(list(options.keys()))
        self.assertEqual(expected, result)

    # HU Postflop: BB can FOLD, CALL $2, RAISE $4 (when SB bets)
    def test_getoptions_HU_BBpost_SBbets_CALLFOLDRAISE(self):
        self.setUp(players=2, street=2)
        next(self.br)  # Seat 1
        self.br.process_option(betting.Action('BET', 4))  # SB 4-bet caps
        p = next(self.br)  # Seat 0
        expected = ['c', 'f', 'r']

        options = self.br.get_options(p)
        result = sorted(list(options.keys()))
        self.assertEqual(expected, result)

    # Tests for allins and partial bets and raises.
    # HU Preflop: SB can FOLD, CALL $1, RAISE $3
    def test_getoptions_allinBB_ALLIN(self):
        self.setUp_shorty(players=2, shortstack=1, street=1)
        next(self.br)
        self.br.process_option(betting.Action('CALL', 1))
        p = next(self.br)
        self.assertEqual(self.br.bettor, 1)
        expected = ['a']
        options = self.br.get_options(p)
        result = sorted(list(options.keys()))
        self.assertEqual(expected, result)

    # SB is shorty, but only has $2.50, not enough for a real raise.
    # SB can only BET, not RAISE
    def test_getoptions_3max_shortSB_cannotRaise(self):
        self.setUp_shorty(players=3, shortstack=2.50, street=1)
        next(self.br)  # Button seat 0
        self.br.process_option(betting.Action('CALL', 2))
        p = next(self.br)  # SB Seat 1
        self.assertEqual(self.br.bettor, 1)
        expected = ['b', 'c', 'f']
        options = self.br.get_options(p)
        result = sorted(list(options.keys()))
        self.assertEqual(expected, result)
        # Should cost the SB exactly 1.50.
        self.assertEqual(options['b'].cost, 1.50)

    # SB is shorty, but only has $3.50, just enough for a real raise.
    def test_getoptions_3max_shortSB_CALLFOLDRAISE(self):
        self.setUp_shorty(players=3, shortstack=3.50, street=1)
        next(self.br)  # Button seat 0
        self.br.process_option(betting.Action('CALL', 2))
        p = next(self.br)  # SB Seat 1
        self.assertEqual(self.br.bettor, 1)
        expected = ['c', 'f', 'r']
        options = self.br.get_options(p)
        result = sorted(list(options.keys()))
        self.assertEqual(expected, result)
        # Should cost the SB exactly 2.50.
        self.assertEqual(options['r'].cost, 2.50)

    # SB is shorty, doesn't have enough for a real raise.
    # Players behind cannot reraise.
    def test_getoptions_3max_shortSB_BBcannotRaise(self):
        self.setUp_shorty(players=3, shortstack=2.50, street=1)
        next(self.br)  # Button seat 0
        self.br.process_option(betting.Action('CALL', 2))
        p = next(self.br)  # SB Seat 1
        self.br.process_option(betting.Action('BET', 1.50))
        p = next(self.br)  # SB Seat 2
        self.assertEqual(self.br.bettor, 2)
        self.assertEqual(self.br.bet, 2.5)

        expected = ['c', 'f', 'r']
        options = self.br.get_options(p)
        result = sorted(list(options.keys()))
        self.assertEqual(expected, result)
        # Should cost the BB $2 to raise
        self.assertEqual(options['r'].cost, 2)

    """
    Tests for action_string(action)
    """
    # Bet
    # Raise
    # Call
    # Fold
    # Allin

    """
    Tests for invested(player)
    """
    # Player bet 100 during the round.
    def test_invested_playerbet100_returns100(self):
        self.setUp(players=2)
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
        expected = 2
        result = self.br.cost(self.br.get_bettor())
        self.assertEqual(expected, result)

    # Street 1: Bet = 2. Bettor is SB, put in 1. Cost = 1.
    def test_cost_SB_predraw_complete_costs1(self):
        self.setUp(players=2)
        expected = 1
        result = self.br.cost(self.br.get_bettor())
        self.assertEqual(expected, result)

    # Street 2: Bet = 2. Bettor is BB, Cost = 0.
    def test_cost_BB_openbetting_costs0(self):
        self.setUp(players=2, street=2)
        expected = 0
        result = self.br.cost(self.br.get_bettor())
        self.assertEqual(expected, result)

    """
    Tests for done()
    """
    def test_done_2playersacted_returnsTrue(self):
        self.setUp(players=2)
        expected = True
        self.br.next_bettor()  # 0 -> 1
        result = self.br.done()
        self.assertEqual(expected, result)

    def test_done_BBnotacted_returnsFalse(self):
        self.setUp(players=2)
        expected = False
        result = self.br.done()
        self.assertEqual(expected, result)

    """
    Tests for set_bettor_and_closer()
    """
    # 6 players. Predraw. BTN=0, SB=1, BB=2. closer=2, bettor=3
    def test_setbettors_w_blinds_6plyr_predraw(self):
        closer, bettor = 2, 3
        self.assertEqual(closer, self.br.closer)
        self.assertEqual(bettor, self.br.bettor)

    # 6 players. Postdraw. BTN=0, SB=1, BB=2. closer=0, bettor=1
    def test_setbettors_w_blinds_6plyr_postdraw(self):
        self.setUp(players=6, street=2)
        closer, bettor = 0, 1
        self.assertEqual(closer, self.br.closer)
        self.assertEqual(bettor, self.br.bettor)

    # 2 players. Predraw. BTN/SB=0, BB=1. closer=1, bettor=0
    def test_setbettors_w_blinds_2plyr_predraw(self):
        self.setUp(players=2)
        closer, bettor = 1, 0
        self.assertEqual(closer, self.br.closer)
        self.assertEqual(bettor, self.br.bettor)

    # 2 players. Postdraw. BTN/SB=0, BB=1. closer=0, bettor=1
    def test_setbettors_w_blinds_2plyr_postdraw(self):
        self.setUp(players=2, street=2)
        closer, bettor = 0, 1
        self.assertEqual(closer, self.br.closer)
        self.assertEqual(bettor, self.br.bettor)

    """
    Tests for set_bettors_w_antes()
    """
    def test_setbettorswantes_seat5islow_bettor5_closer4(self):
        self.setUp_studGame()
        closer, bettor = 4, 5
        self.assertEqual(closer, self.br.closer)
        self.assertEqual(bettor, self.br.bettor)

    """
    Tests for set_betsize(self):
    """
    # FiveCardDraw: street 1, BB=2, betsize = 2
    def test_setbetsize_street1_betsize2(self):
        expected = 2
        result = self.br.betsize
        self.assertEqual(expected, result)

    # FiveCardDraw: street 2, BB=2, betsize = 4
    def test_setbetsize_street2_betsize4(self):
        self.setUp(street=2)
        expected = 4
        result = self.br.betsize
        self.assertEqual(expected, result)

    # Stud: level 2, street 1 should be the small bet: 2
    def test_setbetsize_stud_street1_betsize2(self):
        self.setUp_studGame(level=2, street=1)
        expected = 2
        result = self.br.betsize
        self.assertEqual(expected, result)

    # Stud: level 2, street 3 should be the big bet: 2
    def test_setbetsize_stud_street3_betsize4(self):
        self.setUp_studGame(level=2, street=3)
        expected = 4
        result = self.br.betsize
        self.assertEqual(expected, result)

    """
    Tests for current_bet()
    """
    def test_getbet_HU_street1_returns2(self):
        self.setUp(players=2, street=1)
        expected = 2
        result = self.br.get_bet()
        self.assertEqual(expected, result)

    # No bets yet, current bet should be 0
    def test_getbet_HU_street2_returns0(self):
        self.setUp(players=2, street=2)
        expected = 0
        result = self.br.get_bet()
        self.assertEqual(expected, result)

    # Stud: The bringin has posted. The next player needs to pay the current bet.
    # Level 2, the ante is $0.50, and bringin is $1.
    def test_getbet_bringin_returns1(self):
        self.setUp_studGame(level=2)
        self.r.post_bringin()
        expected = 1
        result = self.br.get_bet()
        self.assertEqual(expected, result)

    """
    Tests for get_betlevel
    """
    def test_getbetlevel_0bet_returns0(self):
        self.setUp(players=2, street=2)
        expected = 0
        result = self.br.get_betlevel()
        self.assertEqual(expected, result)

    def test_getbetlevel_preflopBB_returns1(self):
        self.setUp(players=2, street=1)
        expected = 1
        result = self.br.get_betlevel()
        self.assertEqual(expected, result)

    # If bet=10 and betsize=4, betlevel should be 5.
    def test_getbetlevel_bet12_betsize4_returns3(self):
        self.setUp(street=2)
        # 2/4, betsize = 4
        # Current bet should be 0 before this.
        self.assertTrue(self.br.bet == 0)
        self.br.bet += 12
        expected = 3
        result = self.br.get_betlevel()
        self.assertEqual(expected, result)

    def test_getbetlevel_bet10_betsize4_returns2(self):
        self.setUp(street=2)
        # 2/4, betsize = 4
        # Current bet should be 0 before this.
        self.assertTrue(self.br.bet == 0)
        self.br.bet += 10
        expected = 2
        result = self.br.get_betlevel()
        self.assertEqual(expected, result)

    """
    Tests for get_bettor()
    """
    # 6 players, new table. Preflop. BTN=0, SB=1, BB=2. bettor should be 3.
    def test_getbettor_6plyr_predraw_returnsseat3(self):
        bettor = 3
        expected = self.r._table.seats[bettor]
        result = self.br.get_bettor()
        self.assertEqual(expected, result)

    # 6 players, new table. Postdraw. BTN=0, SB=1, BB=2. bettor should be 1.
    def test_getbettor_6plyr_postdraw_returnsseat1(self):
        self.setUp(street=2)
        bettor = 1
        expected = self.r._table.seats[bettor]
        result = self.br.get_bettor()
        self.assertEqual(expected, result)

    # 2 players, new table. Predraw. BTN/SB=0, BB=1. bettor should be 0.
    def test_getbettor_2plyr_predraw_returnsseat0(self):
        self.setUp(players=2)
        bettor = 0
        expected = self.r._table.seats[bettor]
        result = self.br.get_bettor()
        self.assertEqual(expected, result)

    # 2 players, new table. Postdraw. BTN/SB=0, BB=1. bettor should be 1.
    def test_getbettor_2plyr_postdraw_returnsseat1(self):
        self.setUp(players=2, street=2)
        bettor = 1
        expected = self.r._table.seats[bettor]
        result = self.br.get_bettor()
        self.assertEqual(expected, result)

    """
    # Tests for next_bettor()
    """
    # 6 players, street 1: Current bettor=3, next should be 4
    def test_nextbettor_6players_street1_returnsPlayer4(self):
        self.br.next_bettor()
        expected = 4
        result = self.br.bettor
        self.assertEqual(expected, result)

    # 6 players, street 2: Current bettor=1, next should be 2
    def test_nextbettor_6players_street2_returnsPlayer2(self):
        self.setUp(street=2)
        self.br.next_bettor()
        expected = 2
        result = self.br.bettor
        self.assertEqual(expected, result)

    # 2 players, street 1: Current bettor=0, next should be 1
    def test_nextbettor_2players_street1_returnsPlayer1(self):
        self.setUp(players=2)
        self.br.next_bettor()
        expected = 1
        result = self.br.bettor
        self.assertEqual(expected, result)

    # 2 players, street2: Current bettor=1, next should be 0
    def test_nextbettor_2players_street2_returnsPlayer0(self):
        self.setUp(players=2, street=2)
        self.br.next_bettor()
        expected = 0
        result = self.br.bettor
        self.assertEqual(expected, result)

    """
    Tests for get_closer()
    """
    # 6 players, new table. Predraw. BTN=0, SB=1, BB=2. closer should be 2.
    def test_getcloser_6plyr_predraw_returnsseat2(self):
        closer = 2
        expected = self.r._table.seats[closer]
        result = self.br.get_closer()
        self.assertEqual(expected, result)

    # 6 players, new table. Postdraw. BTN=0, SB=1, BB=2. closer should be 0.
    def test_getcloser_6plyr_postdraw_returnsseat0(self):
        self.setUp(street=2)
        closer = 0
        expected = self.r._table.seats[closer]
        result = self.br.get_closer()
        self.assertEqual(expected, result)

    # 2 players, new table. Predraw. BTN/SB=0, BB=1. closer should be 1.
    def test_getcloser_2plyr_predraw_returnsseat1(self):
        self.setUp(players=2)
        closer = 1
        expected = self.r._table.seats[closer]
        result = self.br.get_closer()
        self.assertEqual(expected, result)

    # 2 players, new table. Postdraw. BTN/SB=0, BB=1. closer should be 0.
    def test_getcloser_2plyr_postdraw_returnsseat0(self):
        self.setUp(players=2, street=2)
        closer = 0
        expected = self.r._table.seats[closer]
        result = self.br.get_closer()
        self.assertEqual(expected, result)

    """
    Tests for reopened_closer(self, bettor):
    """
    # Ex: Heads up, seat 0 is bettor, closer = seat 1
    def test_reopenedcloser_HU_seat0reopens_returns1(self):
        self.setUp(players=2, street=1)
        bettor = 0
        expected = 1
        result = self.br.reopened_closer(bettor)
        self.assertEqual(expected, result)

    # Ex: Heads up, seat 1 is current bettor, closer seat 0
    def test_reopenedcloser_HU_seat1reopens_returns0(self):
        self.setUp(players=2, street=1)
        bettor = 0
        expected = 1
        result = self.br.reopened_closer(bettor)
        self.assertEqual(expected, result)

    # Ex: 6max, seat 3 is current bettor, closer seat 2
    def test_reopenedcloser_6max_seat3reopens_returns2(self):
        self.setUp(players=6, street=1)
        bettor = 3
        expected = 2
        result = self.br.reopened_closer(bettor)
        self.assertEqual(expected, result)

    """
    Tests for set_stacks(self):
    """
    # Draw5: Blind posting
    def test_setstacks_predraw_fullstacks(self):
        self.setUp(players=2)
        expected = {'bob0': 1000, 'bob1': 1000}
        result = self.br.stacks
        self.assertEqual(expected, result)

    def test_setstacks_postdraw_stacksminusblinds(self):
        self.setUp(players=2, street=2)
        expected = {'bob0': 999, 'bob1': 998}
        result = self.br.stacks
        self.assertEqual(expected, result)

    # Stud5: Ante posting
    def test_setstacks_stud_street1_samestacks(self):
        self.setUp_studGame(players=2, level=4, street=1)
        expected = {'bob0': 1000, 'bob1': 1000}
        result = self.br.stacks
        self.assertEqual(expected, result)

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
    def test_calcodds_pot10_bet5_returns2(self):
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
