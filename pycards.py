#!/usr/bin/env python3

from __future__ import print_function
import blinds
import table
import os
import sys
import combos
import session

GAME = 'FIVE CARD DRAW'
TABLE = 6
STAKES = blinds.Blinds()
NAME = 'LUNNA'

# Define menu opions
options = {}
options['c'] = ('(C)ombination counts', 'view_combos()')
options['f'] = ('(F)ive card Draw', 'play_poker()')
options['n'] = ('(N)ame change', 'pick_name()')
options['s'] = ('(S)takes', 'pick_limit()')
options['t'] = ('(T)able size', 'pick_table()')
options['m'] = ('(M)enu', 'menu()')
options['e'] = ('(E)xit', 'exitgracefully()')


def print_logo():
    with open('logo.txt') as f:
        print(f.read())
    print('='*80)


def exitgracefully():
    print('Bye!')
    sys.exit()


def menu():
    os.system('clear')
    print_logo()
    print('')
    print('Settings:')
    print('Playername: {}'.format(NAME))
    print('Game:       {}'.format(GAME))
    print('Table Size: {}'.format(TABLE))
    print('Stakes:     {}'.format(STAKES))
    print('')
    for o in options:
        print(options[o][0])


def view_combos():
    for i in range(1, 8):
        print("There are {} combos of {} cards in a standard 52 card deck.".format(
            combos.n_choose_k(52, i), i))


def pick_limit():
    print('Please enter what limit you want to play:(default 2/4)')
    STAKES.levels()

    while True:
        choice = input(':> ')
        if int(choice) in STAKES.blind_dict.keys():
            print('You selected {}'.format(choice))
            STAKES.set_level(int(choice))
            break
        else:
            print('Selection not available, try again.')


def pick_table():
    print('What size table do you want to play? (default is 2 seats)')

    for l in table.VALID_SIZES:
        print('{}, '.format(l), end='')

    choice = input(':> ')
    if int(choice) in table.VALID_SIZES:
        print('You selected {}'.format(choice))
        TABLE = choice
    else:
        print('Selection not available, going with default: 6 seats')
        global TABLE
        TABLE = 6


def pick_name():
    print('Please enter your username.')
    while True:
        name = input(':> ')
        if len(name) > 15:
            print('Name is too long! Must be less than 15 characters.')
        else:
            break
    global NAME
    NAME = name


def play_poker():
    print('Alright, let\'s play some poker!')

    print('Initializing new game...\n')
    g = session.Draw5Session('FIVE CARD DRAW', STAKES, TABLE, NAME)

    playing = True

    while playing:
        print(g)
        g.play()
        choice = input('keep playing? > ')
        if choice.lower() == 'n' or choice == 0:
            playing = False

        os.system('clear')
    exit()


if __name__ == "__main__":
    print_logo()
    menu()

    while True:
        choice = input('> ')
        choice = choice.lower()

        if choice in options:
            exec(options[choice][1])
        else:
            print('Not a valid option!')
