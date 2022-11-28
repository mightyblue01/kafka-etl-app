from kafka import KafkaConsumer, KafkaProducer
import sys
import os
from datetime import datetime
from dateutil import tz
import json

INPUT_TOPIC = os.environ.get('KAFKA_INPUT_TOPIC')
OUTPUT_TOPIC = os.environ.get('KAFKA_OUTPUT_TOPIC')
KAFKA_BROKER_URL = os.environ.get('KAFKA_BROKER_URL')

to_zone = tz.tzutc()
from_zone = tz.tzlocal()


def write_message_to_output_topic(json_msg, output_topic):
    producer = KafkaProducer(
                bootstrap_servers=KAFKA_BROKER_URL,
                value_serializer=lambda value: json.dumps(value).encode(),
            )
    producer.send(output_topic,
                  json_msg)


# read messages from input topic and process them
# e.g. convert to utc
def process_messages(input_topic, output_topic):
    # Initialize consumer variable
    #print(f'input topic {input_topic}, output topic {output_topic}')
    consumer = KafkaConsumer(
                    input_topic,
                    group_id='group2',
                    bootstrap_servers=KAFKA_BROKER_URL,
                    api_version=(2, 0, 2)
                )

    # Read messages from consumer
    for msg in consumer:
        json_str = json.loads(msg.value)
        json_msg = {}

        for key, val in json_str.items():
            if key == "myTimestamp":
                # check for msgs with empty value as provided in on of the
                # samples, further checks can be added here to handle other
                # types of malformed messages
                if val != '':
                    local = datetime.strptime(val, '%Y-%m-%dT%H:%M:%S%z')
                    json_msg[key] = datetime.strftime(local.astimezone(to_zone),
                                            '%Y-%m-%dT%H:%M:%S%z')
                else:
                    print('dropping msg with empty value where key is {key}')
                    continue
            else:
                json_msg[key] = val
        # check if final message has both the keys (myKey, myTimestamp)
        if len(json_msg) == 2:
            write_message_to_output_topic(json_msg, output_topic)

    # Terminate the script
    #sys.exit()


if __name__ == "__main__":
    process_messages(INPUT_TOPIC, OUTPUT_TOPIC)
