##############################################################################
# This script ingests messages from a given Kafka input topic and transforms
# message timestamps from local timezone to UTC and publishes the updated
# messages to another output topic.
##############################################################################
# Submitted by Basant Khati
##############################################################################
from json import JSONDecodeError
from kafka import KafkaConsumer, KafkaProducer
from kafka.errors import KafkaError
from datetime import datetime
from dateutil import tz
import json
import os

INPUT_TOPIC = os.environ.get('KAFKA_INPUT_TOPIC')
OUTPUT_TOPIC = os.environ.get('KAFKA_OUTPUT_TOPIC')
KAFKA_BROKER_URL = os.environ.get('KAFKA_BROKER_URL')

to_zone = tz.tzutc()
from_zone = tz.tzlocal()


def write_message_to_topic(json_msg):
    try:
        producer = KafkaProducer(
                    bootstrap_servers=KAFKA_BROKER_URL,
                    value_serializer=lambda value: json.dumps(value).encode(),
                )
        producer.send(OUTPUT_TOPIC,
                      json_msg)

    except KafkaError as e:
        print(f'Kafka Producer - Exception during publishing message - {e}')
    except Exception as e:
        print(f'exception- {e}')


def read_messages_from_topic():
    try:
        consumer = KafkaConsumer(
                        INPUT_TOPIC,
                        group_id='group2',
                        bootstrap_servers=KAFKA_BROKER_URL,
                    )
        # Read messages from consumer
        for msg in consumer:
            try:
                json_str = json.loads(msg.value)

            except JSONDecodeError as e:
                print(f'JSON error in loading message - {e}; message - {msg}')
                continue

            if process_message(json_str) is not None:
                write_message_to_topic(json_str)

    except KafkaError as e:
        print(f'Kafka consumer - Exception during consuming message - {e}; '
              f'message - {msg}')

    except JSONDecodeError as e:
        print(f'JSONDecodeError - error loading message - {e}; '
              f'message - {msg}')

    except Exception as e:
        print(f'exception {e}; message - {msg}')


# read messages from input topic and process them
# e.g. convert to utc
def process_message(json_mesg):
    transformed_msg = None
    try:
        # check if required key exists
        if "myTimestamp" in json_mesg:
            local = datetime.strptime(json_mesg["myTimestamp"], '%Y-%m-%dT%H:%M:%S%z')
            json_mesg["myTimestamp"] = datetime.strftime(local.astimezone(to_zone),
                                                 '%Y-%m-%dT%H:%M:%S%z')
            transformed_msg = json_mesg
            return transformed_msg

    except ValueError as e:
        print(f'ValueError - {e}; message - {json_mesg}')

    except Exception as e:
        print(f'exception {e}; message - {json_mesg}')

    return transformed_msg


if __name__ == "__main__":
    read_messages_from_topic()
