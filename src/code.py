import time

from app import App
import adafruit_logging as logging

logger = logging.getLogger("main")
logger.setLevel(logging.INFO)

# file_handler = logging.FileHandler("/log.txt", mode="a")
# logger.addHandler(file_handler)

def run():
    try:
        app = App()
        logger.info('App gestartet')
        app.run()
    except Exception as e:
        logger.error(f'App unerwartet geschlossen: {e}')
        time.sleep(10)
        run()

run()

