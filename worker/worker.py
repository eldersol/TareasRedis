from celery import Celery
import redis
import uuid
import psycopg2

# Connect to our Redis instance
redis_instance = redis.StrictRedis(host='tareasredis_cache_1',
                                   port=6379, decode_responses=True)

app = Celery(
    'task',
    broker='pyamqp://user:bitnami@rabbitmq',
    backend='rpc://user:bitnami@rabbitmq',
)

@app.task(name='addTask')
def add(numero1, numero2, operador):
    resultado = 0

    if operador == 'suma':
        resultado = int(numero1) + int(numero2)
    elif operador == 'resta':
        resultado = int(numero1) - int(numero2)
    elif operador == 'multi':
        resultado = int(numero1)*int(numero2)
    elif operador == 'div':
        resultado = int(numero1)/int(numero2)

    key = str(uuid.uuid4())
    redis_instance.hset(key, "numero1", numero1)
    redis_instance.hset(key, "numero2", numero2)
    redis_instance.hset(key, "resultado", resultado)

    return key


@app.task(name='updateTask')
def update(redis_id, operacion_id):
    redis_dic = redis_instance.hgetall(str(redis_id))
    resultado = redis_dic['resultado']

    try:
        connection = psycopg2.connect(user="postgres",
                                      password="postgres",
                                      host="db_postgres",
                                      port="5432")
        cursor = connection.cursor()
        postgres_insert_query = "UPDATE operacion_operacion SET resultado =" + str(resultado) + "WHERE id=" + str(operacion_id)

        cursor.execute(postgres_insert_query)
        connection.commit()

    except (Exception, psycopg2.Error) as error:
        print("Error!!!!", error)

    finally:
        if connection:
            cursor.close()
            connection.close()


    return None



