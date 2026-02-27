import time
import board
import busio
import adafruit_scd30

i2c = busio.I2C(board.SCL, board.SDA, frequency=50000)
scd30 = adafruit_scd30.SCD30(i2c)

while True:
    if scd30.data_available:
        print("CO2 ppm:", scd30.CO2)
        print("Temp C:", scd30.temperature)
        print("RH %:", scd30.relative_humidity)
        print()
    time.sleep(0.5)