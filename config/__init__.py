from dotenv import load_dotenv


load_dotenv()


from .logging import logging
from .redis import redis


try:
    redis.ping()
except Exception as ex:
    logging.error('[Redis]: Invalid connect')
    raise ex


import config.schedule
