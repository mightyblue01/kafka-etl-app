import json
from _pytest.fixtures import fixture

from process_kafka_msgs import process_message


@fixture
def sample_json_data():
    with open("resources/sample_messages.txt") as f:
        json_msgs = []
        try:
            for line in f:
                json_msgs.append(json.loads(line))
        except FileNotFoundError:
            print(f'Input sample file not found - {FileNotFoundError}')
        except Exception as e:
            print(f'JSONDecodeError - error loading message - {e}')
    return json_msgs


def test_total_messages_count(sample_json_data):
    assert len(sample_json_data) == 6


def test_json_message_loaded_as_expected(sample_json_data):
    assert "{'myKey': 11, 'myTimestamp': '2022-03-01T09:11:04+01:00'}" \
           == str(sample_json_data[0])


def test_process_message_method_for_valid_message(sample_json_data):
    expected_msg = {"myKey": 12, "myTimestamp": "2022-03-01T08:12:08+0000",
                        "key2": "2022-03-01"}
    assert expected_msg == process_message(sample_json_data[2])


def test_process_message_method_for_invalid_timestamp(sample_json_data):
    assert None is process_message(sample_json_data[4])


def test_process_message_method_for_invalid_message():
    bad_message_format = "invalid message"
    assert None is process_message(bad_message_format)
