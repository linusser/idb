import board
import time
import tm1637lib

display = tm1637lib.Grove4DigitDisplay(board.D9, board.D10) # nRF52840 D9, D10, Grove D4

colon = False

msg = 'CO2 1213PPnm    tTEnmP 25C    rH 50ö/o'
# Plus 4 für 3 leerzeichen am Start und 1 damit am schluss 4 leere angezeigt werden
len_msg = len(msg) + 4
msg = '   '+ msg + '    '
while True:
    display.set_colon(colon)
    for i in range(len_msg):
        display.show(msg[i:i+4])
        time.sleep(0.5)