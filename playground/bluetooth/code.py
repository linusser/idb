import time
from adafruit_ble import BLERadio
from adafruit_ble.advertising.standard import ProvideServicesAdvertisement
from adafruit_ble.services.nordic import UARTService
import _bleio

print("BLE ok")

ble = BLERadio()
uart = UARTService()
advertisement = ProvideServicesAdvertisement(uart)

print("BLE UART startet, advertising ...")
print(ble.name)

while True:
    ble.start_advertising(advertisement)
    while not ble.connected:
        time.sleep(0.1)

    print("Verbunden")

    while ble.connected:
        data = uart.read(32)  # bis 32 Bytes lesen
        if data:
            text = data.decode("utf-8", errors="replace")
            print("RX:", text)
            uart.write(data)  # Echo zurück
        time.sleep(0.01)

    print("Getrennt")