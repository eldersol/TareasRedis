from celery import Celery
import redis

# Connect to our Redis instance
redis_instance = redis.StrictRedis(host='tareasredis_cache_1',
                                   port=6379, decode_responses=True)

app = Celery(
    'postman',
    broker='pyamqp://user:bitnami@rabbitmq',
    backend='rpc://user:bitnami@rabbitmq',
)

@app.task(name='addTask')
def add(x, y, operador):
    key = "llave"
    redis_instance.set(key, "valor")
    return x + y
