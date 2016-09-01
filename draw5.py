from __future__ import print_function
import card
import evaluator as ev
import poker

DEALT = 5


class Draw5Session(poker.Session):
    def play(self):
        """
        Play a round of Five Card Draw.
        """
        _round = self.new_round()

        if len(self._table.get_players(CARDS=True)) > 0:
            raise Exception('One or more players have cards before the deal!')

        _round.post_blinds()
        _round.deal_cards(DEALT)
        _round.sortcards()

        print(self._table)      # Show table pre draw

        # Pre-draw betting
        victor = _round.betting_round()

        print(_round)           # Display pot

        if victor is None:
            # Discard phase
            discards = discard_phase(self._table, _round.d)
            _round.muck.extend(discards)
            _round.sortcards()

            print(self._table)  # Show table post draw

            # Post-draw betting round
            victor = _round.betting_round()
            print(_round)           # Display pot

            if victor is None:
                # Showdown!
                _round.showdown()
            else:
                # 1 left:
                _round.award_pot(victor, _round.pot)
        else:
            # 1 left:
            _round.award_pot(victor, _round.pot)

        # Cleanup all cards
        _round.muck_all_cards()
        _round.check_integrity_post()

        # Remove broke players
        broke_players = _round._table.remove_broke()
        if broke_players:
            for p in broke_players:
                print('{} left the table with no money!'.format(p))

        # Move the table button
        self._table.move_button()

        # Advance round counter
        self.rounds += 1


def made_hand_discards(hand, ranklist):
    """
    Determine the best cards to discard for a given made hand.
    hand is a Hand object.
    """
    PAT_HANDS = ['STRAIGHT', 'FLUSH', 'FULL HOUSE', 'STRAIGHT FLUSH', 'ROYAL FLUSH']
    DIS_RANKS = ['PAIR', 'TRIPS', 'QUADS']

    if hand.rank() in PAT_HANDS:
        return []  # Don't discard anything
    elif hand.rank() in DIS_RANKS:
        #  standard discard
        paircard = ranklist[0].rank
        return ev.strip_ranks(hand.cards, paircard)
    elif hand.rank() == 'TWO PAIR':
        # Keep the two pair, discard 1.
        paircard = ranklist[0].rank + ranklist[1].rank

        return ev.strip_ranks(hand.cards, paircard)


def auto_discard(hand, max_discards=5):
    """
    Calculates the best discard in a 5 card hand. Takes a maximum number of allowed discards. If
    the auto-pick for discards is larger than the max, we will pop out the lowest cards(thereby
    keeping the higher and more valuable cards) until we reach the allowable number.
    # hand is a Hand object
    """
    ranklist = ev.rank_list(hand.cards)
    if hand.rank() == 'HIGH CARD':
        # Process any available draws
        discards = draw_discards(sorted(hand.cards[:]), ranklist)
    else:
        discards = made_hand_discards(hand, ranklist)

    while len(discards) > max_discards:
        lowcard = min(discards)
        discards.remove(lowcard)

    return discards


def draw_discards(cards, ranklist):
    """
    Calculates the approprate card to discard for any draw-type hands.
    """
    suit = ev.dominant_suit(cards)
    suit_count = ev.count_suit(cards, suit)

    if suit_count == 4:
        return ev.strip_suits(cards, suit)

    # Test for open-ended straight draw(s)
    OESD = ev.check_draw(cards, 4, 0)
    if OESD is not None:
        return ev.extract_discards(cards, OESD)

    # Test for gutshot straight draw(s)
    GSSD = ev.check_draw(cards, 4, 1)
    if GSSD is not None:
        return ev.extract_discards(cards, GSSD)

    # Test for the wheel draw
    if ranklist[0].rank == 'A':
        WD = ev.check_draw(cards, 3, 1)

        if WD is not None and WD[-1].val() <= 5:
            # The obvious discard is the dangling high card
            return [cards[-2]]

    # Draw to high cards (J+)
    if card.RANKS[ranklist[2].rank] > 10:
        highcards = ''.join([ranklist[i].rank for i in range(3)])
        return ev.strip_ranks(cards, highcards)
    elif card.RANKS[ranklist[1].rank] > 10:
        highcards = ''.join([ranklist[i].rank for i in range(2)])
        return ev.strip_ranks(cards, highcards)

    # Draw to an Ace
    # We'll generally draw to an Ace over any backdoor draws.
    if ranklist[0].rank == 'A':
        return ev.strip_ranks(cards, 'A')

    if suit_count == 3:  # Backdoor flush draw
        return ev.strip_suits(cards, suit)

    # Backdoor straight draws are pretty desparate
    BDSD = ev.check_draw(cards, 3, 0)
    if BDSD is not None:
        return ev.extract_discards(cards, BDSD)

    # 1-gap Backdoor straight draws are truly desparate!
    BDSD = ev.check_draw(cards, 3, 1)
    if BDSD is not None:
        return ev.extract_discards(cards, BDSD)

    # Last ditch effort - just draw to the best 2.
    highcards = ''.join([ranklist[i].rank for i in range(2)])
    return ev.strip_ranks(cards, highcards)


def discard_phase(table, deck):
    """
    Goes through a table and offers all players with cards the option to discard.
    Returns a list of all the discards (ie:"muck" cards)
    """
    print('Discard phase: ' + '~'*55)
    # Make sure the button goes last!
    holdingcards = table.get_players(CARDS=True)
    muckpile = []

    for p in holdingcards:
        max_discards = (5 if len(deck) >= 5 else len(deck))
        if max_discards == 0:
            print('Deck has been depleted!')
            break
        if p.is_human():
            discards = human_discard(p._hand, max_discards)
        else:
            discards = auto_discard(p._hand, max_discards)

        if discards:
            print('{} discards {}'.format(str(p), discards).rjust(70))
        else:
            print('{} stands pat.'.format(str(p)).rjust(70))

        # Redraw!
        human_draw = []
        for c in discards:
            muckpile.append(p.discard(c))
            draw = deck.deal()

            if p.is_human():
                draw.hidden = False
                human_draw.append(draw)

            p.add_card(draw)

        if p.is_human():
            print('{} draws {}'.format(str(p), human_draw).rjust(70))

    print('')

    return muckpile


def discard_menu(hand):
    cards = ' '.join([str(c) for c in hand.cards])
    txt = 'Your discard....1  2  3  4  5\n'.rjust(70)
    txt += '\t'*7 + cards
    txt += '\n'
    return txt


def help_txt():
    print('')
    print('Enter the cards you want to discard:')
    print('Example: "1" discards card 1, "12" discards cards 1 and 2, etc.')


def human_discard(hand, max_discards=5):
    """
    Offers the human player a menu of discard options and returns the list of chosen discards.
    """
    print(discard_menu(hand))
    while True:
        helpme = ['?', 'h', 'help']
        user_str = input(':> ')
        if user_str in helpme:
            help_txt()
            continue

        # Split up the #s, and reverse them so we can remove them without the list
        # collapsing and disrupting the numbering.
        valid_picks = ['1', '2', '3', '4', '5']
        picks = sorted(
            [int(x) for x in set(user_str) if x in valid_picks], reverse=True)

        if len(picks) > max_discards:
            print('Sorry, the deck is low -- you can only pick up to {} cards.'.format(
                max_discards))
            continue

        discards = []

        for n in picks:
            discards.append(hand.cards[int(n) - 1])
        break
    return discards
