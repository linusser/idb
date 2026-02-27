import board
import tm1637lib
import time

from sensor import Measurement

class Display:
    def __init__(self):
        self.display = tm1637lib.Grove4DigitDisplay(board.D9, board.D10)  # nRF52840 D9, D10, Grove D4
        self.display.set_colon(False)


    def display_raw_text(self, msg):
        # Plus 4 für 3 leerzeichen am Start und 1 damit am schluss 4 leere angezeigt werden
        len_msg = len(msg) + 4
        msg = '   ' + msg + '    '

        for i in range(len_msg):
            self.display.show(msg[i:i + 4])
            time.sleep(0.33)

    def display_measurement(self, measurement):
        co2, temp, rh = measurement.rounded()
        msg = f'CO2 {co2}PPnm    tTEnmP {temp}C    rH {rh}ö/o'
        self.display_raw_text(msg)

    def display_network_error(self):
        msg = 'Error no nEtTuworK ConnECtTIon'
        for i in range(3):
            self.display_raw_text(msg)
            time.sleep(5)

    def display_network_error(self):
        msg = 'Error no SEnSor DAtTA'
        for i in range(3):
            self.display_raw_text(msg)
            time.sleep(5)