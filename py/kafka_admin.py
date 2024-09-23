import os
import logging
from datetime import datetime as dt
from dotenv import load_dotenv
from fastapi import FastAPI

from kafka import KafkaAdminClient
from kafka.admin import NewTopic, ConfigResource, ConfigResourceType
from kafka.errors import TopicAlreadyExistsError

# Kafka configuration
# config = {
#     'bootstrap.servers': '10.0.0.120:9092'  # Update with your Kafka broker(s)
# }

load_dotenv(verbose=True)

# get environment variables
print('Topic Name: ', f"{os.environ['TOPIC_TRANSACTION_BASIC_NAME']}")
print(f'Partitions: ', int(os.environ['TOPIC_TRANSACTION_BASIC_PARTITIONS']))
print('Replica Factors: ', int(os.environ['TOPIC_TRANSACTION_BASIC_REPLICAS']))
print('Topic Name: ', os.getenv('TOPIC_TRANSACTION_BASIC_NAME'))
print('=' * 100)


# Create event handler

def create_topic():
    client = KafkaAdminClient(bootstrap_servers=os.environ['BOOTSTRAP_SERVERS'])

    topic = NewTopic(name=os.environ['TOPIC_TRANSACTION_BASIC_NAME'],
                     num_partitions=int(os.environ['TOPIC_TRANSACTION_BASIC_PARTITIONS']),
                     replication_factor=int(os.environ['TOPIC_TRANSACTION_BASIC_REPLICAS']))

    try:
        client.create_topics([topic], validate_only=False)
        print('Topic created successfully!')
        print('=' * 100)

    # except TopicAlreadyExistsError as e:
    #     logging.exception("Topic Already exist")

    except Exception as e:
        print(f'Failed to create topic: {e}')

    finally:
        client.close()


# return {"message": os.getenv('TOPIC_TRANSACTION_BASIC_NAME')}


def create_kafka_topics(broker, topic_list):
    # Initialize Kafka Admin Client
    admin_client = KafkaAdminClient(
        bootstrap_servers=broker,
        client_id='my_kafka_client'
    )

    # Prepare NewTopic objects
    topics = [NewTopic(name=topic, num_partitions=1, replication_factor=1) for topic in topic_list]

    # Create topics
    try:
        admin_client.create_topics(new_topics=topics, validate_only=False)
        print(f"Topics created: {', '.join(topic_list)}")
    except Exception as e:
        print(f"Failed to create topics: {e}")
        print()
        print('=' * 100)

    finally:
        # Close the admin client
        admin_client.close()


def update_kafka_config():
    client = KafkaAdminClient(bootstrap_servers=os.environ['BOOTSTRAP_SERVERS'])

    cfg_resource_update = ConfigResource(
        ConfigResourceType.TOPIC,
        os.environ['TOPIC_TRANSACTION_BASIC_NAME'],
        configs={'retention.ms': 360000}
    )
    client.alter_configs([cfg_resource_update])
    print('Config has updated successfully!')
    print('=' * 100)
    client.close()


def hello_world():
    print("Hello World")

    # return {"message": os.getenv('TOPIC_TRANSACTION_BASIC_NAME')}


create_topic()
update_kafka_config()

# broker = '10.0.0.120:9092'  # Replace with your Kafka broker
# topic_list = ["topic1", "topic2", "topic3"]  # Replace with your topics
# create_kafka_topics(broker, topic_list)
