import player
import table
import names
import random

DEPOSIT = 10000
DEF_STACK = 1000
STEP = 100


def factory(**new_config):
    config = {
        'seats': None,
        'game': None,
        'tablename': 'default',
        'types': 'random',  # Player types
        'names': 'bob',  # Player names, can be 'random'
        'empty': False,
        'heroseat': None,
        'deposit': DEPOSIT,
        'stack': DEF_STACK,
        'stepstacks': False,
        'variance': None,   # A percentage that the stack size can randomly vary.
        'remove': None,
    }

    config.update(new_config)
    SEATS = config['seats']
    t = table.Table(SEATS)
    t.name = config['tablename']

    if config['empty']:
        return t

    # Create a list of players
    if config['names'] == 'random':
        # Generate random names
        nameset = names.random_names(SEATS)
    else:
        nameset = [config['names'] + str(i) for i in range(SEATS)]

    # Fund and Seat the players
    for i, s in enumerate(t):
        if i == config['heroseat']:
            continue  # Save this seat for the hero.
        p = player.factory(nameset[i], config['game'], config['types'])

        p.deposit(config['deposit'])
        s.sitdown(p)

    # Players buyin to the table.
    # There are a few different ways to set stack sizes.
    # - There is a DEF_STACK value for a default.
    # - stack parameter sets the stack amount.
    # - There is a stepstacks bool to trigger stacksizes as a stepped 100, 200, 300, pattern.
    # - There is a BBs parameter passed as a (BB size, BB quantity) pair to set stacks to the
    #    commonly measured units of big blinds.
    # - There is a stackvariation parameter to randomly vary the sizes of the stacks. The
    #   parameter is a float value that is used to randomly calculate the variations.

    # *** Player buyins ***
    # Go through all the seats
    for i, s in enumerate(t):
        # Check if the seat is occupied or vacant.
        if s.vacant():
            continue

        # Buy chips based on the parameter preference
        if config['stepstacks']:
            s.buy_chips(STEP * (i + 1))
        elif config['stack']:
            s.buy_chips(config['stack'])
        else:
            s.buy_chips(DEF_STACK)

        # Random variations
        if config['variance']:
            hilimit = int(s.stack * config['variance'])
            offset = random.randint(0, hilimit)
            s.stack -= offset

    # Removes a player from the table, if specified.
    if config['remove'] is not None:
        t.pop(config['remove'])

    return t
