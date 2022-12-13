from utils.environ import env
from redis import ConnectionPool, Redis


redis = Redis(
    connection_pool=ConnectionPool(
        host=env('REDIS_HOST', 'localhost'),
        port=env('REDIS_PORT', 6379),
        username=env('REDIS_USERNAME'),
        password=env('REDIS_PASSWORD'),
        db=env('REDIS_DB', 0),
    )
)