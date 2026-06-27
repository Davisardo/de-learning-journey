import pandas as pd
import logging
from datetime import datetime

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


def transform_crypto_data(raw_data):
    """Transform raw data dari API ke DataFrame yang bersih"""

    df = pd.DataFrame(raw_data)

    # Pilih kolom yang relevan
    kolom = [
        "id",
        "symbol",
        "name",
        "current_price",
        "market_cap",
        "price_change_percentage_24h",
        "total_volume",
        "last_updated",
    ]
    df = df[kolom]

    # Rename kolom
    df.columns = [
        "coin_id",
        "symbol",
        "name",
        "price_usd",
        "market_cap",
        "price_change_24h",
        "volume_24h",
        "last_updated",
    ]

    # Tambah kolom status berdasarkan perubahan harga
    df["trend"] = df["price_change_24h"].apply(
        lambda x: "UP" if x > 0 else ("DOWN" if x < 0 else "STABLE")
    )

    # Tambah timestamp kapan data diproses
    df["processed_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    logging.info(f"Transform selesai: {len(df)} baris")
    return df


if __name__ == "__main__":
    from extract import extract_crypto_data

    raw = extract_crypto_data()
    df = transform_crypto_data(raw)
    print(df[["name", "price_usd", "trend"]].to_string())
