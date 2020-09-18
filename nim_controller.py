from nim_game import Nim, Pile
import string
import random as rnd


class NimController:
    def __init__(self, misere):
        self.nim = Nim(misere)
        self.moves_lives = ''

    def make_piles(self):
        # randomly generate a number of piles in O(n) time

        self.num_piles = rnd.randint(2, 5)
        valid_piles = {}
        j = 0
        # create a list of the piles and distribute one item to each pile

        for i in range(0, self.num_piles):
            pile_name = string.ascii_uppercase[i % 26]
            if i >= 26:
                pile_name = string.ascii_uppercase[j] + \
                    string.ascii_uppercase[i % 26]

            if i % 26 == 0 and i > 26:
                j += 1

            valid_piles.update({pile_name: 1})

        # since we have already distributed one to each pile, we set the distributed var equal to that amount
        distributed = self.num_piles

        random_buffer = rnd.randint(0, 10)
        # while we haven't distributed enough items, continue distributing items to random piles
        # we want at least 2*N+1 items distributed, but we include a buffer for some extra randomness
        while distributed < (2*self.num_piles+1)+random_buffer:
            pile_name = rnd.choice(list(valid_piles.keys()))
            valid_piles[pile_name] += 1
            distributed += 1

        # j=0
        # for i in range(0, self.num_piles):
        #     pile_name = string.ascii_uppercase[i%26]

        #     if i >= 26:
        #         pile_name=string.ascii_uppercase[j]+string.ascii_uppercase[i%26]
        #     if i % 26 == 0:
        #         j+=1
        for name, size in valid_piles.items():
            self.nim.make_pile(name, size)

    # utility functions used by the gui

    def get_pile_dict(self):
        self.nim.index_piles_by_name()
        return self.nim.i_piles

    def get_pile_string(self):
        return self.nim.view_piles()

    def make_move(self, pile_name, remove_num):
        self.nim.index_piles_by_name()
        move = self.nim.i_piles[pile_name].remove_items(remove_num)
        if self.nim.is_game_over():
            self.nim.winner = "Computer" if self.nim.misere else "You"

        return "You "+move
