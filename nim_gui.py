from tkinter import *
from tkinter import ttk

from nim_controller import NimController

FONT = "Helvetica"
class NimGui:
    def __init__(self, master):
        self.frame = master

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
            self.frame, textvariable=self.comp_text, font=(FONT, 10))

        # Label for displaying information about the previous move
        self.info_label = Label(
            self.frame, textvariable=self.move_text, font=(FONT, 12))

        # Label for displaying information about the game type
        self.game_info_label = Label(
            self.frame, textvariable=self.game_info, font=(FONT, 12))

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
        self.num_input =ttk.Combobox(self.frame, textvariable=self.remove_num, width=20)
        # num_input = Spinbox(
        #     self.frame, textvariable=self.remove_num, from_=1, to=10, width=20)

        # Checkbox for indicating whether the type of game should be normal or misere
        self.misere_checkbox = Checkbutton(
            self.frame, text="Misere game", variable=self.is_misere)

        # Button for starting a new game
        self.new_game_button = Button(
            self.frame, text="New Game", command=self.start_game, width=20)

        # Display all options on the window
        self.new_game_button.place(x=10, y=10)
        self.misere_checkbox.place(x=160, y=12)
        self.game_info_label.place(x=10, y=40)
        self.comp_text_label.place(x=10, y=65)
        self.computer_move_button.place(x=10, y=100)
        self.user_move_button.place(x=10, y=125)
        self.num_input.place(x=10,y=150)

        self.piles_label.place(x=200, y=175)
        self.info_label.place(x=200, y=125)
        self.disable_buttons()

    def make_pile_buttons(self):
        if(len(self.pile_buttons) > 0):
            self.remove_pile_buttons()
            self.pile_buttons = []

        piles_dict = self.nim_ctrl.get_pile_dict()
        x=25
        y=200
        for pile_name in piles_dict.keys():
            btn = Radiobutton(self.frame, text=pile_name,
                              variable=self.selected_pile, value=pile_name)
            self.pile_buttons.append(btn)
            if y > 800:
                x+=60
                y=200
            btn.place(x=x, y=y)
            y+=25


    def disable_buttons(self):
        self.user_move_button["state"] = "disabled"
        self.computer_move_button["state"] = "disabled"

    def check_game_over(self):
        if self.nim_ctrl.nim.winner:
            plural = "" if self.nim_ctrl.nim.winner == "You" else "s"
            self.game_info.set(f"{self.nim_ctrl.nim.winner} win{plural}!")
            self.disable_buttons()
            self.move_text.set('')

    def set_num_input(self):
        max_size = self.nim_ctrl.nim.get_max_pile_size()
        self.num_input["values"] = [i for i in range(1, max_size+1)]
        if max_size > 0:
            self.num_input.current(0)

    def start_game(self):
        self.nim_ctrl = NimController(self.is_misere.get())
        self.nim_ctrl.make_piles()
        self.make_pile_buttons()
        self.setup_page_strings()
        self.user_move_button["state"] = "normal"
        self.computer_move_button["state"] = "normal"
        self.set_num_input()
        self.comp_text.set('')
        self.move_text.set('')

    def setup_page_strings(self):
        game_type = "misere" if self.is_misere.get() else "normal"
        self.game_info.set(f'You are playing a {game_type} game')
        self.pile_string.set(self.nim_ctrl.get_pile_string())

    def remove_pile_buttons(self):
        for btn in self.pile_buttons:
            btn.place_forget()

    def make_computer_move(self):
        move_info = self.nim_ctrl.nim.make_winning_move()
        self.move_text.set(move_info)
        self.pile_string.set(self.nim_ctrl.get_pile_string())
        self.comp_text.set(self.nim_ctrl.nim.comp_text)
        self.user_move_button["state"] = "normal"
        self.computer_move_button["state"] = "disabled"
        self.set_num_input()
        self.check_game_over()


    def make_move(self):
        try:
            move_info = self.nim_ctrl.make_move(
                self.selected_pile.get(), self.remove_num.get())
            self.move_text.set(move_info)
            self.pile_string.set(self.nim_ctrl.get_pile_string())
            self.user_move_button["state"] = "disabled"
            self.computer_move_button["state"] = "normal"
            self.set_num_input()
            self.check_game_over()
            


        except ValueError:
            self.move_text.set("Invalid move")



main = Tk()
main.geometry("1600x1600")
c = NimGui(main)
main.mainloop()
