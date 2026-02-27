from app import App
import adafruit_logging as logging

logger = logging.getLogger("main")
logger.setLevel(logging.INFO)

# file_handler = logging.FileHandler("/log.txt", mode="a")
# logger.addHandler(file_handler)

try:
    app = App()
    logger.info('App gestartet')
    app.run()
except Exception as e:
    logger.error('App unerwartet geschlossen:', e)

