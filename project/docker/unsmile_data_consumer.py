from kafka import KafkaConsumer, KafkaProducer
from elasticsearch import Elasticsearch

import json
import datetime
import pytz

# Kafka
brokers = ["localhost:9091", "localhost:9092", "localhost:9093"]

UNSMILE_DATA_TOPIC = "unsmile_data"

consumer = KafkaConsumer(UNSMILE_DATA_TOPIC, bootstrap_servers = brokers)
producer = KafkaProducer(bootstrap_servers = brokers)

# Elasticsearch
ELASTICSEARCH_HOST = "http://localhost:9200"
es = Elasticsearch([ELASTICSEARCH_HOST])

INDEX_NAME = "unsmile"

for message in consumer:
    msg = json.loads(message.value.decode())
    # Send data to elasticsearch 
    msg.update({'@timestamp': datetime.datetime.now(pytz.timezone('Asia/Seoul')).strftime('%Y-%m-%dT%H:%M:%S%z')})
    print(msg)
    res = es.index(index=INDEX_NAME, document=msg)

    


