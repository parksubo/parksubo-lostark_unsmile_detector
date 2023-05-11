from transformers import TextClassificationPipeline, BertForSequenceClassification, AutoTokenizer
from kafka import KafkaConsumer, KafkaProducer
import json

# If score is over 0.5, Judge the data as the label
def baseline(message):
    model_name = 'smilegate-ai/kor_unsmile'
    model = BertForSequenceClassification.from_pretrained(model_name)
    tokenizer = AutoTokenizer.from_pretrained(model_name)

    pipe = TextClassificationPipeline(
            model = model,
            tokenizer = tokenizer,
            device = -1,   # cpu: -1, gpu: gpu number
            return_all_scores = True,
            function_to_apply = 'sigmoid'
        )
    
    for result in pipe(message)[0]:
        if result['score'] >= 0.5:
            return result
    
    return None

# Kafka
brokers = ["localhost:9091", "localhost:9092", "localhost:9093"]

BOARD_DATA_TOPIC = "board_data"
CLEAN_DATA_TOPIC = "clean_data"
UNSMILE_DATA_TOPIC = "unsmile_data"

consumer = KafkaConsumer(BOARD_DATA_TOPIC, bootstrap_servers = brokers)
producer = KafkaProducer(bootstrap_servers = brokers)

for message in consumer:
    msg = json.loads(message.value.decode())
    result = baseline(msg["title"])
    if result:
        topic = CLEAN_DATA_TOPIC if result["label"] == "clean" else UNSMILE_DATA_TOPIC
        # Add label, score data to msg
        msg["label"] = result["label"]
        msg["score"] = result["score"]
        
        producer.send(topic=topic, value=json.dumps(msg).encode("utf-8"))
        print("Topic : " + topic, "/ Title : " + msg["title"], "/ Label : " + msg["label"])
    