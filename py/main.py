import os
import uuid
from typing import List

from dotenv import load_dotenv
from faker import Faker
from kafka import KafkaAdminClient
from kafka.admin import NewTopic
from kafka.errors import TopicAlreadyExistsError
from kafka.producer import KafkaProducer

from commands import CreateTransactionCommand
from entities import Transaction

from fastapi import FastAPI

load_dotenv(verbose=True)

app = FastAPI()


@app.on_event('startup')
async def startup_event():
    client = KafkaAdminClient(bootstrap_servers=os.environ['BOOTSTRAP_SERVERS'])
    topic = NewTopic(name=os.environ['TOPIC_TRANSACTION_BASIC_NAME'],
                     num_partitions=int(os.environ['TOPIC_TRANSACTION_BASIC_PARTITIONS']),
                     replication_factor=int(os.environ['TOPIC_TRANSACTION_BASIC_REPLICAS']))

    try:
        client.create_topics([topic])

    # except TopicAlreadyExistsError as e:
    #     logging.exception("Topic Already exist")

    except Exception as e:
        print(f'Failed to create topic: {e}')

    finally:
        client.close()
    # return {"message": os.getenv('TOPIC_TRANSACTION_BASIC_NAME')}


def create_producer():
    return KafkaProducer(bootstrap_servers=os.environ['BOOTSTRAP_SERVERS'])


@app.post('/api/tran', status_code=201, response_model=list[Transaction])
async def create_transactions(cmd: CreateTransactionCommand):
    transaction_list: list[Transaction] = []

    faker = Faker()
    producer = create_producer()

    for _ in range(cmd.count):
        tran_obj = Transaction(id=uuid.uuid4(),
                               date=faker.date(),
                               amount=faker.currency(),
                               customer=faker.name()
                               )
        print(f'{tran_obj.id} - {tran_obj.date}')
        transaction_list.append(tran_obj)
        producer.send(topic=os.environ['TOPIC_TRANSACTION_BASIC_NAME'],
                      key=tran_obj.customer.lower().replace(r's+', '-').encode('utf-8'),
                      value=tran_obj.json().encode('utf-8'))

    producer.flush()

    return transaction_list

# create_transactions()
