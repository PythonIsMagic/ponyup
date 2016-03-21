import unittest
import deck
import card


class TestDeck(unittest.TestCase):
    """
    Tests for __init__ and Deck construction.
    """
    def test_init_nocards_stddeckwithsize52(self):
        d = deck.Deck()
        expected = 52
        result = len(d)
        self.assertEqual(expected, result)

    def test_init_2cards_haslen2(self):
        cards = []
        cards.append(card.Card('A', 's'))
        cards.append(card.Card('K', 's'))
        d = deck.Deck(cards)
        expected = 2
        result = len(d)
        self.assertEqual(expected, result)

    """
    Tests for shuffle()
    """

    """
    Tests for sort()
    """
    def test_sort_2cards_deuceisfirst(self):
        cards = []
        cards.append(card.Card('A', 's'))
        cards.append(card.Card('2', 's'))
        d = deck.Deck(cards)
        d.sort()
        expected = '2'
        result = d.cards[0].rank
        self.assertEqual(expected, result)

    """
    Tests for deal()
    """
    def test_deal_stddeck_sizeIs51(self):
        d = deck.Deck()
        d.deal()
        expected = 51
        result = len(d)
        self.assertEqual(expected, result)

    """
    Tests for remove(card)
    """
    def test_remove_removeAs_sizeIs51(self):
        d = deck.Deck()
        c = card.Card('A', 's')
        d.remove(c)
        expected = 51
        result = len(d)
        self.assertEqual(expected, result)

    """
    Tests for contains(card)
    """

    """
    Tests for __str__
    """

    """
    Tests for subclasses
    """
    def test_init_Deck1Joker_size53(self):
        d = deck.Deck1Joker()
        expected = 53
        result = len(d)
        self.assertEqual(expected, result)

    def test_init_Deck1Joker_containsZs(self):
        d = deck.Deck1Joker()
        joker = card.Card('Z', 's')
        expected = True
        result = d.contains(joker)
        self.assertEqual(expected, result)

    def test_init_Deck2Joker_containsZsZc(self):
        d = deck.Deck2Joker()
        joker1 = card.Card('Z', 's')
        joker2 = card.Card('Z', 'c')
        expected = True
        result = d.contains(joker1) and d.contains(joker2)
        self.assertEqual(expected, result)

if __name__ == "__main__":
    unittest.main()
