from datetime import datetime
import logging
import pandas as pd

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


# ==============================================================================
# 1. HELPER FUNCTIONS (UDF)
# ==============================================================================
def get_hour(time_seconds):
    return (time_seconds // 3600) % 24  # ubah Time (detik) jadi jam 0-23


def get_time_period(hour):
    if hour >= 18 or hour <= 3:
        return "Night"
    elif hour >= 4 and hour <= 10:
        return "Morning"
    elif hour >= 11 and hour <= 15:
        return "Afternoon"
    else:
        return "Evening"


def is_peak_hour(hour, peak_hours):
    return hour in peak_hours


def get_amount_bucket(amount):
    if amount <= 10:
        return "Small"
    elif amount <= 50:
        return "Medium"
    elif amount <= 200:
        return "Large"
    else:
        return "Very Large"


# ==============================================================================
# 2. BUILD FUNCTIONS (RETURN DATA + DATAFRAME)
# ==============================================================================
def build_dim_time(data):
    data["hour"] = data["Time"].apply(get_hour)
    data["time_period"] = data["hour"].apply(get_time_period)

    hourly_counts = data["hour"].value_counts()
    peak_hours = hourly_counts.nlargest(6).index.tolist()  # 6 jam tersibuk
    data["is_peak_hour"] = data["hour"].apply(lambda h: is_peak_hour(h, peak_hours))

    dim_time = (
        data[["hour", "time_period", "is_peak_hour"]]
        .drop_duplicates()
        .sort_values("hour")
        .reset_index(drop=True)
    )
    return data, dim_time


def build_dim_amount(data):
    data["amount_bucket"] = data["Amount"].apply(get_amount_bucket)
    dim_amount_data = {
        "amount_bucket": ["Small", "Medium", "Large", "Very Large"],
        "min_range": [0.0, 10.01, 50.01, 200.01],
        "max_range": [10.0, 50.0, 200.0, float(999999.99)],
    }
    dim_amount = pd.DataFrame(dim_amount_data)
    return data, dim_amount


def build_dim_fraud(data):
    dim_fraud_data = {
        "Class": [0, 1],
        "fraud_label": ["Normal", "Fraud"],
        "risk_level": ["Low", "High"],
    }
    dim_fraud = pd.DataFrame(dim_fraud_data)
    return data, dim_fraud


def build_dim_features(data):
    # bagi V1, V2, V3 jadi 3 kategori berdasarkan quantile (33%/33%/33%)
    data["V1_category"] = pd.qcut(data["V1"], q=3, labels=["Low", "Medium", "High"])
    data["V2_category"] = pd.qcut(data["V2"], q=3, labels=["Low", "Medium", "High"])
    data["V3_category"] = pd.qcut(data["V3"], q=3, labels=["Low", "Medium", "High"])

    _, bins_v1 = pd.qcut(
        data["V1"], q=3, labels=["Low", "Medium", "High"], retbins=True
    )
    _, bins_v2 = pd.qcut(
        data["V2"], q=3, labels=["Low", "Medium", "High"], retbins=True
    )
    _, bins_v3 = pd.qcut(
        data["V3"], q=3, labels=["Low", "Medium", "High"], retbins=True
    )

    dim_features_data = {
        "feature_name": ["V1", "V2", "V3"],
        "low_max": [bins_v1[1], bins_v2[1], bins_v3[1]],
        "medium_max": [bins_v1[2], bins_v2[2], bins_v3[2]],
    }
    dim_features = pd.DataFrame(dim_features_data)
    return data, dim_features


def build_fact_transaction(data):
    data = data.reset_index(drop=True)
    data["transaction_id"] = data.index  # buat ID unik sebagai primary key
    fact_transaction = data[
        [
            "transaction_id",
            "hour",
            "amount_bucket",
            "Class",
            "Amount",
            "V1_category",
            "V2_category",
            "V3_category",
        ]
    ]
    return data, fact_transaction


# ==============================================================================
# 3. RUN STANDALONE (untuk testing transform.py sendiri tanpa BigQuery)
# ==============================================================================
if __name__ == "__main__":
    logging.info("Memulai proses load data mentah...")
    data = pd.read_csv("data/creditcard.csv")  # baca dataset mentah
    data = data.drop_duplicates()
    logging.info(f"Data setelah drop duplikat: {len(data)} baris")

    data, dim_time = build_dim_time(data)
    data, dim_amount = build_dim_amount(data)
    data, dim_fraud = build_dim_fraud(data)
    data, dim_features = build_dim_features(data)
    data, fact_transaction = build_fact_transaction(data)

    print("\n=== DIM TIME ===")
    print(dim_time)
    print("\n=== DIM AMOUNT ===")
    print(dim_amount)
    print("\n=== DIM FRAUD ===")
    print(dim_fraud)
    print("\n=== DIM FEATURES ===")
    print(dim_features)
    print("\n=== FACT TRANSACTION (head) ===")
    print(fact_transaction.head())

    logging.info(f"dim_time        : {dim_time.shape}")
    logging.info(f"dim_amount      : {dim_amount.shape}")
    logging.info(f"dim_fraud       : {dim_fraud.shape}")
    logging.info(f"dim_features    : {dim_features.shape}")
    logging.info(f"fact_transaction: {fact_transaction.shape}")
