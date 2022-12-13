from logging import basicConfig, getLevelName, DEBUG, getLogger
from utils.environ import env


basicConfig(
    filename=env('LOGGING_FILENAME', './logs/app.log'),
    encoding=env('LOGGING_ENCODING', 'utf-8'),
    level=getLevelName(env('LOGGING_LEVEL', getLevelName(DEBUG)).upper())
)

logging = getLogger()
logging.info('[logging]')