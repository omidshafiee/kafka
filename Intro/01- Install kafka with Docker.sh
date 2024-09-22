docker-compose up -d

docker-compose ps

docker-compose down -v




######################################################################
# use kafka cli container

kafka-topics.sh --list --bootstrap-server 10.0.0.120:9092



docker exec -it cli-tools
  --bootstrap-server broker0:29092,broker2:29093,broker2:29094
	kafka-topics --list
	
	
# Create Topic
kafka-topics --bootstrap-server broker0:29092,broker2:29093,broker2:29094 \
	--create --topic people --partitions 2 --replication-factor 2
	
# Get info about topic
kafka-topics  --bootstrap-server broker0:29092,broker2:29093,broker2:29094  --describe --topic people
	

	
# Delete Topic
kafka-topics --bootstrap-server broker0:29092,broker2:29093,broker2:29094 \
	--delete --topic people 