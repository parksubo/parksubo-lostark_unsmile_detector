from kafka import KafkaConsumer, KafkaProducer
from elasticsearch import Elasticsearch
import json

# Kafka
brokers = ["localhost:9091", "localhost:9092", "localhost:9093"]

UNSMILE_DATA_TOPIC = "unsmile_data"

consumer = KafkaConsumer(UNSMILE_DATA_TOPIC, bootstrap_servers = brokers)
producer = KafkaProducer(bootstrap_servers = brokers)

# elasticsearch
# es = Elasticsearch(["localhost:9200"])

for message in consumer:
    msg = json.loads(message.value.decode())
    print(msg)

    
    