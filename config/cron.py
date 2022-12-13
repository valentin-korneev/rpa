from .logging import logging
from inspect import stack
from utils.environ import env
from os.path import exists
from json import loads, dumps
from .redis import redis
from hashlib import sha256
from schedule import every, cancel_job


_crons = {}


def _check_scripts(scripts, job_scripts):
    return set(job_scripts) == (set(job_scripts) & set(scripts))


def worker(id):
    print(id)


def load_cron():
    try:
        r_scripts = loads(redis.get('ODR-SCRIPTS') or '{}')
        r_jobs = loads(redis.get('ODR-JOBS') or '{}')

        path = env('CRONTAB_SCRIPTS')
        if not exists(path):
            raise FileNotFoundError(f'{path} not found (CRONTAB_SCRIPTS)')

        with open(path) as scripts:
            data = loads(scripts.read())
            r_keys = r_scripts.keys()
            d_keys = set()
            for item in data:
                id = item.get('id')
                sha = sha256(dumps(item).encode("utf-8")).hexdigest()
                item['hash'] = sha
                d_keys.add(id)
                if id not in r_scripts or r_scripts.get(id).get('hash') != sha:
                    r_scripts[id] = item
            r_keys -= d_keys
            for k in r_keys:
                del r_scripts[k]
            

        path = env('CRONTAB_JOBS')
        if not exists(path):
            raise FileNotFoundError(f'{path} not found (CRONTAB_JOBS)')

        with open(path, 'r') as jobs:
            data = loads(jobs.read())
            r_keys = r_jobs.keys()
            d_keys = set()
            for item in data:
                id = item.get('id')
                if _check_scripts(r_scripts, item.get('scripts')):
                    sha = sha256(dumps(item).encode("utf-8")).hexdigest()
                    item['hash'] = sha
                    d_keys.add(id)
                    if id not in r_jobs or r_jobs.get(id).get('hash') != sha:
                        r_jobs[id] = item
                        if id in _crons:
                            cancel_job(_crons[id])
                        _crons[id] = every(1).seconds.do(worker, id)
                else:
                    logging.warning(f'Job {id} has invalid script')
            r_keys -= d_keys
            for k in r_keys:
                del r_jobs[k]
                if k in _crons:
                    cancel_job(_crons[k])
                    del _crons[k]

        redis.set('ODR-SCRIPTS', dumps(r_scripts))
        redis.set('ODR-JOBS', dumps(r_jobs))
    except Exception as ex:
        logging.error(f'[{stack()[0].filename}] {ex}')