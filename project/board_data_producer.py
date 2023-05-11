from kafka import KafkaProducer
import time
import random
import csv
import json

# Kafka
brokers = ["localhost:9091", "localhost:9092", "localhost:9093"]
producer = KafkaProducer(bootstrap_servers = brokers)
topic = "board_data"

# Data producer
with open("./dataset/board_data.csv", "r", encoding="utf-8") as file:
    rows = csv.reader(file)
    # Skip the header row
    next(rows)
    for row in rows:
        nickname, title, reg_date = row
        new_data = {
            "nickname" : nickname,
            "title" : title,
            "reg_date" : reg_date,
        }
        
        producer.send(topic=topic, value=json.dumps(new_data).encode("utf-8"))
        print(new_data)
        
        # # For random time data
        # t = random.randrange(1, 3) * 0.3
        # time.sleep(t)
    