import sessions
import discard


class Draw5Session(sessions.Session):
    def play(self):
        """
        Play a round of Five Card Draw.
        """
        DEALT = 5
        r = self.new_round()
        r._table.move_button()
        r._table.set_blinds()
        print(r.post_blinds())
        r.deal_cards(DEALT)
        r.sortcards()

        for s in self.streets:
            if r.street == 1:
                # Discard phase
                discards = discard.discard_phase(self._table, r.d)
                r.muck.extend(discards)
                r.sortcards()
                # print table after discarding and drawing

            if not r.betting_over():
                self.betting_round(r)

            if self.found_winner(r):
                break
        else:
            r.showdown()

        r.cleanup()
        self.rounds += 1
