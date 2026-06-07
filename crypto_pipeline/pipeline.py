import logging
from extract import extract_crypto_data
from transform import transform_crypto_data
from load import load_to_postgres

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def run_pipeline():
    logging.info("=== Crypto ETL Pipeline Dimulai ===")

    # Extract
    raw_data = extract_crypto_data()

    # Transform
    df = transform_crypto_data(raw_data)

    # Load
    load_to_postgres(df)

    logging.info("=== Pipeline Selesai ===")

if __name__ == "__main__":
    run_pipeline()