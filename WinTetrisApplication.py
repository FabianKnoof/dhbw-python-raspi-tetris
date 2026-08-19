import time

from tkinter import *

from Tetris import Tetris


class WinTetrisApplication:

    def __init__(self):

        self.root = Tk()

        self.number_columns = 10  # y-range/ width
        self.number_rows = 20  # x-range/ height

        self.tetris = Tetris(self.get_base_play_field(), self)

        self.label_matrix = self.get_label_play_field()

        self.timer_interval = 0.5

        self.label_score = Label(self.root, text="Score:")
        self.label_score.grid(row=self.number_rows + 1, column=0, columnspan=self.number_columns, sticky="W")

        self.root.bind("<Key>", self.move)

        Label(self.root, text="Movement: 'A','D' or 'Left','Right").grid(
            row=self.number_rows + 2, column=0, columnspan=self.number_columns - 2, sticky="W")
        Label(self.root, text="Rotation: 'Q','E' or ',''.'").grid(
            row=self.number_rows + 3, column=0, columnspan=self.number_columns, sticky="W")
        Label(self.root, text="Fall faster: 'S' or 'Down'").grid(
            row=self.number_rows + 4, column=0, columnspan=self.number_columns, sticky="W")

        # self.main()
        try:
            self.main()
        except TclError:
            print(TclError.__name__)

    def main(self):
        print("game start")
        while self.tetris.run():
            score = "Score: {}".format(self.tetris.get_score())
            self.label_score.config(text=score)
            self.update_view()
            time.sleep(self.timer_interval)  # this sets how fast the game will run

        print("game over")
        print(score)

        Label(self.root, text="game over").grid(row=self.number_rows + 1, column=6, columnspan=3)
        self.root.mainloop()

    def update_view(self):
        self.draw_fields_to_matrix()
        self.root.update_idletasks()
        self.root.update()

    def move(self, event):  # Directions are mirrored
        if event.char == "a" or event.keysym == "Left":
            self.tetris.move_tetromino_right()
        elif event.char == "d" or event.keysym == "Right":
            self.tetris.move_tetromino_left()
        elif event.char == "e" or event.char == ".":
            self.tetris.rotate_tetromino_counter_clockwise()
        elif event.char == "q" or event.char == ",":
            self.tetris.rotate_tetromino_clockwise()
        elif event.char == "s" or event.keysym == "Down":
            self.tetris.move_tetromino_down()
            self.tetris.move_tetromino_down()
            self.tetris.move_tetromino_down()
            self.tetris.move_tetromino_down()

        self.update_view()

    def get_label_play_field(self):
        label_matrix = []
        for row in range(self.number_rows):
            label_matrix.append([])
            for column in range(self.number_columns):
                label_matrix[row].append(Label(self.root, bg="black", width=2, height=1))
                label_matrix[row][column].grid(row=row, column=column, padx=1, pady=1)
        return label_matrix

    def get_base_play_field(self):
        base_play_field = []
        for row in range(self.number_rows):
            base_play_field.append([])
            for column in range(self.number_columns):
                base_play_field[row].append(0)
        return base_play_field

    def draw_fields_to_matrix(self):
        for pos_x, row in enumerate(self.tetris.get_play_field()):
            for pos_y, cell in enumerate(row):
                if cell == 1:
                    self.label_matrix[pos_x][pos_y].config(bg="white")
                else:
                    self.label_matrix[pos_x][pos_y].config(bg="black")

    def decrease_timer_interval(self):
        self.timer_interval *= 0.9


application = WinTetrisApplication()
