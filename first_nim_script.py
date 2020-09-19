import random as rnd
import string


def get_input_as_nonzero_int(prompt):
    while 1:
        try:
            res = int(input(prompt))
            if res <= 0:
                print("Your choice must be larger than 0!")
            else:
                return res
        except:
            print("I couldn't understand that. Try using a number...")


class Pile:
    def __init__(self, name, size):
        self.name = name
        self.items = [1 for i in range(0, size)]

    def size(self):
        return len(self.items)

    def is_pile_empty(self):
        return True if len(self.items) == 0 else False

    def print_pile_size(self):
        if(self.is_pile_empty()):
            print(f"Pile {self.name} is empty")
        else:
            print(f"Pile {self.name} has {len(self.items)} items")

    def add_items(self, num_items):
        for i in range(0, num_items):
            self.items.append(1)

        self.print_pile_size()

    def remove_items(self, num_items):
        if(num_items <= len(self.items)):
            for i in range(0, num_items):
                self.items.pop()
            print(f"Removed {num_items} items from pile {self.name}")
        else:
            raise ValueError(
                f"Couldn't remove {num_items} items from pile {self.name} as it only contains {len(self.items)} items")
     

class Nim:
    def __init__(self, misere):
        self.piles = []
        self.i_piles = {}
        self.misere = misere

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

    def view_piles(self):
        to_string = ''
        max_size = 0
        pile_str = ''
        for pile in self.piles:
            if pile.size() > max_size:
                max_size = pile.size()

            pile_str += f"| {pile.name} |"

        for i in range(max_size-1, -1, -1):
            for pile in self.piles:
                if len(pile.items) > i:
                    to_string += ('| = |')
                else:
                    to_string += ('|   |')

            to_string += '\n'
        to_string += pile_str
        print(to_string)

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


        pile_strings = f"{self.piles[0].size()}" 
        for pile in self.piles[1:]:
            pile_strings += f" ⊕  {pile.size()}" 
        pile_strings += f" = {total}"
        print(pile_strings)
        return total

    def get_nim_sum(self, a, b):
        return a ^ b

    def index_piles_by_name(self):
        self.i_piles = {}
        for pile in self.piles:
            self.i_piles.update({pile.name: pile})

    def select_valid_pile(self):
        self.view_piles()
        pile_name = input("Which pile would you like to remove from? ").upper()

        if pile_name not in self.i_piles.keys():
            print("Sorry, I couldn't find that pile!")
            return self.select_valid_pile()

        pile = self.i_piles[pile_name]

        if pile.is_pile_empty():
            print("You can't remove items from an empty pile!")
            return self.select_valid_pile()

        return pile

    def make_finishing_misere_move(self):
        max_pile = self.get_max_size_pile()
        count_nonempty_piles = sum(1 for pile in self.piles if pile.size() > 0)
        if count_nonempty_piles % 2 == 1:
            return max_pile.remove_items(max_pile.size()-1)
        else:
            return max_pile.remove_items(max_pile.size())

    def make_winning_move(self):
        if self.misere:
            # the strategy to win a misere games only differs when there is exactly one pile with a size >= 2
            piles_larger_than_2 = sum(1 for pile in self.piles if pile.size() > 1)
            if piles_larger_than_2 == 1:
                return self.make_finishing_misere_move()

        n_sum = self.get_total_nim_sum()
        if n_sum !=0:
            print(f"The total nim sum is not zero before the computer makes its move\nThis means the computer will win. It will look through all the piles until it finds one where the nim-sum of its size and X ({n_sum}) is less than its size")

            for p in self.piles:
                # get the size of the current pile
                p_len = p.size()

                # get the nim sum of the total nim sum of all piles and the current pile size
                p_sum = self.get_nim_sum(n_sum, p_len)

                # if the result of the previous p_sum is less than the current pile size, reducing this pile will be a winning move
                if p_sum < p_len:
                    print(f"Pile {p.name} has a size of {p_len}")
                    print(f"{p_len} ⊕  {n_sum} = {p_sum}")
                    print(f"Since {p_sum} < {p_len}, removing from this pile will be a winning move")
                    # print("Computer is making a winning move")

                    # we want to reduce this pile's size to the nim sum of its current size and the total nim sum of all pile sizes
                    print(f"The winning move is reducing {p.name}'s size to nim sum of its current size and X\n{p_len} ⊕  {n_sum} = {p_sum}")
                    rem = p_len - p_sum
                    print(f"The computer leaves the nim-sum of all pile sizes as zero, meaning it's now impossible for you to win this game :)")

                    return p.remove_items(rem)

        else:
            print("Since the nim-sum of all pile sizes is not zero prior to making a move, it's not possible for the computer to win unless you make a mistake (no pressure)")
            print("So instead, the computer will make its move at random")
            p = rnd.choice(self.piles)
            while len(p.items) == 0:
                p = rnd.choice(self.piles)

            return p.remove_items(rnd.randint(1, len(p.items)))

    def prompt_for_move(self):
        n_sum = self.get_total_nim_sum()
        result = "You can win" if n_sum != 0 else "You cannot win"
        if not self.misere:
            print(result)
        self.index_piles_by_name()
        pile = self.select_valid_pile()
        num = get_input_as_nonzero_int(
            f"How many items would you like to remove from pile {pile.name}? ")

        while num > len(pile.items):
            print(
                f"Couldn't remove {num} items from pile {pile.name} as it only contains {len(pile.items)} items")
            num = get_input_as_nonzero_int(
                f"How many items would you like to remove from pile {pile.name}? ")

        pile.remove_items(num)
        self.view_piles()




class NimController:
    def __init__(self, misere):
        self.nim = Nim(misere)

   
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

        for name, size in valid_piles.items():
            self.nim.make_pile(name, size)
        
    def get_pile_dict(self):
        self.nim.index_piles_by_name()
        return self.nim.i_piles

    def get_pile_string(self):
        return self.nim.view_piles()

    def make_move(self, pile_name, remove_num):
        self.nim.index_piles_by_name()
        return self.nim.i_piles[pile_name].remove_items(remove_num)


misere = False
g = NimController(misere)
g.make_piles()

# In a normal game, the goal is to be the last to take an object
# In misere play, the goal is to ensure the opponent takes the last object
# print("You are playing a normal game (You win if you take the last object)" if not misere else "You are playing a misere game (You win if your opponent takes the last object)")
while(1):
    print("\nYour turn\n")
    g.nim.prompt_for_move()
    if(g.nim.is_game_over()):
        print("You lost!" if misere else "You win!")
        break
    print("\nComputer's turn\n")
    g.nim.make_winning_move()
    if(g.nim.is_game_over()):
        print("Computer Lost!" if misere else "Computer won")
        break
