"""
  " Tests for tools.py
  """
import unittest
from ponyup import card
from ponyup import evaluator as ev
from ponyup import tools


class TestTools(unittest.TestCase):
    """ Functions tests for tools.py """
    def test_tocard_As_returnsAs(self):
        string = 'As'
        rank = 'A'
        suit = 's'
        result = tools.to_card(string)
        self.assertEqual(rank, result.rank)
        self.assertEqual(suit, result.suit)

    def test_tocard_AA_returnsAs(self):
        string = 'AA'
        self.assertRaises(Exception, tools.to_card, string)

    def test_converttocards_AsKs_returnsCardAsKs(self):
        As, Ks = card.Card('A', 's'), card.Card('K', 's')
        cardstr = ['As', 'Ks']
        expected = [As, Ks]
        result = tools.convert_to_cards(cardstr)
        self.assertEqual(expected, result)

    def test_make_royalflush_returnsRoyalFlush(self):
        h = tools.make('royalflush')
        expected = 'ROYAL FLUSH'
        result = ev.get_type(ev.get_value(h))
        self.assertEqual(expected, result)

    # Ask for 0 cards, returns 0 cards
    def test_getcards_0_returns0cards(self):
        h = tools.get_cards(0)
        expected = 0
        result = len(h)
        self.assertEqual(expected, result)

    # Ask for 1 cards, returns 1 cards
    def test_getcards_1_returns1card(self):
        h = tools.get_cards(1)
        expected = 1
        result = len(h)
        self.assertEqual(expected, result)

    # Ask for 2 cards, returns 2 cards
    def test_getcards_2_returns2cards(self):
        h = tools.get_cards(2)
        expected = 2
        result = len(h)
        self.assertEqual(expected, result)


