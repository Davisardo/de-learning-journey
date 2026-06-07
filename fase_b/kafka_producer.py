from  kafka import KafkaProducer
import json
import time
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

producer = KafkaProducer(
    bootstrap_servers=['localhost:9092'],
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

# Simulasi event transaksi real-time
transaksi = [
    {"user_id": 1, "nama": "Davis", "nilai": 15000},
    {"user_id": 2, "nama": "Andi", "nilai": -5000},
    {"user_id": 3, "nama": "Budi", "nilai": 25000},
    {"user_id": 4, "nama": "Citra", "nilai": 0},
    {"user_id": 5, "nama": "Deni", "nilai": 50000},
]

for trx in transaksi:
    producer.send("transaksi-topic", value=trx)
    logging.info(f"Terkirim: {trx}")
    time.sleep(1)

producer.flush()
logging.info("Semua pesan terkirim")
