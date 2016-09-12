import colors
import lobby
import names

"""
Provides tools for interacting with the user at the text-based console.
"""
menu = {}
menu['h'] = ('(H)elp', 'show_help()')
menu['o'] = ('(O)ptions', 'show_options()')
menu['q'] = ('(Q)uit', 'exit()')


def show_help():
    print('This is the help menu')


def show_options():
    print('This is the options menu')


def prompt(p=''):
    print(p)
    i = input(':> ')
    # Process the universal options
    if i in menu:
        exec(menu[i][1])  # Execute the menu item.
        return None
    else:  # We got something else...
        return i


def is_integer(num):
    """
    Returns True if the num argument is an integer, and False if it is not.
    """
    try:
        num = float(num)
    except:
        return False

    return num.is_integer()


def pick_game():
    tables = lobby.sorted_by_game_and_lev()
    print(lobby.numbered_list(tables))
    valid_choices = list(range(len(tables)))

    while True:
        choice = prompt('What game do you want to play?')
        if choice is None:
            pass
        elif is_integer(choice) is False:
            print('Please enter a number for your selection!')
        elif int(choice) in valid_choices:
            return tables[int(choice)]
        else:
            print('Selection not available, try again.')


def pick_name():
    while True:
        name = prompt('Please enter your username.')
        if name is None:
            pass
        elif not names.is_validname(name):
            print('Name must be between {} and {} characters long.'.format(
                names.MIN_LEN, names.MAX_LEN))
        elif names.has_surr_char(name):
            print('Name cannot have any of these characters: {}'.format(
                names.INVALID_CHARACTERS))
        else:
            return name


def betmenu(actions):
    """
    Display a list of betting options, and get input from the player to pick a valid option.
    """
    nice_opts = ['[' + colors.color(v.name[0], 'white', STYLE='BOLD') + ']' +
                 v.name[1:].lower()
                 for k, v in sorted(actions.items())]
    choices = '/'.join(nice_opts)

    while True:
        choice = prompt('{}?'.format(choices))
        if choice is None:
            pass  # They chose a main menu option
        elif choice.lower() in actions:
            return actions[choice]
        else:
            print('Invalid choice, try again.')


def display_table(table, hero=None):
    """
    Return the string representation of the table, with colors.
    """
    _str = ''
    _str = colors.color('{:5}{:7}{:7}{:20}{:<17}{:16}\n'.format(
        'Seat', 'Blinds', 'Dealer', 'Player', 'Chips', 'Hand'), 'gray', STYLE='BOLD')

    for i, s in enumerate(table.seats):
        if s is None:
            # No player is occupying the seat
            _str += '{}\n'.format(i)
            continue
        else:
            _str += '{:<5}'.format(i)

        if table.TOKENS['SB'] == i:
            _str += colors.color('{:7}'.format('[SB]'), 'lightblue')
        elif table.TOKENS['BB'] == i:
            _str += colors.color('{:7}'.format('[BB]'), 'blue')
        elif table.TOKENS['BI'] == i:
            _str += colors.color('{:7}'.format('[BI]'), 'lightblue')
        else:
            _str += ' '*7

        if table.TOKENS['D'] == i:
            _str += colors.color('{:7}'.format('[D]'), 'purple')
        else:
            _str += ' '*7

        _str += '{:20}'.format(str(s.player))

        _str += colors.color('${:<16}'.format(s.stack), 'yellow')

        # Display hand if available
        if s == hero:
            _str += '{:16}'.format(str(s.hand.peek()))
        elif s.hand is not None:
            _str += '{:16}'.format(str(s.hand))
        _str += '\n'

    return _str


def player_listing(table):
    """
    Returns the list of seats with players and stacks, for the hand history.
    """
    _str = ''
    for i, s in enumerate(table.seats):
        _str += 'Seat #{}: {}(${})\n'.format(i, str(s.player), s.stack)
    return _str


"""
How to make this display color?
def action_string(action):
    s = self.get_bettor()
    act_str = ''
    act_str += '{} {}s'.format(s.player, action.name.lower())

    amt = colors.color(' $' + str(action.cost), 'yellow')

    if action.name in ['BET', 'RAISE']:
        return colors.color(act_str, 'red') + amt
    elif action.name == 'CALL':
        return colors.color(act_str, 'white') + amt
    elif action.name == 'FOLD':
        return colors.color(act_str, 'purple')
    elif action.name == 'CHECK':
        return colors.color(act_str, 'white')
    elif action.name == 'ALLIN':
        return colors.color(
            '{}{} is all in.'.format(spacing(self.level()), s.player), 'gray')
    else:
        raise Exception('Error processing the action!')
"""
