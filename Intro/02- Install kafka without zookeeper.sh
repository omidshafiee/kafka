wget https://archive.apache.org/dist/kafka/3.0.0/kafka_2.13-3.0.0.tgz

tar xzf kafka_2.12-3.0.0.tgz
mv kafka_2.12-3.0.0  kafka

#KAFKA_HOME
export KAFKA_HOME=/home/bi/kafka/
export PATH=$KAFKA_HOME/bin/:$PATH

kafka-storage.sh random-uuid

# uuid = 9CmPsWypQ8OwedpO0F0SKw

kafka-storage.sh format -t <uuid>  -c /home/bi/kafka/config/kraft/server.properties


kafka-server-start.sh -daemon kafka/config/kraft/server.properties

kafka-topic.sh

# Topics list:
kafka-topics.sh --bootstrap-server 10.0.0.120:9092  --list

# Create Producer:

kafka-console-producer.sh --bootstrap-server 10.0.0.120:9092  --topic transaction.basic.python 


{"name":"Mehdi", "title":"Chief Data Scientist"}
{"name":"Majid", "title":"Chief Financial Analyst"}
{"name":"Reza", "title":"Chief Biological Analyst"}
{"name":"Alvan", "title":"Chief Motivator"}

# producer with keys
kafka-console-producer.sh --bootstrap-server 10.0.0.120:9092  --topic transaction.basic.python \ --property "parse.key=true" --property "key.separator=|"

Data Scientist|{"name":"Mehdi", "title":"Chief Data Scientist"}

# Create Consumer:
kafka-console-consumer.sh --bootstrap-server 10.0.0.120:9092  --topic transaction.basic.python \
	--from-beginning --property "print.key=true"


