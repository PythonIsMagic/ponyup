import unittest
import session_factory


class TestSessions(unittest.TestCase):

    """
    Tests for clear_broke_players()
    """
    def test_clearbrokeplayers(self):
        s = session_factory.factory(seats=6, game='FIVE CARD DRAW', level=1)
        p = s._table.seats[0]
        p.stack = 0
        expected = []
        s.clear_broke_players()
        result = s._table.get_broke_players()
        self.assertEqual(expected, result)
