import logging

# Setup logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("pipeline.log"),
        logging.StreamHandler()
    ]
)

# Simulasi pipeline
data = ["15000", "N/A", "25000", "error", "50000"]

logging.info("Pipeline dimulai")

for item in data:
    try:
        nilai = int(item)
        logging.info(f"Data diproses: {nilai}")
    except ValueError:
        logging.warning(f"Data tidak valid, dilewati: {item}")

logging.info("Pipeline selesai")
