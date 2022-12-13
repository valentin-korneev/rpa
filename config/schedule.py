from schedule import every, run_pending
from .cron import load_cron
from time import sleep
from utils.environ import env
from .redis import redis


redis.delete('ODR-SCRIPTS')
redis.delete('ODR-JOBS')
every(env('SCHEDULE_EVERY', 30)).seconds.do(load_cron)

while True:
    run_pending()
    sleep(1)