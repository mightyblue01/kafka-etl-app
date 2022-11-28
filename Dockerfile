FROM python:3.8.15-slim

LABEL maintainer="BasantKhati"

RUN apt update && \
    apt install --no-install-recommends -y build-essential gcc && \
    apt clean && rm -rf /var/lib/apt/lists/*

WORKDIR /usr/src

# Install dependencies
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy source code
COPY process_kafka_msgs.py /usr/src/process_kafka_msgs.py

#CMD ["python3", "/usr/src/process_kafka_msgs.py"]
CMD ["python3", "process_kafka_msgs.py"]

