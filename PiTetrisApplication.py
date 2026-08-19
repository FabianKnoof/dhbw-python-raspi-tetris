import time, os, sys

from gpiozero import Button

from luma.core.interface.serial import spi, noop
from luma.core.render import canvas
from luma.led_matrix.device import max7219
from luma.core.virtual import viewport
from luma.core.legacy import text
from luma.core.legacy.font import proportional, LCD_FONT

from Tetris import Tetris


class PiTetrisApplication:

    def __init__(self):
        self.serial = spi(port=0, device=0, gpio=noop())
        self.device = max7219(self.serial, width=32, height=8,
                              block_orientation=-90)  # set led matrix width and height here and maybe change the tetromino_orientation
        # in this case, width equals the x-axis, height equals the y-axis
        # tetrominos will move down along the x-axis

        self.button_reset_game = Button(13)
        self.button_reset_game.when_pressed = lambda: os.execl(sys.executable, sys.executable, *sys.argv)

        self.tetris = Tetris(self.get_base_play_field(), self)

        self.button_move_right = Button(27)
        self.button_move_right.when_activated = lambda: self.tetris.move_tetromino_right()

        self.button_move_left = Button(17)
        self.button_move_left.when_pressed = lambda: self.tetris.move_tetromino_left()

        self.button_rotate_clockwise = Button(5)
        self.button_rotate_clockwise.when_pressed = lambda: self.tetris.rotate_tetromino_clockwise()

        self.button_rotate_counter_clockwise = Button(22)
        self.button_rotate_counter_clockwise.when_pressed = lambda: self.tetris.rotate_tetromino_counter_clockwise()

        self.button_move_down_faster = Button(6)

        self.timer_interval = 0.5

        self.main()

    def main(self):
        print("game start")
        while self.tetris.run():
            if self.button_move_down_faster.is_pressed:
                self.tetris.move_tetromino_down()
                self.tetris.move_tetromino_down()
                self.tetris.move_tetromino_down()
                self.tetris.move_tetromino_down()
            self.draw_fields_to_matrix()
            time.sleep(self.timer_interval)  # this sets how fast the game will run

        print("game over")
        score = "   score: {}".format(self.tetris.get_score())
        print(score)
        print("press the reset button to restart")

        virtual = viewport(self.device, width=200, height=100)
        with canvas(virtual) as draw:
            text(draw, (0, 0), score, fill="white", font=proportional(LCD_FONT))
        while True:
            for offset in range(len(score) * 5):
                virtual.set_position((offset, 0))
                time.sleep(0.1)

    def get_base_play_field(self):
        base_play_field = []
        for row in range(self.device.width):
            base_play_field.append([])
            for cell in range(self.device.height):
                base_play_field[row].append(0)
        return base_play_field

    def draw_fields_to_matrix(self):
        with canvas(self.device) as draw:
            for x, row in enumerate(self.tetris.get_play_field()):
                for y, cell in enumerate(row):
                    if cell == 1:
                        draw.point((x, y), fill="white")

    def decrease_timer_interval(self):
        self.timer_interval *= 0.9


application = PiTetrisApplication()
