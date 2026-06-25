import pandas as pd
import logging

# Setup logging
logging.basicConfig(level=logging.INFO, format="%(message)s")
logger = logging.getLogger(__name__)


def load_data():
    filepath = r"D:\de-learning-journey\data\logistics\DataCoSupplyChainDataset.csv"
    df = pd.read_csv(filepath, encoding="latin-1")
    logger.info(f"[LOAD] Loaded {len(df):,} baris dari CSV")
    return df


def validate_and_clean(df):
    initial_rows = len(df)
    logger.info(f"[START] Total baris masuk: {initial_rows:,}")
    logger.info("=" * 50)

    # STEP 2 - REMOVE DUPLICATES
    before_dupes = len(df)
    df = df.drop_duplicates()
    logger.info(f"[DUPLICATES] Dibuang: {before_dupes - len(df):,} baris")

    # STEP 3A - HANDLE MISSING VALUES (kolom WAJIB → drop)
    required_cols = [
        "Order Id",
        "Shipping Mode",
        "Days for shipping (real)",
        "Days for shipment (scheduled)",
        "order date (DateOrders)",
    ]
    before_missing = len(df)
    df = df.dropna(subset=required_cols)
    logger.info(f"[KOLOM KOSONG] Dibuang: {before_missing - len(df):,} baris")

    # STEP 3B - HANDLE MISSING VALUES (kolom OPSIONAL → fill)
    df['Order Zipcode'] = df['Order Zipcode'].fillna('UNKNOWN')
    df['Customer Zipcode'] = df['Customer Zipcode'].fillna('UNKNOWN')
    logger.info(f"Kolom 'Order Zipcode' dan 'Customer Zipcode' yang kosong sudah di isi dengan 'UNKNOWN'")

    # STEP 4A - VALIDATE LOGIC (nilai negatif)
    before_negative = len(df)
    df = df[df['Days for shipping (real)'] >= 0]
    df = df[df['Days for shipment (scheduled)'] >= 0]
    logger.info(f"[VALIDATE] Nilai negatif dibuang: {before_negative - len(df):,} baris")

    # STEP 4B - VALIDATE LOGIC (Order Id tidak valid)
    before_invalid = len(df)
    df = df[df['Order Id'].notna() & (df['Order Id'] != 0)]
    logger.info(f"[VALIDATE] Order Id tidak valid dibuang: {before_invalid - len(df):,} baris")

    # STEP 5 - LOG HASIL AKHIR
    final_rows = len(df)
    logger.info(f"[DONE] Total baris keluar: {final_rows:,}")
    logger.info(f"[REMOVED] Total dibuang: {initial_rows - final_rows:,} baris")
    logger.info(f"[INFO] Data tersisa: {(final_rows/initial_rows) * 100:.2f}%")
    logger.info("=" * 50)

    return df


if __name__ == "__main__":
    df = load_data()
    df_clean = validate_and_clean(df)
