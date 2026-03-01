import time

import board
import busio
from digitalio import DigitalInOut
import adafruit_logging as logging

from adafruit_esp32spi import adafruit_esp32spi
import adafruit_connection_manager
import adafruit_minimqtt.adafruit_minimqtt as MQTT

from secrets import secrets

logger = logging.getLogger("main")
logger.setLevel(logging.INFO)

class Network():
    def __init__(self):
        self._init_network()
        self._connect_wifi()
        self._init_mqtt()

    def _init_network(self):
        esp32_cs = DigitalInOut(board.D13)
        esp32_ready = DigitalInOut(board.D11)
        esp32_reset = DigitalInOut(board.D12)

        self._spi = busio.SPI(board.SCK, board.MOSI, board.MISO)
        self._esp = adafruit_esp32spi.ESP_SPIcontrol(self._spi, esp32_cs, esp32_ready, esp32_reset)


    def _connect_wifi(self):
        logger.info('WiFi connecting...')
        self._esp.connect_AP(secrets["ssid"], secrets["password"])
        logger.info(f"WiFi OK, IP: {self._esp.pretty_ip(self._esp.ip_address)}")

    def _init_mqtt(self):
        self._pool = adafruit_connection_manager.get_radio_socketpool(self._esp)
        self._mqtt = MQTT.MQTT(
            broker=secrets["mqtt_broker"],
            port=secrets["mqtt_port"],
            socket_pool=self._pool,
            is_ssl=False
        )

        logger.info("MQTT connecting...")
        self._mqtt.connect()
        logger.info("MQTT OK")

    def publish(self, msg, topic=secrets["mqtt_topic"]):
        self._mqtt.publish(topic, msg)
        logger.info(f'Published: {msg} to {topic}')

    def loop(self):
        self._mqtt.loop()

    def get_secure_time(self):
        try:
            raw_tuple = self._esp.get_time()

            utc_seconds = raw_tuple[0]
            local_seconds = utc_seconds + 3600

            t = time.localtime(local_seconds)
            timestamp = "{:04}-{:02}-{:02} {:02}:{:02}:{:02}".format(
                t[0], t[1], t[2], t[3], t[4], t[5]
            )
            return timestamp
        except Exception as e:
            logger.error(f"Couldn't fetch time: {e}")
            return None




