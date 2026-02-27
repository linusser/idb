import time
import board
import digitalio
import tm1637lib

display = tm1637lib.Grove4DigitDisplay(board.D9, board.D10) # nRF52840 D9, D10, Grove D4

btn = digitalio.DigitalInOut(board.SWITCH)
btn.direction = digitalio.Direction.INPUT
btn.pull = digitalio.Pull.UP  # typisch: nicht gedrückt=True, gedrückt=False

while True:
    if not btn.value:
        display.show(" GAY")
        display.set_colon(False)
        time.sleep(5)
        display.clear()
    time.sleep(0.05)