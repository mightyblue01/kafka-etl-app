# start kafka producer container and push messages from input file sample_messages.txt
docker exec --interactive kafka-etl-app_broker_1  kafka-console-producer --bootstrap-server broker:9092 --topic input_topic < resources/sample_messages.txt
echo "published messages to input_topic"

# messages published in input_topic will be processed by kafka etl app and published to output_topic
# we now read those processed messages from output_topic and dump in a file processed_messages.jsonl
docker exec  --interactive kafka-etl-app_broker_1 kafka-console-consumer --bootstrap-server broker:9092 --topic output_topic --from-beginning --group groupa --timeout-ms 5000 > processed_messages.txt

echo "captured processed messages in processed_messages.txt file"
exit 
