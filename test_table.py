import unittest
import card
import deck
import table
import player


class TestTable(unittest.TestCase):
    """
    Setup a table filled with 6 players for testing.
    """
    def setUp(self):
        self.t = make_table(6)

    """
    Tests for __init__ and table construction
    """
    # initialized with invalid seat count(less than 2)
    def test_init_invalidtablesize1_throwException(self):
        self.assertRaises(ValueError, table.Table, '1')

    # initialized with invalid seat count(more than 10)
    def test_init_invalidtablesize11_throwException(self):
        self.assertRaises(ValueError, table.Table, '11')

    # initialized with valid seat count
    def test_init_validtablesize_validSize(self):
        t = table.Table(6)
        expected = 6
        result = len(t)
        self.assertEqual(expected, result)

    """
    Tests for __len__()
    """
    # Also tested in the init and add/remove player tests.
    def test_len_lenOfSetupTable_returns6(self):
        expected = 6
        result = len(self.t)
        self.assertEqual(expected, result)

    """
    Tests for __str__()
    """
    # Test that table displays correctly?
    def test_str_newtable_correctDisplay(self):
        expected = ''
        expected += '#  Tokens Player         Chips     Hand      \n'
        expected += '--------------------------------------------------\n'
        expected += '0         bob0           $1000     \n'
        expected += '1         bob1           $1000     \n'
        expected += '2         bob2           $1000     \n'
        expected += '3         bob3           $1000     \n'
        expected += '4         bob4           $1000     \n'
        expected += '5         bob5           $1000     \n'

        result = str(self.t)
        self.assertEqual(expected, result)

    """
    Tests for __iter__(), __next__() # needed?
    """
    # Test that the table iterates through few players in order, full table
    def test_next_setUpTable_getsseat0(self):
        expected = 'bob0'
        iterator = self.t.__iter__()
        result = str(iterator.__next__())
        self.assertEqual(expected, result)

    # Test that it goes to the next player.
    def test_next2_setUpTable_getsseat1(self):
        expected = 'bob1'
        iterator = self.t.__iter__()
        iterator.__next__()
        result = str(iterator.__next__())
        self.assertEqual(expected, result)

    # Iter should skip over an empty seat
    def test_next_removedseat0_getsseat1(self):
        self.t.remove_player(0)
        expected = 'bob1'
        iterator = self.t.__iter__()
        result = str(iterator.__next__())
        self.assertEqual(expected, result)

    """
    Tests for btn(), move_button()
    """
    # A new table should have the button set to -1
    def test_btn_setUpTable_returnsNeg1(self):
        expected = -1
        result = self.t.btn()
        self.assertEqual(expected, result)

    # New table, moving button once should go from -1 to 0.
    def test_movebutton_setUpTable_returns0(self):
        expected = 0
        self.t.move_button()
        result = self.t.btn()
        self.assertEqual(expected, result)

    # New table(without seat 0), moving button once should go from -1 to 1
    def test_movebutton_seat0removed_returns1(self):
        expected = 1
        self.t.remove_player(0)
        self.t.move_button()
        result = self.t.btn()
        self.assertEqual(expected, result)

    def test_movebutton_fulltableof6(self):
        tablesize = len(self.t)
        # Note: I wanted to use a generator to make the test cases here, but didn't work yet.
        for i in range(tablesize):
            self.check_btn(i)

    def check_btn(self, b):
        self.t.move_button()
        expected = b
        result = self.t.btn()
        self.assertEqual(expected, result)

    # New table: Button at 0, sb should be at 1
    def test_movebutton_setUpTable_SBat1(self):
        expected = 1
        self.t.move_button()
        result = self.t.get_sb()
        self.assertEqual(expected, result)

    # New table(seat 1 removed): Button at 0, sb should be at 2
    def test_movebutton_seat1removed_SBat2(self):
        expected = 2
        self.t.remove_player(1)
        self.t.move_button()
        result = self.t.get_sb()
        self.assertEqual(expected, result)

    # New table: Button at 0, bb should be at 2
    def test_movebutton_setUpTable_BBat2(self):
        self.t.move_button()
        # Confirm btn is at 0
        self.assertEqual(self.t.btn(), 0, "button ain't right")
        expected = 2
        result = self.t.get_bb()
        self.assertEqual(expected, result)

    # New table(seat 2 removed): Button at 0, bb should be at 3
    def test_movebutton_seat2removed_BBat3(self):
        self.t.remove_player(2)
        self.t.move_button()
        # Confirm btn is at 0
        self.assertEqual(self.t.btn(), 0, "button ain't right")
        expected = 3
        result = self.t.get_bb()
        self.assertEqual(expected, result)

    """
    Tests for add_player()
    """
    # Adding 1 player to an empty table, size should be 1.
    def test_addplayer_toEmptyTable_1player(self):
        t = table.Table(6)
        t.add_player(0, player.Player('bob0', 'CPU'))
        expected = 1
        result = len(t.get_players())
        self.assertEqual(expected, result)

    # Adding 1 player to an empty table, contains the added player
    def test_addplayer_toEmptyTable_containsPlayer(self):
        t = table.Table(6)
        p = player.Player('bob0', 'CPU')
        t.add_player(0, p)
        expected = 1
        result = p in t
        self.assertEqual(expected, result)

    # Adding 1 player to an occupied spot,
    def test_addplayer_tooccupiedspot_raiseException(self):
        t = table.Table(6)
        p1 = player.Player('bob0', 'CPU')
        p2 = player.Player('bob1', 'CPU')
        t.add_player(0, p1)
        self.assertRaises(ValueError, t.add_player, 0, p2)

    # Adding a duplicate player to the table, should raise exception.
    def test_addplayer_duplicateplayer_raiseException(self):
        t = table.Table(6)
        p1 = player.Player('bob0', 'CPU')
        p2 = player.Player('bob1', 'CPU')
        p3 = player.Player('bob1', 'CPU')
        t.add_player(0, p1)
        t.add_player(1, p2)
        self.assertRaises(ValueError, t.add_player, 3, p3)

    """
    Tests for indexof
    """
    # Add a player to seat 0, indexof returns 0
    def test_indexof_playerinseat0_returns0(self):
        t = table.Table(6)
        p = player.Player('bob0', 'CPU')
        t.add_player(0, p)
        expected = 0
        result = t.get_index(p)
        self.assertEqual(expected, result)

    # indexof a player not in the table, returns -1
    def test_indexof_nonpresentplayer_returnsNeg1(self):
        t = table.Table(6)
        p = player.Player('bob0', 'CPU')
        p2 = player.Player('bob1', 'CPU')
        t.add_player(0, p)
        expected = -1
        result = t.get_index(p2)
        self.assertEqual(expected, result)

    """
    Tests for remove_player()
    """
    # Remove player 0, table doesn't contain the player at seat 0.
    def test_removeplayer_removeseat0_doesntcontainseat0(self):
        p = player.Player('bob0', 'CPU')
        self.t.remove_player(0)
        expected = False
        result = p in self.t
        self.assertEqual(expected, result)

    # Remove player 0, seat 0 is None
    def test_removeplayer_removeseat0_seat0isNone(self):
        self.t.remove_player(0)
        expected = True
        result = self.t.seats[0] is None
        self.assertEqual(expected, result)

    """
    Tests for get_players()
    """
    # From the setUp table, gets an array size 6.
    def test_getplayers_6players_returnslistsize6(self):
        expected = 6
        result = len(self.t.get_players())
        self.assertEqual(expected, result)

    # From a table of 1, gets an array of size 1.
    def test_getplayers_1player_returnslistsize1(self):
        t = table.Table(6)
        p1 = player.Player('bob0', 'CPU')
        t.add_player(0, p1)
        expected = 1
        result = len(t.get_players())
        self.assertEqual(expected, result)

    # From a table of one, gets the player at the table.
    def test_getplayers_1player_listcontainsplayer(self):
        t = table.Table(6)
        p1 = player.Player('bob0', 'CPU')
        t.add_player(0, p1)
        expected = True
        result = p1 in t
        self.assertEqual(expected, result)

    """
    Tests for valid_bettors()
    """
    # 0 players holding cards, gets an array size 0
    def test_validbettors_0withcards_returns0(self):
        expected = 0
        result = self.t.valid_bettors()
        self.assertEqual(expected, result)

    # 1 players holding cards, gets an array size 1
    def test_validbettors_1withcards_returns1(self):
        expected = 1
        c = card.Card('A', 's')
        self.t.seats[0].add_card(c)
        result = self.t.valid_bettors()
        self.assertEqual(expected, result)

    """
    Tests for next(from_seat)
    """
    # New setUp table, user supplies from_seat out of list index range. Should raise exception.
    def test_next_outofboundsseat100_raiseException(self):
        seat = 100
        self.assertRaises(ValueError, self.t.next, seat)

    # Less than -1 is an error. -1 is the starting point for the button and other tokens.
    def test_next_outofboundsseatneg2_raiseException(self):
        seat = -2
        self.assertRaises(ValueError, self.t.next, seat)

    # New setUp table, from_seat 0, returns 1
    def test_next_setUptable_returnSeat0(self):
        seat = 0
        expected = 1
        result = self.t.next(seat)
        self.assertEqual(expected, result)

    # Empty seat between 0 and 2, returns 1
    def test_next_from0_seat1empty_return2(self):
        seat = 0
        self.t.remove_player(1)
        expected = 2
        result = self.t.next(seat)
        self.assertEqual(expected, result)

    # setUp table, negative step, from_seat 0, returns 5
    def test_next_negativestep_from0_returnSeat5(self):
        seat = 0
        expected = 5
        result = self.t.next(seat, -1)
        self.assertEqual(expected, result)

    # Empty seat between 4 and 0, returns 5
    def test_next_negativestep_seat5empty_from0_returnSeat5(self):
        seat = 0
        self.t.remove_player(5)
        expected = 4
        result = self.t.next(seat, -1)
        self.assertEqual(expected, result)

    # No players, return -1
    def test_next_noplayers_returnsNeg1(self):
        t = table.Table(6)
        seat = 0
        self.assertRaises(Exception, t.next, seat)

    # No players, negative step, return -1
    def test_next_negativestep_noplayers_returnsNeg1(self):
        t = table.Table(6)
        seat = 0
        self.assertRaises(Exception, t.next, seat)