class TestPokerhands(unittest.TestCase):
    """ Tests for all the poker hands to make sure get_value, get_type, and
        get_description work.
    """
    # ROYAL FLUSHES
    def test_getvalue_royalflush_returns100000000000(self):
        #  h = royalflush()
        h = tools.make('royalflush')
        expected = 100000000000
        result = ev.get_value(h)
        self.assertEqual(expected, result)

    def test_gettype_royalflush_returnsROYALFLUSH(self):
        h = tools.make('royalflush')
        h = tools.make('royalflush')
        val = ev.get_value(h)
        expected = 'ROYAL FLUSH'
        result = ev.get_type(val)
        self.assertEqual(expected, result)

    def test_get_description_royalflush_returnsAHigh(self):
        h = tools.make('royalflush')
        val = ev.get_value(h)
        expected = 'A High'
        result = ev.get_description(val, h)
        self.assertEqual(expected, result)

    # STRAIGHT FLUSHES
    def test_getvalue_straightflushhigh_returns90900000000(self):
        h = tools.make('straightflush_high')
        expected = 91300000000
        result = ev.get_value(h)
        self.assertEqual(expected, result)

    def test_gettype_straightflushhigh_returnsSTRAIGHTFLUSH(self):
        h = tools.make('straightflush_high')
        val = ev.get_value(h)
        expected = 'STRAIGHT FLUSH'
        result = ev.get_type(val)
        self.assertEqual(expected, result)

    def test_get_description_straightflushhigh_returnKHigh(self):
        h = tools.make('straightflush_high')
        val = ev.get_value(h)
        expected = 'K High'
        result = ev.get_description(val, h)
        self.assertEqual(expected, result)

    def test_getvalue_straightflushlow_returns90000000000(self):
        h = tools.make('straightflush_low')
        expected = 90000000000
        result = ev.get_value(h)
        self.assertEqual(expected, result)

    def test_gettype_straightflushlow_returnsSTRAIGHTFLUSH(self):
        h = tools.make('straightflush_low')
        val = ev.get_value(h)
        expected = 'STRAIGHT FLUSH'
        result = ev.get_type(val)
        self.assertEqual(expected, result)

    def test_get_description_straightflushlow_return5High(self):
        h = tools.make('straightflush_low')
        val = ev.get_value(h)
        expected = '5 High'
        result = ev.get_description(val, h)
        self.assertEqual(expected, result)

    # FOUR OF A KINDS, ('QUADS')
    def test_getvalue_quadshigh_returns81413000000(self):
        h = tools.make('quads_high')
        expected = 81413000000
        result = ev.get_value(h)
        self.assertEqual(expected, result)

    def test_gettype_quadshigh_returnsQUADS(self):
        h = tools.make('quads_high')
        val = ev.get_value(h)
        expected = 'QUADS'
        result = ev.get_type(val)
        self.assertEqual(expected, result)

    def test_get_description_quadshigh_returnsAs(self):
        h = tools.make('quads_high')
        val = ev.get_value(h)
        expected = 'A\'s'
        result = ev.get_description(val, h)
        self.assertEqual(expected, result)

    def test_getvalue_quadslow_returns80203000000(self):
        h = tools.make('quads_low')
        expected = 80203000000
        result = ev.get_value(h)
        self.assertEqual(expected, result)

    def test_gettype_quadslow_returnsQUADS(self):
        h = tools.make('quads_low')
        val = ev.get_value(h)
        expected = 'QUADS'
        result = ev.get_type(val)
        self.assertEqual(expected, result)

    def test_get_description_quadslow_returns2s(self):
        h = tools.make('quads_low')
        val = ev.get_value(h)
        expected = '2\'s'
        result = ev.get_description(val, h)
        self.assertEqual(expected, result)

    # FULL HOUSES ('BOATS')
    def test_getvalue_fullhousehigh_returns71413000000(self):
        h = tools.make('fullhouse_high')
        expected = 71413000000
        result = ev.get_value(h)
        self.assertEqual(expected, result)

    def test_gettype_fullhousehigh_returnsFULLHOUSE(self):
        h = tools.make('fullhouse_high')
        val = ev.get_value(h)
        expected = 'FULL HOUSE'
        result = ev.get_type(val)
        self.assertEqual(expected, result)

    def test_get_description_fullhousehigh_returnsAsfullofKs(self):
        h = tools.make('fullhouse_high')
        val = ev.get_value(h)
        expected = 'A\'s full of K\'s'
        result = ev.get_description(val, h)
        self.assertEqual(expected, result)

    def test_getvalue_fullhouselow_returns70203000000(self):
        h = tools.make('fullhouse_low')
        expected = 70203000000
        result = ev.get_value(h)
        self.assertEqual(expected, result)

    def test_gettype_fullhouselow_returnsFULLHOUSE(self):
        h = tools.make('fullhouse_low')
        val = ev.get_value(h)
        expected = 'FULL HOUSE'
        result = ev.get_type(val)
        self.assertEqual(expected, result)

    def test_get_description_fullhouselow_returns2sfullof3s(self):
        h = tools.make('fullhouse_low')
        val = ev.get_value(h)
        expected = '2\'s full of 3\'s'
        result = ev.get_description(val, h)
        self.assertEqual(expected, result)

    # FLUSHES
    def test_getvalue_flushhigh_returns61413121109(self):
        h = tools.make('flush_high')
        expected = 61413121109
        result = ev.get_value(h)
        self.assertEqual(expected, result)

    def test_gettype_flushhigh_returns(self):
        h = tools.make('flush_high')
        val = ev.get_value(h)
        expected = 'FLUSH'
        result = ev.get_type(val)
        self.assertEqual(expected, result)

    def test_get_description_flushhigh_returnsAhigh(self):
        h = tools.make('flush_high')
        val = ev.get_value(h)
        expected = 'A High'
        result = ev.get_description(val, h)
        self.assertEqual(expected, result)

    def test_getvalue_flushlow_returns60705040302(self):
        h = tools.make('flush_low')
        expected = 60705040302
        result = ev.get_value(h)
        self.assertEqual(expected, result)

    def test_gettype_flushlow_returns(self):
        h = tools.make('flush_low')
        val = ev.get_value(h)
        expected = 'FLUSH'
        result = ev.get_type(val)
        self.assertEqual(expected, result)

    def test_get_description_flushlow_returns7high(self):
        h = tools.make('flush_low')
        val = ev.get_value(h)
        expected = '7 High'
        result = ev.get_description(val, h)
        self.assertEqual(expected, result)

    # STRAIGHTS
    def test_getvalue_straighthigh_returns51413121110(self):
        h = tools.make('straight_high')
        expected = 51413121110
        result = ev.get_value(h)
        self.assertEqual(expected, result)

    def test_gettype_straighthigh_returnsSTRAIGHT(self):
        h = tools.make('straight_high')
        val = ev.get_value(h)
        expected = 'STRAIGHT'
        result = ev.get_type(val)
        self.assertEqual(expected, result)

    def test_get_description_straighthigh_returnAHigh(self):
        h = tools.make('straight_high')
        val = ev.get_value(h)
        expected = 'A High'
        result = ev.get_description(val, h)
        self.assertEqual(expected, result)

    def test_getvalue_straightmid_returns51110090807(self):
        h = tools.make('straight_mid')
        expected = 51110090807
        result = ev.get_value(h)
        self.assertEqual(expected, result)

    def test_gettype_straightmid_returnsSTRAIGHT(self):
        h = tools.make('straight_mid')
        val = ev.get_value(h)
        expected = 'STRAIGHT'
        result = ev.get_type(val)
        self.assertEqual(expected, result)

    def test_get_description_straightmid_returnJHigh(self):
        h = tools.make('straight_mid')
        val = ev.get_value(h)
        expected = 'J High'
        result = ev.get_description(val, h)
        self.assertEqual(expected, result)

    def test_getvalue_straightlow_returns50000000000(self):
        h = tools.make('straight_low')
        expected = 50000000000
        result = ev.get_value(h)
        self.assertEqual(expected, result)

    def test_gettype_straightlow_returnsSTRAIGHT(self):
        h = tools.make('straight_low')
        val = ev.get_value(h)
        expected = 'STRAIGHT'
        result = ev.get_type(val)
        self.assertEqual(expected, result)

    def test_get_description_straightlow_return5High(self):
        h = tools.make('straight_low')
        val = ev.get_value(h)
        expected = '5 High'
        result = ev.get_description(val, h)
        self.assertEqual(expected, result)

    # THREE OF A KIND ('SET', 'TRIPS'
    def test_getvalue_tripshigh_returns41413120000(self):
        h = tools.make('trips_high')
        expected = 41413120000
        result = ev.get_value(h)
        self.assertEqual(expected, result)

    def test_gettype_tripshigh_returnsTRIPS(self):
        h = tools.make('trips_high')
        val = ev.get_value(h)
        expected = 'TRIPS'
        result = ev.get_type(val)
        self.assertEqual(expected, result)

    def test_get_description_tripshigh_returnsAs(self):
        h = tools.make('trips_high')
        val = ev.get_value(h)
        expected = 'A\'s'
        result = ev.get_description(val, h)
        self.assertEqual(expected, result)

    def test_getvalue_tripslow_returns40204030000(self):
        h = tools.make('trips_low')
        expected = 40204030000
        result = ev.get_value(h)
        self.assertEqual(expected, result)

    def test_gettype_tripslow_returnsTRIPS(self):
        h = tools.make('trips_low')
        val = ev.get_value(h)
        expected = 'TRIPS'
        result = ev.get_type(val)
        self.assertEqual(expected, result)

    def test_get_description_tripslow_returns2s(self):
        h = tools.make('trips_low')
        val = ev.get_value(h)
        expected = '2\'s'
        result = ev.get_description(val, h)
        self.assertEqual(expected, result)

    # TWO PAIRS
    def test_getvalue_twopairhigh_returns31413120000(self):
        h = tools.make('twopair_high')
        expected = 31413120000
        result = ev.get_value(h)
        self.assertEqual(expected, result)

    def test_gettype_twopairhigh_returnsTWOPAIR(self):
        h = tools.make('twopair_high')
        val = ev.get_value(h)
        expected = 'TWO PAIR'
        result = ev.get_type(val)
        self.assertEqual(expected, result)

    def test_get_description_twopairhigh_returnsAsAndKs(self):
        h = tools.make('twopair_high')
        val = ev.get_value(h)
        expected = 'A\'s and K\'s'
        result = ev.get_description(val, h)
        self.assertEqual(expected, result)

    def test_getvalue_twopairlow_returns30302040000(self):
        h = tools.make('twopair_low')
        expected = 30302040000
        result = ev.get_value(h)
        self.assertEqual(expected, result)

    def test_gettype_twopairlow_returnsTWOPAIR(self):
        h = tools.make('twopair_low')
        val = ev.get_value(h)
        expected = 'TWO PAIR'
        result = ev.get_type(val)
        self.assertEqual(expected, result)

    def test_get_description_twopairlow_returns3sAnd2s(self):
        h = tools.make('twopair_low')
        val = ev.get_value(h)
        expected = '3\'s and 2\'s'
        result = ev.get_description(val, h)
        self.assertEqual(expected, result)

    # PAIRS
    def test_getvalue_pairhigh_returns21413121100(self):
        h = tools.make('pair_high')
        expected = 21413121100
        result = ev.get_value(h)
        self.assertEqual(expected, result)

    def test_gettype_pairhigh_returnsPAIR(self):
        h = tools.make('pair_high')
        val = ev.get_value(h)
        expected = 'PAIR'
        result = ev.get_type(val)
        self.assertEqual(expected, result)

    def test_get_description_pairhigh_returnsAs(self):
        h = tools.make('pair_high')
        val = ev.get_value(h)
        expected = 'A\'s'
        result = ev.get_description(val, h)
        self.assertEqual(expected, result)

    def test_getvalue_pairlow_returns20205040300(self):
        h = tools.make('pair_low')
        expected = 20205040300
        result = ev.get_value(h)
        self.assertEqual(expected, result)

    def test_gettype_pairlow_returnsPAIR(self):
        h = tools.make('pair_low')
        val = ev.get_value(h)
        expected = 'PAIR'
        result = ev.get_type(val)
        self.assertEqual(expected, result)

    def test_get_description_pairlow_returns2s(self):
        h = tools.make('pair_low')
        val = ev.get_value(h)
        expected = '2\'s'
        result = ev.get_description(val, h)
        self.assertEqual(expected, result)

    # Draws
    def test_getvalue_OESFD_returns1110090802(self):
        h = tools.make('OESFD')
        expected = 1110090802
        result = ev.get_value(h)
        self.assertEqual(expected, result)

    def test_gettype__returnsHIGHCARD(self):
        h = tools.make('OESFD')
        val = ev.get_value(h)
        expected = 'HIGH CARD'
        result = ev.get_type(val)
        self.assertEqual(expected, result)

    def test_getvalue_GSSFD_returns1110090702(self):
        h = tools.make('GSSFD')
        expected = 1110090702
        result = ev.get_value(h)
        self.assertEqual(expected, result)

    def test_gettype_GSSFD_returnsHIGHCARD(self):
        h = tools.make('GSSFD')
        val = ev.get_value(h)
        expected = 'HIGH CARD'
        result = ev.get_type(val)
        self.assertEqual(expected, result)

    def test_getvalue_flushdraw_hi_returns1410090702(self):
        h = tools.make('flushdrawA')
        expected = 1410090702
        result = ev.get_value(h)
        self.assertEqual(expected, result)

    def test_gettype_flushdrawhi_returnsHIGHCARD(self):
        h = tools.make('flushdrawA')
        val = ev.get_value(h)
        expected = 'HIGH CARD'
        result = ev.get_type(val)
        self.assertEqual(expected, result)

    def test_getvalue_flushdraw_returns1009070302(self):
        h = tools.make('flushdrawB')
        expected = 1009070302
        result = ev.get_value(h)
        self.assertEqual(expected, result)

    def test_gettype_flushdraw_returnsHIGHCARD(self):
        h = tools.make('flushdrawB')
        val = ev.get_value(h)
        expected = 'HIGH CARD'
        result = ev.get_type(val)
        self.assertEqual(expected, result)

    def test_getvalue_OESD_returns1110090802(self):
        h = tools.make('OESD')
        expected = 1110090802
        result = ev.get_value(h)
        self.assertEqual(expected, result)

    def test_gettype_OESD_returns(self):
        h = tools.make('OESD')
        val = ev.get_value(h)
        expected = 'HIGH CARD'
        result = ev.get_type(val)
        self.assertEqual(expected, result)

    def test_getvalue_GSSD_returns1413111002(self):
        h = tools.make('GSSD')
        expected = 1413111002
        result = ev.get_value(h)
        self.assertEqual(expected, result)

    def test_gettype_GSSD_returnsHIGHCARD(self):
        h = tools.make('GSSD')
        val = ev.get_value(h)
        expected = 'HIGH CARD'
        result = ev.get_type(val)
        self.assertEqual(expected, result)

    def test_getvalue_wheeldraw_returns1413040302(self):
        h = tools.make('wheeldraw')
        expected = 1413040302
        result = ev.get_value(h)
        self.assertEqual(expected, result)

    def test_gettype_wheeldraw_returnsHIGHCARD(self):
        h = tools.make('wheeldraw')
        val = ev.get_value(h)
        expected = 'HIGH CARD'
        result = ev.get_type(val)
        self.assertEqual(expected, result)
