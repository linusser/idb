import time
import board
import busio
from digitalio import DigitalInOut

from adafruit_esp32spi import adafruit_esp32spi
import adafruit_connection_manager
import adafruit_minimqtt.adafruit_minimqtt as MQTT

from secrets import secrets

# AirLift FeatherWing pins
esp32_cs = DigitalInOut(board.D13)
esp32_ready = DigitalInOut(board.D11)
esp32_reset = DigitalInOut(board.D12)

spi = busio.SPI(board.SCK, board.MOSI, board.MISO)
esp = adafruit_esp32spi.ESP_SPIcontrol(spi, esp32_cs, esp32_ready, esp32_reset)

print("WiFi connecting...")
esp.connect_AP(secrets["ssid"], secrets["password"])
print("WiFi OK, IP:", esp.pretty_ip(esp.ip_address))

pool = adafruit_connection_manager.get_radio_socketpool(esp)

mqtt = MQTT.MQTT(
    broker=secrets["mqtt_broker"],
    port=secrets["mqtt_port"],     # <-- custom port here
    socket_pool=pool,
    is_ssl=False,                  # no TLS
)

print("MQTT connecting...")
mqtt.connect()
print("MQTT OK")

topic = "fhnw/test/out"
i = 0

while True:
    mqtt.loop()
    msg = f"msg {i}"
    mqtt.publish(topic, msg)
    print("published:", msg)
    i += 1
    time.sleep(3)