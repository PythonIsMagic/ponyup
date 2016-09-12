import unittest
import stacks
import table_factory
import testtools


class TestStacks(unittest.TestCase):
    def setUp(self, seats=6):
        self.t = table_factory.SteppedStackTable(seats)
        testtools.deal_random_cards(self.t, 1)

    """
    Tests for test_largest(table):
    """
    def test_largest_6players_returns600(self):
        self.setUp(seats=6)
        expected = 600
        result = stacks.largest(self.t)
        self.assertEqual(expected, result)

    """
    Tests for test_smallest(table):
    """
    def test_smallest_6players_returns100(self):
        expected = 100
        result = stacks.smallest(self.t)
        self.assertEqual(expected, result)

    """
    Tests for test_average(table):
    """
    def test_average_6players_returns350(self):
        expected = 350
        result = stacks.average(self.t)
        self.assertEqual(expected, result)

    """
    Tests for test_effective(table):
    """
    def test_effective_6players_returns350(self):
        self.setUp(seats=6)
        expected = 350
        result = stacks.effective(self.t)
        self.assertEqual(expected, result)

    def test_effective_2players_returns100(self):
        self.setUp(seats=2)
        expected = 100
        result = stacks.effective(self.t)
        self.assertEqual(expected, result)

    """
    Tests for stacklist(table)
    """
    def test_stacklist_6players_returns4stacks(self):
        self.setUp(seats=6)
        expected = [100, 200, 300, 400, 500, 600]
        result = stacks.stacklist(self.t)
        self.assertEqual(expected, result)

