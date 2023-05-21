from kafka import KafkaProducer
from datetime import datetime
import mysql.connector
import json
import time

# Kafka
brokers = ["kafka-broker01:9092", "kafka-broker02:9092", "kafka-broker03:9092"]
producer = KafkaProducer(bootstrap_servers=brokers)
topic = "board_data"

# Read MySQL user info
with open("./user.txt", "r", encoding="utf-8") as file:
    line = file.readline()
    user, password = line.split(",")

# Connect MySQL
conn = mysql.connector.connect(
    host="mysql-server",
    user=user,
    password=password,
    database="lostark_raw_data"
)

# Load data from MySQL for the first time
cursor = conn.cursor()
cursor.execute("SELECT * FROM board_data")
rows = cursor.fetchall()

# Send initial data to Kafka
for row in rows:
    id, nickname, title, reg_date = row
    reg_date = datetime.strftime(reg_date, "%Y-%m-%d")
    new_data = {
        "nickname": nickname,
        "title": title,
        "reg_date": reg_date,
    }
    producer.send(topic=topic, value=json.dumps(new_data).encode("utf-8"))

cursor.close()
conn.close()

# Continuously check for new data in MySQL per 5 sec
while True:
    # Reconnect MySQL for new data detection
    conn = mysql.connector.connect(
        host="mysql-server",
        user=user,
        password=password,
        database="lostark_raw_data"
    )
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM board_data ORDER BY id DESC LIMIT 1")
    row = cursor.fetchone()
    # print("row[0]:", row[0])
    # print("id:", id)
    if row[0] != id:
        id, nickname, title, reg_date = row
        reg_date = datetime.strftime(reg_date, "%Y-%m-%d")
        new_data = {
            "nickname": nickname,
            "title": title,
            "reg_date": reg_date,
        }
        producer.send(topic=topic, value=json.dumps(new_data).encode("utf-8"))

    cursor.close()
    conn.close()
    time.sleep(5)
    