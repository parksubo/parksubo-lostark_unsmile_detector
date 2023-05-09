from kafka import KafkaProducer
import unsmile_detector
import time
import random
import csv

brokers = ["localhost:9091", "localhost:9092", "localhost:9093"]
producer = KafkaProducer(bootstrap_servers = brokers)

topicName = "korean_unsmile"

with open("./dataset/test.csv", "r", encoding="utf-8") as file:
    rows = csv.reader(file)
    for row in rows:
        nickname, title, reg_date = row
        # If detected
        result = unsmile_detector.baseline(title)
        if result:
            data = row
            data.append(result['label'])
            data.append(result['score'])
            print(data)
            data_bytes = str(data).encode("utf-8")
            producer.send(topicName, value=data_bytes)
            
        # for random time chatting
        # t = random.randrange(1, 3) * 0.01
        # time.sleep(t)
        