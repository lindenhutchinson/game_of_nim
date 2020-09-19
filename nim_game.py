import random as rnd
import string


class Pile:
    def __init__(self, name, size):
        self.name = name
        self.size = size

    def add_items(self, num_items):
        self.size += num_items


    def remove_items(self, num_items):
        if(num_items <= self.size):
            self.size -= num_items
            return(f"removed {num_items} item{'s' if num_items > 1 else ''} from pile {self.name}")
        else:
            raise ValueError(
                f"Couldn't remove {num_items} items from pile {self.name} as it only contains {self.size} items")


class Nim:
    def __init__(self, misere):
        self.piles = []
        self.i_piles = {}
        self.comp_text = ''
        self.misere = misere
        self.winner = False

    def is_game_over(self):
        for p in self.piles:
            if p.size > 0:
                return False

        return True

    def make_pile(self, name, num_items):
        self.piles.append(Pile(name, num_items))

    # calculates the nim-sum of all piles
    def get_total_nim_sum(self):
        # creates an array to hold the size of each pile
        sizes = []
        for p in self.piles:
            sizes.append(p.size)

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

    def get_max_pile_size(self):
        max_pile_size = 0
        for p in self.piles:
            if p.size > max_pile_size:
                max_pile_size = p.size

        return max_pile_size

    def make_finishing_misere_move(self):
        max_pile_size = 0
        for p in self.piles:
            if p.size > max_pile_size:
                max_pile = p
                max_pile_size = p.size

        count_nonempty_piles = sum(1 for pile in self.piles if pile.size > 0)

        if count_nonempty_piles % 2 == 1:
            move = max_pile.remove_items(max_pile.size-1)
            if self.is_game_over():
                self.winner = "You"
            return "Computer "+move
        else:
            move = max_pile.remove_items(max_pile.size)
            if self.is_game_over():
                self.winner = "You"
            return "Computer "+move

    # This function is the "brains" of the computer player
    # It will make a winning move if one is available, otherwise it will make a completely random move
    # This move is made in O(n) time so the number of piles barely impacts the system solution
    def make_winning_move(self):
        if self.misere:
            # the strategy to win a misere games only differs when there is exactly one pile with a size >= 2
            piles_larger_than_2 = sum(
                1 for pile in self.piles if pile.size > 1)
            if piles_larger_than_2 == 1:
                return self.make_finishing_misere_move()

        n_sum = self.get_total_nim_sum()
        # If the total nim sum is not zero prior to making a move, the computer will win this game
        if n_sum != 0:
            winning_moves = {}
            for p in self.piles:
                # get the nim sum of the total nim sum of all piles and the current pile size
                p_sum = self.get_nim_sum(n_sum, p.size)

                # if the result of p_sum is less than the current pile size, reducing this pile will be a winning move
                if p_sum < p.size:
                    # we want to reduce this pile's size to the nim sum of its current size and the total nim sum of all pile sizes
                    rem = p.size - p_sum
                    winning_moves.update({p: rem})

            if len(winning_moves.keys()) > 0:
                best_rem = 0
                for pile, rem in winning_moves.items():
                    if rem > best_rem:
                        best_rem = rem
                        best_pile = pile
                        # the nim-sum of all pile sizes is now zero,
                        # meaning it's now impossible for the user to win this game
                self.comp_text = "It's no longer possible for you to win this game :)"
                move = best_pile.remove_items(best_rem)
                if self.is_game_over():
                    self.winner = "You" if self.misere else "Computer"
                return "Computer "+move

        else:
            # Since the nim-sum of all pile sizes is zero prior to making a move,
            # it's not possible for the computer to win unless the user makes a mistake
            # So instead, the computer will make a random move
            p = rnd.choice(self.piles)
            while p.size == 0:
                p = rnd.choice(self.piles)

            move = p.remove_items(rnd.randint(1, p.size))
            if self.is_game_over():
                self.winner = "You" if self.misere else "Computer"
            return "Computer "+move
