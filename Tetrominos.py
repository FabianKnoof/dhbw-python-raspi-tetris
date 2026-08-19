from abc import ABC


class Tetromino(ABC):

    def __init__(self, play_field):
        self.falling = True

        self.pos = []

        self.play_field = play_field
        self.play_field_height = len(play_field)
        self.play_field_width = len(play_field[0])

    def move_down(self):
        for pos in self.get_max_pos_x():
            if pos[0] + 1 == self.play_field_height:
                self.stop_falling()
                return
            if self.play_field[pos[0] + 1][pos[1]] == 1:
                self.stop_falling()
                return
        self.pos[0][0] += 1
        self.pos[1][0] += 1
        self.pos[2][0] += 1
        self.pos[3][0] += 1

    def move_right(self):
        for pos in self.get_min_pos_y():
            if pos[1] - 1 < 0:
                return
            if self.play_field[pos[0]][pos[1] - 1] == 1:
                return
        self.pos[0][1] -= 1
        self.pos[1][1] -= 1
        self.pos[2][1] -= 1
        self.pos[3][1] -= 1

    def move_left(self):
        for pos in self.get_max_pos_y():
            if pos[1] + 1 == self.play_field_width:
                return
            if self.play_field[pos[0]][pos[1] + 1] == 1:
                return
        self.pos[0][1] += 1
        self.pos[1][1] += 1
        self.pos[2][1] += 1
        self.pos[3][1] += 1

    def rotate_clockwise(self):
        center_pos = self.get_pos()[0]
        centered_pos = self.get_centered_pos(center_pos)  # Centered position, the position ist centered on (0,0)
        rotated_centered_pos = []
        for pos in centered_pos:
            rotated_centered_pos.append((pos[1] * (-1), pos[0]))  # Rotating each position
        rotated_pos = self.get_rotated_pos(center_pos, rotated_centered_pos)  # 'Decentering' the position

        if self.check_if_rotated_pos_is_valid(rotated_pos):
            self.set_pos(rotated_pos)

    def rotate_counter_clockwise(self):
        center_pos = self.get_pos()[0]
        centered_pos = self.get_centered_pos(center_pos)
        rotated_centered_pos = []
        for pos in centered_pos:
            rotated_centered_pos.append((pos[1], pos[0] * (-1)))
        rotated_pos = self.get_rotated_pos(center_pos, rotated_centered_pos)

        if self.check_if_rotated_pos_is_valid(rotated_pos):
            self.set_pos(rotated_pos)

    def check_if_rotated_pos_is_valid(self, rotated_pos):
        for i, pos in enumerate(rotated_pos):
            if pos[0] < 0 or pos[0] > self.play_field_height - 1:
                return False
            if pos[1] < 0 or pos[1] > self.play_field_width - 1:
                return False
            if self.play_field[pos[0]][pos[1]] == 1:
                if pos not in self.get_pos():
                    return False
        return True

    def get_rotated_pos(self, center_pos,
                        rotated_centered_pos):  # Adds the 'base' offset of the position back to the position and
        # returns the results
        rotated_pos = []
        for pos in rotated_centered_pos:
            rotated_pos.append([pos[0] + center_pos[0], pos[1] + center_pos[1]])
        return rotated_pos

    def get_centered_pos(self,
                         center_pos):  # Subtracts the offset from the position, so that the first position of the
        # tetromino is (0,0) and returns the results
        centered_pos = []
        for pos in self.get_pos():
            centered_pos.append([pos[0] - center_pos[0], pos[1] - center_pos[1]])
        return centered_pos

    def get_max_pos_x(
            self):  # returns the highest x position for each y position of the tetromino
        # (the bottom edge of the tetromino)
        pos_y_set = {self.pos[0][1], self.pos[1][1], self.pos[2][1], self.pos[3][1]}
        max_pos = [[]]
        for pos in self.get_pos():
            for i, pos_y in enumerate(pos_y_set):
                if pos[1] == pos_y:
                    while len(max_pos) - 1 < i:
                        max_pos.append([])
                    max_pos[i].append([pos[0], pos_y])
        max_pos = [max(pos) for pos in max_pos]
        return max_pos

    def get_max_pos_y(
            self):  # returns the highest y position for each x position of the tetromino
        # (the left edge of the tetromino)
        max_pos = [max(pos) for pos in self.get_pos_y_ordered()]
        return max_pos

    def get_min_pos_y(
            self):  # returns the lowest y position for each x position of the tetromino
        # (the right edge of the tetromino)
        min_pos = [min(pos) for pos in self.get_pos_y_ordered()]
        return min_pos

    def get_pos_y_ordered(self):  # return the y positions, ordered based on the x position
        pos_x_set = {self.pos[0][0], self.pos[1][0], self.pos[2][0], self.pos[3][0]}
        result_pos = [[]]
        for pos in self.get_pos():
            for i, pos_x in enumerate(pos_x_set):
                if pos[0] == pos_x:
                    while len(result_pos) - 1 < i:
                        result_pos.append([])
                    result_pos[i].append([pos_x, pos[1]])
        return result_pos

    def set_pos(self, pos):
        self.pos = pos

    def get_pos(self):
        return self.pos

    def is_falling(self):
        return self.falling

    def stop_falling(self):
        self.falling = False


