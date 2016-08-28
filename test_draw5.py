import unittest
import draw5
import hand
import pokerhands


class TestDraw5(unittest.TestCase):
    #  def test_(self):
        #  self.assertRaises(ValueError, )

    """
    Tests for auto_discard(hand):
    """
    # Royal flush - no discards
    def test_autodiscard_royalflush_returnsEmptyList(self):
        h = hand.Hand(pokerhands.royalflush())
        h.unhide()
        expected = []
        result = [repr(c) for c in sorted(draw5.auto_discard(h))]
        self.assertEqual(expected, result)

    # Straight flush - no discards
    def test_autodiscard_straightflush_returnsEmptyList(self):
        h = hand.Hand(pokerhands.straightflush_high())
        h.unhide()
        expected = []
        result = [repr(c) for c in sorted(draw5.auto_discard(h))]
        self.assertEqual(expected, result)

    # Full house - no discards
    def test_autodiscard_fullhouse_returnsEmptyList(self):
        h = hand.Hand(pokerhands.boat_high())
        h.unhide()
        expected = []
        result = [repr(c) for c in sorted(draw5.auto_discard(h))]
        self.assertEqual(expected, result)

    # Flush - no discards
    def test_autodiscard_flush_returnsEmptyList(self):
        h = hand.Hand(pokerhands.flush_low())
        h.unhide()
        expected = []
        result = [repr(c) for c in sorted(draw5.auto_discard(h))]
        self.assertEqual(expected, result)

    # Straight - no discards
    def test_autodiscard_straight_returnsEmptyList(self):
        h = hand.Hand(pokerhands.straight_mid())
        h.unhide()
        expected = []
        result = [repr(c) for c in sorted(draw5.auto_discard(h))]
        self.assertEqual(expected, result)

    # Quads - discard the non quad card
    def test_autodiscard_quads_returns1card(self):
        # [('A', 's'), ('A', 'd'), ('A', 'h'), ('A', 'c'), ('K', 'c')]
        h = hand.Hand(pokerhands.quads_high())
        h.unhide()
        expected = ['Kc']
        result = [repr(c) for c in sorted(draw5.auto_discard(h))]
        #  result = sorted([repr(c) for c in draw5.auto_discard(h)])
        self.assertEqual(expected, result)

    # Trips - discard the non-trip cards
    def test_autodiscard_trips_returns2cards(self):
        # [('A', 's'), ('K', 'h'), ('A', 'h'), ('A', 'd'), ('Q', 'c')]
        h = hand.Hand(pokerhands.set_high())
        h.unhide()
        expected = ['Qc', 'Kh']
        result = [repr(c) for c in sorted(draw5.auto_discard(h))]
        self.assertEqual(expected, result)

    # Pair - Discard the non-pair cards
    def test_autodiscard_pair_returns3cards(self):
        # [('K', 's'), ('Q', 'h'), ('A', 's'), ('A', 'd'), ('J', 'c')]
        h = hand.Hand(pokerhands.pair_high())
        h.unhide()
        expected = ['Jc', 'Qh', 'Ks']
        result = [repr(c) for c in sorted(draw5.auto_discard(h))]
        self.assertEqual(expected, result)

    # Two-Pair - Discard the non-pair card
    def test_autodiscard_2pair_returns1card(self):
        # [('A', 's'), ('A', 'h'), ('K', 's'), ('K', 'd'), ('Q', 'c')]
        h = hand.Hand(pokerhands.twopair_high())
        h.unhide()
        expected = ['Qc']
        result = [repr(c) for c in sorted(draw5.auto_discard(h))]
        self.assertEqual(expected, result)

    # OESFD - Discard the non-flush card
    def test_autodiscard_OESFD_returns1card(self):
        # [('J', 's'), ('T', 's'), ('8', 's'), ('2', 'd'), ('9', 's')]
        h = hand.Hand(pokerhands.OESFD())
        h.unhide()
        expected = ['2d']
        result = [repr(c) for c in sorted(draw5.auto_discard(h))]
        self.assertEqual(expected, result)

    # GSSFD - Discard the non-flush card
    def test_autodiscard_GSSFD_returns1card(self):
        # [('J', 's'), ('T', 's'), ('7', 's'), ('2', 'd'), ('9', 's')]
        h = hand.Hand(pokerhands.GSSFD())
        h.unhide()
        expected = ['2d']
        result = [repr(c) for c in sorted(draw5.auto_discard(h))]
        self.assertEqual(expected, result)

    # Flush draw - Discard the non-flush card
    def test_autodiscard_flushdraw_returns1card(self):
        # [('A', 's'), ('T', 's'), ('7', 's'), ('2', 'd'), ('9', 's')]
        h = hand.Hand(pokerhands.flushdrawA())
        h.unhide()
        expected = ['2d']
        result = [repr(c) for c in sorted(draw5.auto_discard(h))]
        self.assertEqual(expected, result)

    # OESD - Discard the non-straight card
    def test_autodiscard_OESD_returns1card(self):
        # [('J', 'h'), ('T', 's'), ('8', 'c'), ('2', 'd'), ('9', 's')]
        h = hand.Hand(pokerhands.OESD())
        h.unhide()
        expected = ['2d']
        result = [repr(c) for c in sorted(draw5.auto_discard(h))]
        self.assertEqual(expected, result)

    # GSSD - Discard the non-straightcard
    def test_autodiscard_GSSD_returns(self):
        # [('J', 'h'), ('T', 's'), ('A', 's'), ('2', 'd'), ('K', 'h')]
        h = hand.Hand(pokerhands.GSSD())
        h.unhide()
        expected = ['2d']
        result = [repr(c) for c in sorted(draw5.auto_discard(h))]
        self.assertEqual(expected, result)

    # Wheel draw - Discard the high card
    def test_autodiscard_wheel_returns(self):
        # [('3', 'h'), ('4', 's'), ('A', 's'), ('2', 'd'), ('K', 'h')]
        h = hand.Hand(pokerhands.wheeldraw())
        h.unhide()
        expected = ['Kh']
        result = [repr(c) for c in sorted(draw5.auto_discard(h))]
        self.assertEqual(expected, result)

    # BDFD(low cards) - Discard the non-flush cards
    def test_autodiscard_BDFD1returns2cards(self):
        # [('2', 'd'), ('4', 's'), ('5', 's'), ('7', 's'), ('K', 'h')]
        h = hand.Hand(pokerhands.BDFD1())
        h.unhide()
        expected = ['2d', 'Kh']
        result = [repr(c) for c in sorted(draw5.auto_discard(h))]
        self.assertEqual(expected, result)

    # BDFD(with 2 high cards) - Discard the low cards
    def test_autodiscard_BDFD2returns3cards(self):
        # [('A', 'd'), ('4', 's'), ('5', 's'), ('7', 's'), ('K', 'h')]
        h = hand.Hand(pokerhands.BDFD2())
        h.unhide()
        expected = ['4s', '5s', '7s']
        result = [repr(c) for c in sorted(draw5.auto_discard(h))]
        self.assertEqual(expected, result)

    # 3 High cards - Discard the 2 low cards
    def test_autodiscard_highcards_returns2cards(self):
        # [('A', 'd'), ('4', 's'), ('Q', 's'), ('7', 's'), ('K', 'h')]
        h = hand.Hand(pokerhands.highcards1())
        h.unhide()
        expected = ['4s', '7s']
        result = [repr(c) for c in sorted(draw5.auto_discard(h))]
        self.assertEqual(expected, result)

    # Ace high - Discard the non-pair card
    def test_autodiscard_acehigh_returns4cards(self):
        # [('A', 'd'), ('4', 's'), ('5', 's'), ('7', 's'), ('9', 'h')]
        h = hand.Hand(pokerhands.acehigh())
        h.unhide()
        expected = ['4s', '5s', '7s', '9h']
        result = [repr(c) for c in sorted(draw5.auto_discard(h))]
        self.assertEqual(expected, result)

    # 0 gap BDSD - Discard the non-connected cards
    def test_autodiscard_BDSD_returns2cards(self):
        # [('2', 'd'), ('7', 's'), ('8', 's'), ('9', 'd'), ('K', 'h')]
        h = hand.Hand(pokerhands.BDSD1())
        h.unhide()
        expected = ['2d', 'Kh']
        result = [repr(c) for c in sorted(draw5.auto_discard(h))]
        self.assertEqual(expected, result)

    # 1 gap BDSD - Discard the non-connected cards
    def test_autodiscard_BDSD2_returns2cards(self):
        # [('2', 'd'), ('7', 's'), ('8', 's'), ('9', 'd'), ('K', 'h')]
        h = hand.Hand(pokerhands.BDSD2())
        h.unhide()
        expected = ['2d', 'Kh']
        result = [repr(c) for c in sorted(draw5.auto_discard(h))]
        self.assertEqual(expected, result)

    # Medium cards/junk - Discard the 3 low cards
    def test_autodiscard_junk_returns(self):
        #  [('2', 'd'), ('3', 's'), ('6', 's'), ('8', 'd'), ('T', 'h')]
        h = hand.Hand(pokerhands.junk())
        h.unhide()
        expected = ['2d', '3s', '6s']
        result = [repr(c) for c in sorted(draw5.auto_discard(h))]
        self.assertEqual(expected, result)
