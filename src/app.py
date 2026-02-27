import adafruit_logging as logging
import time

from sensor import Measurement, Sensor

logger = logging.getLogger("main")

DISPLAY_PERIOD = 5.0
MEASURE_PERIOD = 30.0

class App:
    t_next_display: float
    t_next_measure: float
    latest_measurement: Measurement
    failed_measures: int

    def __init__(self):
        self.t_next_display = time.monotonic()
        self.t_next_measure = time.monotonic()
        self.sensor = Sensor()
        self.failed_measures = 0

    def run(self):
        while True:
            now = time.monotonic()
            if now >= self.t_next_display:
                self.latest_measurement = self._measure()
                self.t_next_display = self.t_next_display + MEASURE_PERIOD
            time.sleep(0.01)

    def _measure(self):
        try:
            measurement = self.sensor.read()
            self.failed_measures = 0
            return measurement
        except Exception as e:
            logger.error('Failed to read Sensor: ' + e)
            self.failed_measures = self.failed_measures + 1
            return Measurement.Empty()
