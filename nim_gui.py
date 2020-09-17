from tkinter import *
from nim_game import NimController


class NimGui:
    def __init__(self, master):
        self.frame = Frame(master)
        self.frame.pack()


        self.comp_text = StringVar()
        self.move_text = StringVar()
        self.game_info = StringVar()
        self.selected_pile = StringVar(value="A")
        self.remove_num = IntVar()
        self.pile_string = StringVar()
        self.is_misere = BooleanVar(value=False)
        self.pile_buttons = []

        # Label for displaying information from the computer
        self.comp_text_label = Label(
            self.frame, textvariable=self.comp_text, font=("Courier", 12))

        # Label for displaying information about the previous move
        self.info_label = Label(
            self.frame, textvariable=self.move_text, font=("Courier", 12))

        # Label for displaying information about the game type
        self.game_info_label = Label(
            self.frame, textvariable=self.game_info, font=("Courier", 12))

        # Label for displaying piles and their respective items
        self.piles_label = Label(
            self.frame, textvariable=self.pile_string, font=("Courier", 14))

        # Button that submits the user's move
        self.user_move_button = Button(
            self.frame, text="Make move", command=self.make_move, width=20)

        # Button for having the computer make a move
        self.computer_move_button = Button(
            self.frame, text="Make computer move", command=self.make_computer_move, width=20)

        # Integer input corresponding to the number of items to be removed from the selected pile
        num_input = Spinbox(
            self.frame, textvariable=self.remove_num, from_=1, to=10)

        # Checkbox for indicating whether the type of game should be normal or misere
        self.misere_checkbox = Checkbutton(
            self.frame, text="Misere game", variable=self.is_misere)

        # Button for starting a new game
        self.new_game_button = Button(
            self.frame, text="New Game", command=self.start_game)

        # Display all options on the window
        self.game_info_label.pack() 
        self.new_game_button.pack()
        self.misere_checkbox.pack()
        self.info_label.pack()
        self.piles_label.pack()
        self.comp_text_label.pack() 
        self.computer_move_button.pack()
        self.user_move_button.pack()
        num_input.pack()
        self.disable_buttons()

    def disable_buttons(self):
        self.user_move_button["state"] = "disabled"
        self.computer_move_button["state"] = "disabled"

    def check_game_over(self):
        if self.nim_ctrl.nim.winner:
            plural = "" if self.nim_ctrl.nim.winner == "You" else "s"
            self.game_info.set(f"{self.nim_ctrl.nim.winner} win{plural}!")
            self.disable_buttons()
            self.move_text.set('')


    def start_game(self):
        self.nim_ctrl = NimController(self.is_misere.get())
        self.nim_ctrl.make_piles()
        self.make_pile_buttons()
        self.setup_page_strings()
        self.user_move_button["state"] = "normal"
        self.computer_move_button["state"] = "normal"

    def setup_page_strings(self):
        game_type = "misere" if self.is_misere.get() else "normal"
        self.game_info.set(f'You are playing a {game_type} game')
        self.pile_string.set(self.nim_ctrl.get_pile_string())

    def remove_pile_buttons(self):
        for btn in self.pile_buttons:
            btn.pack_forget()

    def make_pile_buttons(self):
        if(len(self.pile_buttons) > 0):
            self.remove_pile_buttons()
            self.pile_buttons = []

        piles_dict = self.nim_ctrl.get_pile_dict()

        for pile_name in piles_dict.keys():
            btn = Radiobutton(self.frame, text=pile_name,
                              variable=self.selected_pile, value=pile_name)
            self.pile_buttons.append(btn)
            btn.pack()

    def make_computer_move(self):
        move_info = self.nim_ctrl.nim.make_winning_move()
        self.move_text.set(move_info)
        self.pile_string.set(self.nim_ctrl.get_pile_string())
        self.comp_text.set(self.nim_ctrl.get_comp_text())
        self.user_move_button["state"] = "normal"
        self.computer_move_button["state"] = "disabled"
        self.check_game_over()

    def make_move(self):
        try:
            move_info = self.nim_ctrl.make_move(
                self.selected_pile.get(), self.remove_num.get())
            self.move_text.set(move_info)
            self.pile_string.set(self.nim_ctrl.get_pile_string())
            self.user_move_button["state"] = "disabled"
            self.computer_move_button["state"] = "normal"
            self.check_game_over()

        except:
            self.move_text.set("Invalid move")



main = Tk()
main.geometry("600x600")
c = NimGui(main)
main.mainloop()
