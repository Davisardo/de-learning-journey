import json
import logging
import psycopg2
from kafka import KafkaConsumer
from datetime import datetime
from dotenv import load_dotenv
import os

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("logs/consumer.log"), logging.StreamHandler()],
)


def connect_db():
    try:
        conn = psycopg2.connect(
            host=os.getenv("DB_HOST"),
            database=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            port=os.getenv("DB_PORT"),
        )
        logging.info("Koneksi PostgreSQL berhasil")
        return conn
    except Exception as e:
        logging.error(f"Gagal konek ke PostgreSQL: {e}")
        raise


def save_transaction(cursor, conn, transaction):
    try:
        cursor.execute(
            """
            INSERT INTO transactions 
            (order_id, customer_id, product, amount, payment_type, timestamp)
            VALUES (%s, %s, %s, %s, %s, %s)
            """,
            (
                transaction["order_id"],
                transaction["customer_id"],
                transaction["product"],
                transaction["amount"],
                transaction["payment_type"],
                transaction["timestamp"],
            ),
        )
        conn.commit()
        return True
    except Exception as e:
        logging.error(f"Gagal simpan transaksi {transaction['order_id']}: {e}")
        conn.rollback()
        return False


if __name__ == "__main__":
    logging.info("=== Consumer dimulai ===")
    start_time = datetime.now()
    total_processed = 0
    total_error = 0

    conn = connect_db()
    cursor = conn.cursor()

    consumer = KafkaConsumer(
        "transactions",
        bootstrap_servers="127.0.0.1:9092",
        value_deserializer=lambda v: json.loads(v.decode("utf-8")),
        auto_offset_reset="latest",
        group_id="transaction-consumer-group",
        api_version=(3, 7),
    )

    try:
        for message in consumer:
            transaction = message.value
            success = save_transaction(cursor, conn, transaction)
            if success:
                total_processed += 1
                logging.info(
                    f"[OK] {transaction['order_id']} | {transaction['product']} | {transaction['amount']}"
                )
            else:
                total_error += 1

            if total_processed % 10 == 0 and total_processed > 0:
                elapsed = (datetime.now() - start_time).seconds
                logging.info(
                    f"=== Stats: {total_processed} sukses | {total_error} error | {elapsed} detik berjalan ==="
                )

    except KeyboardInterrupt:
        elapsed = (datetime.now() - start_time).seconds
        logging.info(f"=== Consumer dihentikan ===")
        logging.info(
            f"=== Total: {total_processed} sukses | {total_error} error | {elapsed} detik ==="
        )
    finally:
        cursor.close()
        conn.close()
        logging.info("=== Koneksi database ditutup ===")
