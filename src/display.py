import board
import tm1637lib
import time

from sensor import Measurement

class Display:
    def __init__(self):
        self.display = tm1637lib.Grove4DigitDisplay(board.D9, board.D10)  # nRF52840 D9, D10, Grove D4

    def display_raw_text(self, msg):
        for i in range(msg):
            self.display.show(msg[i:i + 4])
            time.sleep(0.33)

    def display_measurement(self, measurement):
