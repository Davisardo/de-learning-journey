import json
import random
import time
import logging
from datetime import datetime
from kafka import KafkaProducer

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

producer = KafkaProducer(
    bootstrap_servers='127.0.0.1:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8'),
    api_version=(3, 7, 0)
)

def generate_transaction():
    return {
        "order_id": f"ORD-{random.randint(10000, 99999)}",
        "customer_id": f"CUST-{random.randint(1, 1000)}",
        "product": random.choice(["laptop", "phone", "headset", "keyboard", "monitor"]),
        "amount": round(random.uniform(50000, 5000000), 2),
        "payment_type": random.choice(["credit_card", "transfer", "ewallet"]),
        "timestamp": datetime.now().isoformat()
    }

if __name__ == "__main__":
    logging.info("Producer dimulai — mengirim transaksi ke Kafka...")
    while True:
        transaction = generate_transaction()
        producer.send('transactions', value=transaction)
        logging.info(f"Terkirim: {transaction}")
        time.sleep(1)