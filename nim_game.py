import random as rnd
import string


class Pile:
    def __init__(self, name, size):
        self.name = name
        self.items = [1 for i in range(0, size)]

    def size(self):
        return len(self.items)

    def is_pile_empty(self):
        return True if len(self.items) == 0 else False

    def add_items(self, num_items):
        for i in range(0, num_items):
            self.items.append(1)

    def remove_items(self, num_items):
        if(num_items <= len(self.items)):
            for i in range(0, num_items):
                self.items.pop()
            plural = 's' if num_items > 1 else ''
            return(f"removed {num_items} item{plural} from pile {self.name}")
        else:
            raise ValueError(
                f"Couldn't remove {num_items} items from pile {self.name} as it only contains {len(self.items)} items")


class Nim:
    def __init__(self, misere):
        self.piles = []
        self.i_piles = {}
        self.misere = misere
        self.winner = False

    def is_game_over(self):
        for p in self.piles:
            if not p.is_pile_empty():
                return False

        return True

    def make_pile(self, name, num_items):
        self.piles.append(Pile(name, num_items))

    def get_max_size_pile(self):
        max_pile = Pile('negative', -1)
        for p in self.piles:
            if p.size() > max_pile.size():
                max_pile = p

        return max_pile

    # create and return a string to represent each pile and its corresponding items
    def view_piles(self):
        to_string = ''
        max_size = 0
        pile_str = ''
        for pile in self.piles:
            if pile.size() > max_size:
                max_size = pile.size()

            pile_str += f"  {pile.name}  "

        for i in range(max_size-1, -1, -1):
            for pile in self.piles:
                if len(pile.items) > i:
                    to_string += ('  =  ')
                else:
                    to_string += ('     ')

            to_string += '\n'
        to_string += pile_str
        return to_string

    # calculates the nim-sum of all piles
    def get_total_nim_sum(self):
        # creates an array to hold the size of each pile
        sizes = []
        for p in self.piles:
            sizes.append(p.size())

        total = sizes[0]
        # calculate the nim sum of each pile
        for i in range(1, len(sizes)):
            total = self.get_nim_sum(total, sizes[i])
        return total

    def get_nim_sum(self, a, b):
        return a ^ b

    def index_piles_by_name(self):
        self.i_piles = {}
        for pile in self.piles:
            self.i_piles.update({pile.name: pile})

    def make_finishing_misere_move(self):
        max_pile = self.get_max_size_pile()
        count_nonempty_piles = sum(1 for pile in self.piles if pile.size() > 0)
        if count_nonempty_piles % 2 == 1:
            move = max_pile.remove_items(max_pile.size()-1)
            if self.is_game_over():
                self.winner = "You"
            return "Computer "+move
        else:
            move = max_pile.remove_items(max_pile.size())
            if self.is_game_over():
                self.winner = "You"
            return "Computer "+move

    # This function is the "brains" of the computer player
    # It will make a winning move if one is available, otherwise it will make a completely random move
    def make_winning_move(self):
        if self.misere:
            # the strategy to win a misere games only differs when there is exactly one pile with a size >= 2
            piles_larger_than_2 = sum(
                1 for pile in self.piles if pile.size() > 1)
            if piles_larger_than_2 == 1:
                return self.make_finishing_misere_move()

        n_sum = self.get_total_nim_sum()
        # If the total nim sum is not zero prior to making a move, the computer will win this game
        if n_sum != 0:
            for p in self.piles:
                # get the size of the current pile
                p_len = p.size()

                # get the nim sum of the total nim sum of all piles and the current pile size
                p_sum = self.get_nim_sum(n_sum, p_len)

                # if the result of p_sum is less than the current pile size, reducing this pile will be a winning move
                if p_sum < p_len:
                    # we want to reduce this pile's size to the nim sum of its current size and the total nim sum of all pile sizes
                    rem = p_len - p_sum

                    # leave the nim-sum of all pile sizes is now zero,
                    # meaning it's now impossible for the user to win this game
                    move = p.remove_items(rem)
                    if self.is_game_over():
                        self.winner = "You" if self.misere else "Computer"
                    return "Computer "+move

        else:
            # Since the nim-sum of all pile sizes is zero prior to making a move,
            # it's not possible for the computer to win unless the user makes a mistake
            # So instead, the computer will make a random move
            p = rnd.choice(self.piles)
            while len(p.items) == 0:
                p = rnd.choice(self.piles)
            move = p.remove_items(rnd.randint(1, len(p.items)))
            if self.is_game_over():
                self.winner = "You" if self.misere else "Computer"
            return "Computer "+move


class NimController:
    def __init__(self, misere):
        self.nim = Nim(misere)

    def make_piles(self):
        # randomly generate a number of piles
        # because of how the system is built, this number can be increased to 26 (A-Z piles)
        # the game will still be fully playable by human and computer
        # it would be possible to increase further, but the way piles are named would need to be changed
        # and benefits of playing with 27+ piles doesn't seem worth the extra effort
        num_piles = rnd.randint(2, 5)
        valid_piles = {}

        # create a list of the piles and distribute one item to each pile
        for i in range(0, num_piles):
            valid_piles.update({string.ascii_uppercase[i]: 1})

        # since we have already distributed one to each pile, we set the distributed var equal to that amount
        distributed = num_piles

        random_buffer = rnd.randint(0, 5)
        # while we haven't distributed enough items, continue distributing items to random piles
        # we want at least 2*N+1 items distributed, but we include a buffer for some extra randomness
        while distributed < (2*num_piles+1)+random_buffer:
            pile_name = rnd.choice(list(valid_piles.keys()))
            valid_piles[pile_name] += 1
            distributed += 1

        # this loop effectively sorts the randomized piles so they are in alphabetical order
        for i in range(0, num_piles):
            self.nim.make_pile(
                string.ascii_uppercase[i], valid_piles[string.ascii_uppercase[i]])

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

    def get_comp_text(self):
         
    
