
from kafka import KafkaConsumer
# from elasticsearch import Elasticsearch

brokers = ["localhost:9091", "localhost:9092", "localhost:9093"]
topicName = "korean_unsmile"
consumer = KafkaConsumer(topicName, bootstrap_servers = brokers)

for message in consumer:
    message_value = message.value.decode("utf-8")
    