class ITetromino(Tetromino):
    def __init__(self, pos_x_1, pos_y_1, play_field):
        super().__init__(play_field)
        self.pos = [[pos_x_1, pos_y_1], [pos_x_1 + 1, pos_y_1], [pos_x_1 + 2, pos_y_1], [pos_x_1 + 3, pos_y_1]]


class JTetromino(Tetromino):
    def __init__(self, pos_x_1, pos_y_1, play_field):
        super().__init__(play_field)
        self.pos = [[pos_x_1, pos_y_1], [pos_x_1 + 1, pos_y_1], [pos_x_1 + 2, pos_y_1], [pos_x_1 + 2, pos_y_1 + 1]]


class LTetromino(Tetromino):
    def __init__(self, pos_x_1, pos_y_1, play_field):
        super().__init__(play_field)
        self.pos = [[pos_x_1, pos_y_1], [pos_x_1 + 1, pos_y_1], [pos_x_1 + 2, pos_y_1], [pos_x_1 + 2, pos_y_1 - 1]]


class OTetromino(Tetromino):
    def __init__(self, pos_x_1, pos_y_1, play_field):
        super().__init__(play_field)
        self.pos = [[pos_x_1, pos_y_1], [pos_x_1 + 1, pos_y_1], [pos_x_1, pos_y_1 - 1], [pos_x_1 + 1, pos_y_1 - 1]]


class STetromino(Tetromino):
    def __init__(self, pos_x_1, pos_y_1, play_field):
        super().__init__(play_field)
        self.pos = [[pos_x_1, pos_y_1], [pos_x_1, pos_y_1 + 1], [pos_x_1 + 1, pos_y_1 + 1], [pos_x_1 + 1, pos_y_1 + 2]]


class TTetromino(Tetromino):
    def __init__(self, pos_x_1, pos_y_1, play_field):
        super().__init__(play_field)
        self.pos = [[pos_x_1, pos_y_1], [pos_x_1 + 1, pos_y_1 - 1], [pos_x_1 + 1, pos_y_1], [pos_x_1 + 1, pos_y_1 + 1]]


class ZTetromino(Tetromino):
    def __init__(self, pos_x_1, pos_y_1, play_field):
        super().__init__(play_field)
        self.pos = [[pos_x_1, pos_y_1], [pos_x_1, pos_y_1 - 1], [pos_x_1 + 1, pos_y_1 - 1], [pos_x_1 + 1, pos_y_1 - 2]]
