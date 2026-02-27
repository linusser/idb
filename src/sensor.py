import time
import board
import busio
import adafruit_scd30
import json

class Sensor():
    def __init__(self):
        self.i2c = busio.I2C(board.SCL, board.SDA, frequency=50000)
        self.scd30 = adafruit_scd30.SCD30(self.i2c)

    def read(self):
        if self.scd30.data_available:
            measurement = Measurement(
                self.scd30.CO2,
                self.scd30.temperature,
                self.scd30.relative_humidity
            )
            return measurement
        else:
            raise Exception('scd30 Data unavailable')

class Measurement:
    # todo: add datetime
    def __init__(self, co2, temperature, relative_humidity):
        self.co2 = float(co2)
        self.temperature = float(temperature)
        self.relative_humidity = float(relative_humidity)

    def to_dict(self):
        return {
            "CO2": self.co2,
            "temperature": self.temperature,
            "relative_humidity": self.relative_humidity,
        }

    def to_json(self):
        return json.dumps(self.to_dict())

    def rounded(self):
        return round(self.co2), round(self.temperature), round(self.relative_humidity)

    @staticmethod
    def Empty():
        return Measurement(None, None, None)