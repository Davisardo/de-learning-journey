from kafka import KafkaConsumer
import json
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

consumer = KafkaConsumer(
    "transaksi-topic",
    bootstrap_servers=['localhost:9092'],
    auto_offset_reset='earliest',
    value_deserializer=lambda v: json.loads(v.decode('utf-8'))
)

logging.info("Consumer menunggu pesan.....")

for message in consumer:
    data = message.value
    status = "VALID" if data["nilai"] > 0 else ("PERLU DICEK" if data["nilai"] == 0 else "INVALID")
    logging.info(f"Diterima: {data['nama']} | {data['nilai']} | {status}")