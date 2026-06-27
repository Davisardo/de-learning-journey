import psycopg2
import pandas as pd
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

DB_CONFIG ={
    "host": "localhost",
    "port": 5432,
    "database": "crypto_db",
    "user": "davis",
    "password": "davis123"
}

def create_table(conn):
    """Buat tabel kalau belum ada"""
    query = """
        CREATE TABLE IF NOT EXISTS crypto_prices (
            id SERIAL PRIMARY KEY,
            coin_id VARCHAR(50),
            symbol VARCHAR(20),
            name VARCHAR(100),
            price_usd NUMERIC,
            market_cap BIGINT,
            price_change_24h NUMERIC,
            volume_24h BIGINT,
            last_updated VARCHAR(50),
            trend VARCHAR(10),
            processed_at VARCHAR(50)
        )
    """
    cursor = conn.cursor()
    cursor.execute(query)
    conn.commit()
    logging.info("Tabel crypto_prices siap")

def load_to_postgres(df):
    """Load DataFrame ke PostgreSQL"""
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        create_table(conn)

        cursor = conn.cursor()
        for _, row in df.iterrows():
            cursor.execute("""
                INSERT INTO crypto_prices
                (coin_id, symbol, name, price_usd, market_cap,
                price_change_24h, volume_24h, last_updated, trend, processed_at)
                VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, tuple(row))

        conn.commit()
        logging.info(f"Berhasil load {len(df)} baris ke PostgreSQL")
        conn.close()
    
    except Exception as e:
        logging.error(f"Load gagal: {e}")
        raise

if __name__ == "__main__":
    from extract import extract_crypto_data
    from transform import transform_crypto_data

    raw = extract_crypto_data()
    df = transform_crypto_data(raw)
    load_to_postgres(df)
