from celery import Celery
import redis
import uuid

# Connect to our Redis instance
redis_instance = redis.StrictRedis(host='tareasredis_cache_1',
                                   port=6379, decode_responses=True)

app = Celery(
    'task',
    broker='pyamqp://user:bitnami@rabbitmq',
    #backend='rpc://user:bitnami@rabbitmq',
)

@app.task(name='addTask')
def add(numero1, numero2, operador):
    resultado = 0

    if operador == 'suma':
        resultado = int(numero1) + int(numero2)
    elif operador == 'resta':
        resultado = int(numero1) - int(numero2)
    elif operador == 'multiplicacion':
        resultado = int(numero1)*int(numero2)
    elif operador == 'division':
        resultado = int(numero1)/int(numero2)

    key = str(uuid.uuid4())
    redis_instance.hset(key, "numero1", numero1)
    redis_instance.hset(key, "numero2", numero2)
    redis_instance.hset(key, "resultado", resultado)
    return key


@app.task(name='updateTask')
def update():
    print("Actualizar base de datos")
    return None