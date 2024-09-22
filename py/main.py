import os
import logging

from dotenv import load_dotenv
from fastapi import FastAPI

from kafka import KafkaAdminClient
from kafka.admin import NewTopic
from kafka.errors import TopicAlreadyExistsError

# Kafka configuration
# config = {
#     'bootstrap.servers': '10.0.0.120:9092'  # Update with your Kafka broker(s)
# }

load_dotenv(verbose=True)

# print(os.environ['TOPIC_TRANSACTION_BASIC_NAME'])
# print(int(os.environ['TOPIC_TRANSACTION_BASIC_PARTITIONS']))
# print(int(os.environ['TOPIC_TRANSACTION_BASIC_REPLICAS']))
# print(os.getenv('TOPIC_TRANSACTION_BASIC_NAME'))


app = FastAPI()


# Create event handler
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


@app.get('/hello-world')
async def hello_world():
    return {"message": "Helo World"}
    # return {"message": os.getenv('TOPIC_TRANSACTION_BASIC_NAME')}