######################################################
# Thorough test of next()

    # Next, 6 players, from 0, returns 1
    def test_next_from0_returns1(self):
        expected = 1
        result = self.t.next(0)
        self.assertEqual(expected, result)

    # Next, 6 players, from 1, returns 2
    def test_next_from1_returns2(self):
        expected = 2
        result = self.t.next(1)
        self.assertEqual(expected, result)

    # Next, 6 players, from 2, returns 3
    def test_next_from2_returns3(self):
        expected = 3
        result = self.t.next(2)
        self.assertEqual(expected, result)

    # Next, 6 players, from 3, returns 4
    def test_next_from3_returns4(self):
        expected = 4
        result = self.t.next(3)
        self.assertEqual(expected, result)

    # Next, 6 players, from 4, returns 5
    def test_next_from4_returns5(self):
        expected = 5
        result = self.t.next(4)
        self.assertEqual(expected, result)

    # Next, 6 players, from 5, returns 0
    def test_next_from5_returns0(self):
        expected = 0
        result = self.t.next(5)
        self.assertEqual(expected, result)

    """
    Tests for next_player_w_cards(from_seat, step=1)
    """
    # 6 seat table, seat 0 has cards - from 0, returns 0
    def test_nextplayerwcards_from0_seat0hascards_return0(self):
        t = table.Table(6)
        c = card.Card('A', 's')
        self.t.seats[0].add_card(c)
        seat = 0
        self.assertRaises(Exception, t.next_player_w_cards, seat)

    # 6 seat table, seat 0 has cards - from 1, returns 0
    def test_nextplayerwcards_from1_seat0hascards_return0(self):
        c = card.Card('A', 's')
        self.t.seats[0].add_card(c)
        expected = 0
        result = self.t.next_player_w_cards(1)
        self.assertEqual(expected, result)

    # 6 seat table, no cards - raise exception
    def test_nextplayerwcards_nocards_return0(self):
        from_seat = 0
        self.assertRaises(Exception, self.t.next_player_w_cards, from_seat)

    # Full table - all w cards. btn at 0. From 0 returns 1.
    def test_nextplayerwcards_fulltable_from0_return1(self):
        # Button should be at -1 for self.t
        self.t.move_button()
        # Button should be at 0 after move.

        # Give everyone cards
        c = card.Card('A', 's')
        for seat in self.t:
            seat.add_card(c)
        from_seat = 0
        expected = 1
        result = self.t.next_player_w_cards(from_seat)
        self.assertEqual(expected, result)

    # Full table - seat 3 has cards. btn at 0. From 0 returns 3.
    def test_nextplayerwcards_seat3hascards_from0_return3(self):
        self.t.move_button()
        c = card.Card('A', 's')
        self.t.seats[3].add_card(c)
        from_seat = 0
        expected = 3
        result = self.t.next_player_w_cards(from_seat)
        self.assertEqual(expected, result)

    # Full table - all w cards. btn at 0. From 0 returns 5. Negative step
    def test_nextplayerwcards_fulltable_negstep_from0_return5(self):
        # Button should be at -1 for self.t
        self.t.move_button()
        # Button should be at 0 after move.

        # Give everyone cards
        c = card.Card('A', 's')
        for seat in self.t:
            seat.add_card(c)
        from_seat = 0
        expected = 5
        result = self.t.next_player_w_cards(from_seat, -1)
        self.assertEqual(expected, result)

    # Full table - seat 3 has cards. btn at 0. negative step. From 0 returns 4.
    def test_nextplayerwcards_seat4hascards_negstep_from0_return4(self):
        self.t.move_button()
        c = card.Card('A', 's')
        self.t.seats[4].add_card(c)
        from_seat = 0
        expected = 4
        result = self.t.next_player_w_cards(from_seat, -1)
        self.assertEqual(expected, result)

    """
    Tests for get_playerdict()
    """
    # No players at table returns empty dict
    def test_getplayerdict_noplayer_returnsDictsize0(self):
        t = table.Table(6)
        expected = 0
        result = len(t.get_playerdict())
        self.assertEqual(expected, result)

    # 1 player at table, returns dict size 1
    def test_getplayerdict_1player_returnsDictsize1(self):
        t = table.Table(6)
        t.add_player(0, player.Player('bob0', 'CPU'))
        expected = 1
        result = len(t.get_playerdict())
        self.assertEqual(expected, result)

    # 6 players returns dict size 6
    def test_getplayerdict_6players_returnsDictsize6(self):
        expected = 6
        result = len(self.t.get_playerdict())
        self.assertEqual(expected, result)

    """
    Tests for randomize_button()
    """

    # Randomize button on table size 2, button is in range 0-1
    def test_randomizebutton_2seats_inrange0to1(self):
        seats = 2
        t = make_table(seats)
        t.randomize_button()
        result = t.btn() >= 0 and t.btn() < seats
        self.assertTrue(result)

    # Randomize button on table size 6, button is in range 0-5

    def test_randomizebutton_6seats_inrange0to5(self):
        seats = 6
        t = make_table(seats)
        t.randomize_button()
        result = t.btn() >= 0 and t.btn() < seats
        self.assertTrue(result)

    # Randomize button on table size 6, button is in range 0-8
    def test_randomizebutton_9seats_inrange0to8(self):
        seats = 9
        t = make_table(seats)
        t.randomize_button()
        result = t.btn() >= 0 and t.btn() < seats
        self.assertTrue(result)

    """
    Tests for get_cardholders()
    """
    # 1 player with cards. Button is -1. Raises Exception
    def test_getcardholders_btnnotset_seat0hascards_raiseException(self):
        c = card.Card('A', 's')
        self.t.seats[0].add_card(c)

        self.assertRaises(Exception, self.t.get_cardholders)

    # 1 player with cards. Button moved to 0. Returns the player
    def test_getcardholders_btn0_seat0hascards_returnsPlayer(self):
        self.t.move_button()
        # Make sure the btn is at 0
        self.assertTrue(self.t.btn() == 0)

        c = card.Card('A', 's')
        self.t.seats[0].add_card(c)
        expected = [self.t.seats[0]]
        result = self.t.get_cardholders()
        self.assertEqual(expected, result)

    # 2 player with cards. Button moved to 0. Returns the player
    # Since it's heads up, the sb/btn(0) should be first in the returned list
    def test_getcardholders_btn0_seat0and1hascards_return0(self):
        seats = 2
        t = make_table(seats)
        t.move_button()
        # Make sure the btn is at 0
        self.assertEqual(t.btn(), 0)
        # Make sure the sb is at 0.
        self.assertEqual(t.get_sb(), 0)

        deal_cards(t)

        expected = t.seats[0]
        result = t.get_cardholders()[0]
        self.assertEqual(expected, result)

    # 2 player with cards. Button moved to 0. Returns the player
    # Since it's heads up, the sb/btn(0) should be first in the returned list
    def test_getcardholders_btn1_seat0and1hascards_return1(self):
        seats = 2
        t = make_table(seats)
        t.move_button()
        t.move_button()
        # Make sure the btn is at 1
        self.assertEqual(t.btn(), 1)
        # Make sure the sb is at 1.
        self.assertEqual(t.get_sb(), 1)
        deal_cards(t)

        expected = t.seats[1]
        result = t.get_cardholders()[0]
        self.assertEqual(expected, result)

    # 6 players with cards, Button at 0. Returns list with seat 1 first.
    def test_getcardholders_6havecards_btn0_seat1first(self):
        self.t.move_button()
        # Make sure the btn is at 0
        self.assertEqual(self.t.btn(), 0)

        deal_cards(self.t)

        expected = self.t.seats[1]
        result = self.t.get_cardholders()[0]
        self.assertEqual(expected, result)

    # 6 players with cards, Button at 5. Returns list with seat 0 first.
    def test_getcardholders_6havecards_btn5_seat0first(self):
        self.t.TOKENS['BTN'] = 4
        self.t.move_button()
        # Make sure the btn is at 0
        self.assertEqual(self.t.btn(), 0)

        deal_cards(self.t)
        expected = self.t.seats[1]
        result = self.t.get_cardholders()[0]
        self.assertEqual(expected, result)

    # 6 players with cards, Button at 0. Returns list that's size 6.
    def test_getcardholders_6havecards_lengthis6(self):
        self.t.move_button()
        deal_cards(self.t)
        expected = 6
        result = len(self.t.get_cardholders())
        self.assertEqual(expected, result)

    """
    Tests for has_cards(s)
    """
    # Seat 0 has cards, should return True
    def test_hascards_playerhascards_returnsTrue(self):
        c = card.Card('A', 's')
        self.t.seats[0].add_card(c)
        expected = True
        result = self.t.has_cards(0)
        self.assertEqual(expected, result)

    # Seat 0 doesn't have cards, should return False
    def test_hascards_playerhasnocards_returnsFalse(self):
        expected = False
        result = self.t.has_cards(0)
        self.assertEqual(expected, result)

    """
    Tests for remove_broke_players()
    """
    # 6 players, all with chips, returns empty list
    def test_removebrokeplayers_6playerswithchips_returnemptylist(self):
        expected = []
        result = self.t.remove_broke()
        self.assertEqual(expected, result)

    # 1 broke player, returns the player in a list
    def test_removebrokeplayers_1brokeplayer_returnsplayer(self):
        p = self.t.seats[0]
        p.chips = 0
        expected = [p]
        result = self.t.remove_broke()
        self.assertEqual(expected, result)

    # 6 players, all broke, table is empty.
    def test_removebrokeplayers_allbroke_returnsallplayers(self):
        for p in self.t:
            p.chips = 0
        expected = self.t.seats[:]
        result = self.t.remove_broke()
        self.assertEqual(expected, result)

    """
    Tests for get_valuelist()
    """
    # No players have cards, returns empty list
    def test_getvaluelist_nocards_emptylist(self):
        self.t.move_button()
        expected = []
        result = self.t.get_valuelist()
        self.assertEqual(expected, result)

    # 1 player with cards, list is 1 long.
    def test_getvaluelist_1hascards_listis1long(self):
        self.t.move_button()
        c = card.Card('A', 's')
        self.t.seats[0].add_card(c)
        expected = 1
        result = len(self.t.get_valuelist())
        self.assertEqual(expected, result)

    # 6 players with cards, list is 6 long.
    def test_getvaluelist_6havecards_listis6long(self):
        self.t.move_button()
        deal_cards(self.t)
        expected = 6
        result = len(self.t.get_valuelist())
        self.assertEqual(expected, result)

##################################################
# Helper Functions


def make_table(seats):
    # Populate a Table of the specified # of seats with players.
    t = table.Table(seats)
    for i in range(seats):
        t.add_player(i, player.Player('bob{}'.format(i), 'CPU'))

    for p in t:
        p.add_chips(1000)

    return t


def deal_cards(tbl):
    d = deck.Deck()
    for seat in tbl:
        seat.add_card(d.deal())
