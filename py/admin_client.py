from kafka.admin import KafkaAdminClient, NewTopic


# Kafka configuration
def create_kafka_topic():
    print('create_kafka_topic')
    config = {
        'bootstrap.servers': 'localhost:9092'  # Kafka broker address
    }

    # Create an AdminClient instance
    admin_client = KafkaAdminClient(bootstrap_servers='10.0.0.120:9092')

    # Define the topic parameters
    topic_name = 'my_new_topic'
    num_partitions = 3
    replication_factor = 1

    # Create a NewTopic object
    topic = NewTopic(name=topic_name, num_partitions=num_partitions, replication_factor=replication_factor)

    # Call create_topics and pass the topic object
    topic_creation = admin_client.create_topics([topic])

    # Wait for the operation to complete and handle errors
    try:
        result = topic_creation[topic_name].result()  # Will raise an exception if creation fails
        print(f"Topic '{topic_name}' created successfully.")

    except Exception as e:
        print(f"Failed to create topic: {e}")


# Execute the function to create the topic
create_kafka_topic()
