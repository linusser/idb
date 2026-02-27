import time
import board
import busio
import adafruit_scd30
import tm1637lib

i2c = busio.I2C(board.SCL, board.SDA, frequency=50000)
display = tm1637lib.Grove4DigitDisplay(board.D9, board.D10)  # nRF52840 D9, D10, Grove D4
scd30 = adafruit_scd30.SCD30(i2c)

while True:
    if scd30.data_available:
        msg = f'CO2 {round(scd30.CO2)}PPnm    tTEnmP {round(scd30.temperature)}C    rH {round(scd30.relative_humidity)}ö/o'
        # Plus 4 für 3 leerzeichen am Start und 1 damit am schluss 4 leere angezeigt werden
        len_msg = len(msg) + 4
        msg = '   ' + msg + '    '

        display.set_colon(False)
        for i in range(len_msg):
            display.show(msg[i:i + 4])
            time.sleep(0.5)
    time.sleep(5)
