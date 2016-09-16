import blinds
import draw5
import names
import player
import stud
import table_factory


def factory(**new_config):
    config = {
        'seats': None,
        'poolsize': 100,
        'game': None,
        'tablename': 'default',
        'table': None,
        'hero': None,  # If there is a hero, they will be placed at the hero seat.
        'heroseat': 0,
        'level': 1,
        'names': 'bob',
        'deposit': table_factory.DEPOSIT
    }
    config.update(new_config)
    playerpool = make_playerpool(quantity=config['poolsize'])

    # Construct the table
    t = table_factory.factory(
        seats=config['seats'],
        heroseat=(config['heroseat'] if config['hero'] is not None else None),
        game=config['game'],
        tablename=config['tablename'],
        names=config['names'],
    )

    # Create and place the hero player.
    if config['hero']:
        hero = config['hero']
        heroseat = t.seats[config['heroseat']]
        heroseat.sitdown(hero)
        heroseat.buy_chips(table_factory.DEF_STACK)

    if config['game'] == 'FIVE CARD STUD':
        b = blinds.BlindsAnte(config['level'])
        sesh = stud.Stud5Session(config['game'], table=t, blinds=b)

    elif config['game'] == 'FIVE CARD DRAW':
        b = blinds.BlindsNoAnte(config['level'])
        sesh = draw5.Draw5Session(config['game'], table=t, blinds=b)
    else:
        raise ValueError('Game unknown to session!')

    # Set tablename for the session.
    sesh.playerpool = playerpool
    return sesh


def make_playerpool(**new_config):
    config = {
        'quantity': None,
        'game': None,
        'types': 'random',  # Player types
        'names': 'bob',  # Player names, can be 'random'
        'deposit': table_factory.DEPOSIT,
        'variance': None,   # A percentage that the deposit can randomly vary.
    }
    config.update(new_config)
    qty = config['quantity']

    if qty is None or qty <= 0:
        raise ValueError('Cannot make an empty playerpool!')

    # Create a list of players
    if config['names'] == 'random':
        # Generate random names
        nameset = names.random_names(qty)
    else:
        nameset = [config['names'] + str(i) for i in range(qty)]

    playerpool = []

    # Create the players
    for i, n in enumerate(nameset):
        p = player.factory(n, config['game'], config['types'])
        playerpool.append(p)

    # Fund the players
    for p in playerpool:
        p.deposit(config['deposit'])

    return playerpool
