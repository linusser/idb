import adafruit_logging as logging
import time

from sensor import Measurement, Sensor
from display import Display
from network import Network

logger = logging.getLogger("main")
logger.setLevel(logging.INFO)

DISPLAY_PERIOD = 30.0
MEASURE_PERIOD = 60.0
PUBLISH_PERIOD = 60.0

class App:

    def __init__(self):
        self.t_next_display = time.monotonic()
        self.t_next_measure = time.monotonic()
        self.t_next_publish = time.monotonic()
        self.latest_measurement = Measurement.Empty()
        self.sensor = Sensor()
        self.display = Display()
        self.network = Network()
        self.failed_measures = 0

    def run(self):
        while True:
            now = time.monotonic()
            self._keep_connection_alive()

            if now >= self.t_next_measure:
                self.latest_measurement = self._measure()
                self.t_next_measure = self.t_next_measure + MEASURE_PERIOD

            if now >= self.t_next_display:
                self._display()
                self.t_next_display = self.t_next_display + DISPLAY_PERIOD

            if now >= self.t_next_publish:
                self._publish()
                self.t_next_publish = self.t_next_publish + PUBLISH_PERIOD

            time.sleep(0.01)

    def _measure(self):
        try:
            timestamp = self.network.get_secure_time()
            measurement = self.sensor.read(timestamp)
            logger.info('Took measurement with sensor')
            self.failed_measures = 0
            return measurement
        except Exception as e:
            logger.error(f'Failed to read Sensor: {e}')
            self.failed_measures = self.failed_measures + 1
            return Measurement.Empty()

    def _display(self):
        if self.latest_measurement.has_data():
            self.display.display_measurement(self.latest_measurement)
            return

        if self.failed_measures >= 3:
            self.display.display_sensor_error()
            return

    def _publish(self):
        try:
            if self.latest_measurement.has_data() and self.failed_measures == 0:
                self.network.publish(self.latest_measurement.to_json())
        except Exception as e:
            logger.error(f'Failed to publish: {e}')
            self.display.display_network_error()
            # Handle Network

    def _keep_connection_alive(self):
        self.network.loop()
