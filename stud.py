import evaluator


def highhand(table):
    """
    Finds which player has the highest showing hand and return their seat index.  For stud
    games, after the first street, the high hand on board initiates the action (a tie is broken
    by position, with the player who received cards first acting first).
    """
    highvalue = 0
    seat = None
    ties = []

    for s in table.get_players(hascards=True):
        h = s.hand.get_upcards()
        value = evaluator.get_value(h)

        if value > highvalue:
            highvalue, seat = value, s
            ties = [seat]  # Reset any lower ties.
        elif value == highvalue:
            ties.append(s)
            if seat not in ties:
                ties.append(seat)

    # Return the seat index of the first-to-act.
    if len(ties) > 1:
        # Process ties, get the player who was dealt first.
        for s in table.get_players(hascards=True):
            if s in ties:
                return s.NUM
    else:
        return seat.NUM
