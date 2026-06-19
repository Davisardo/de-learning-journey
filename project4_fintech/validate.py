import pandas as pd
import logging

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


def load_data():
    df = pd.read_csv("data/credit/creditcard.csv")
    logging.info(f"Loaded {len(df)} baris")
    return df


def check_missing(df):
    miss_count = df.isnull().sum().sum()
    logging.info(f"Jumlah baris kosong: {miss_count}")
    return miss_count


def check_duplicates(df):
    dup_count = df.duplicated().sum()
    logging.info(f"Jumlah baris duplikat: {dup_count}")
    return dup_count


def check_amount_range(df):
    min_val = df["Amount"].min()
    max_val = df["Amount"].max()
    zero_or_negative = (df["Amount"] <= 0).sum()
    logging.info(f"Amount range: {min_val} - {max_val}, <=: {zero_or_negative}")
    return min_val, max_val, zero_or_negative


def check_time_range(df):
    min_val = df["Time"].min()
    max_val = df["Time"].max()
    logging.info(f"Time range: {min_val} - {max_val}")
    return min_val, max_val


if __name__ == "__main__":
    data = load_data()
    missing = check_missing(data)
    duplicates = check_duplicates(data)
    amount = check_amount_range(data)
    time = check_time_range(data)

zero_amount = data[data["Amount"] == 0]
print(zero_amount["Class"].value_counts())

data_clean = data.drop_duplicates()
logging.info(f"Setelah drop duplikat: {len(data_clean)} baris")
