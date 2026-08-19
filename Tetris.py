from random import randint

from Tetrominos import *


class Tetris:

    def __init__(self, play_field, tetris_application):
        self.play_field = play_field
        self.tetris_application = tetris_application

        self.score = 0
        self.total_tetrominos = 0

        self.tetromino_spawn_pos_x = 0
        self.tetromino_spawn_pos_y = int(len(play_field[0]) / 2)

        self.falling_tetromino = self.get_random_tetromino()
        self.set_fields_on(self.falling_tetromino.get_pos())

    def run(self):
        self.move_tetromino_down()

        if not self.falling_tetromino.is_falling():
            self.update_game_speed()
            self.update_score()

            old_tetromino = self.falling_tetromino
            self.falling_tetromino = self.get_random_tetromino(self.total_tetrominos % 7)
            self.set_fields_on(self.falling_tetromino.get_pos())

            if self.check_if_lost(old_tetromino, self.falling_tetromino):
                return False

        return True

    def move_tetromino_down(self):
        old_pos = [pos[:] for pos in self.falling_tetromino.get_pos()]
        self.falling_tetromino.move_down()
        self.update_fields(old_pos, self.falling_tetromino.get_pos())

    def move_tetromino_right(self):
        old_pos = [pos[:] for pos in self.falling_tetromino.get_pos()]
        self.falling_tetromino.move_right()
        self.update_fields(old_pos, self.falling_tetromino.get_pos())

    def move_tetromino_left(self):
        old_pos = [pos[:] for pos in self.falling_tetromino.get_pos()]
        self.falling_tetromino.move_left()
        self.update_fields(old_pos, self.falling_tetromino.get_pos())

    def rotate_tetromino_clockwise(self):
        old_pos = [pos[:] for pos in self.falling_tetromino.get_pos()]
        self.falling_tetromino.rotate_clockwise()
        self.update_fields(old_pos, self.falling_tetromino.get_pos())

    def rotate_tetromino_counter_clockwise(self):
        old_pos = [pos[:] for pos in self.falling_tetromino.get_pos()]
        self.falling_tetromino.rotate_counter_clockwise()
        self.update_fields(old_pos, self.falling_tetromino.get_pos())

    def check_if_lost(self, old_tetromino, new_tetromino):
        for new_pos in new_tetromino.get_pos():
            if new_pos in old_tetromino.get_pos():
                return True
        return False

    def update_score(self):
        completed_rows = self.completed_rows()
        if len(completed_rows) != 0:
            self.remove_row(completed_rows)
            if len(completed_rows) == 1:
                self.score += 40
            elif len(completed_rows) == 2:
                self.score += 100
            elif len(completed_rows) == 3:
                self.score += 300
            elif len(completed_rows) == 4:
                self.score += 1200

    def completed_rows(self):
        completed_rows = []
        for row_count, row in enumerate(self.play_field):
            for cell in row:
                if cell != 1:
                    break
            else:
                completed_rows.append(row_count)
        return completed_rows

    def remove_row(self, completed_rows):
        for row in completed_rows:
            while row > 0:
                self.play_field[row] = self.play_field[row - 1]
                row -= 1
            self.play_field[0] = [0] * len(self.play_field[1])

    def update_game_speed(self):
        if self.total_tetrominos % 5 == 0:
            self.tetris_application.decrease_timer_interval()

    def update_fields(self, old_pos, new_pos):
        self.set_fields_off(old_pos)
        self.set_fields_on(new_pos)
        self.tetris_application.draw_fields_to_matrix()

    def set_fields_off(self, pos):
        for x in range(len(pos)):
            self.play_field[pos[x][0]][pos[x][1]] = 0

    def set_fields_on(self, pos):
        for x in range(len(pos)):
            self.play_field[pos[x][0]][pos[x][1]] = 1

    def get_random_tetromino(self, tetromino=-1):   # parameter to set a specific Tetromino to spawn
        if tetromino == -1:
            tetromino_number = randint(0, 6)
        else:
            tetromino_number = tetromino

        tetrominos = {
            0: ITetromino(self.tetromino_spawn_pos_x, self.tetromino_spawn_pos_y, self.play_field),
            1: JTetromino(self.tetromino_spawn_pos_x, self.tetromino_spawn_pos_y, self.play_field),
            2: LTetromino(self.tetromino_spawn_pos_x, self.tetromino_spawn_pos_y, self.play_field),
            3: OTetromino(self.tetromino_spawn_pos_x, self.tetromino_spawn_pos_y, self.play_field),
            4: STetromino(self.tetromino_spawn_pos_x, self.tetromino_spawn_pos_y, self.play_field),
            5: TTetromino(self.tetromino_spawn_pos_x, self.tetromino_spawn_pos_y, self.play_field),
            6: ZTetromino(self.tetromino_spawn_pos_x, self.tetromino_spawn_pos_y, self.play_field)
        }
        self.total_tetrominos += 1
        return tetrominos[tetromino_number]

    def get_play_field(self):
        return self.play_field

    def get_score(self):
        return self.score
