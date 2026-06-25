import pandas as pd

# ============================================================
# LEVEL 1 - DATA RECON
# RouteWise Logistics - Supply Chain Exploration
# ============================================================

# 1. LOAD DATA
df = pd.read_csv(
    r"D:\de-learning-journey\data\logistics\DataCoSupplyChainDataset.csv",
    encoding="latin-1",
)

# 2. STRUCTURAL CHECK
print("\n=== Structural Check ===")
print(f"Total Baris: {df.shape[0]}")
print(f"Total Kolom: {df.shape[1]}")
print(df.columns.tolist())
print(df.dtypes)
print("=" * 50)

# 3. COMPLETENESS CHECK
missing = df.isnull().sum() / len(df) * 100
print("\n=== Missing Values (%) ===")
print(missing[missing > 0].sort_values(ascending=False))
print("=" * 50)

# 4. DISTRIBUTION CHECK
print("\n=== Delivery Status ===")
print(df["Delivery Status"].value_counts())

print("\n=== Shipping Mode ===")
print(df["Shipping Mode"].value_counts())
print("=" * 50)


# 5. BUSINESS QUESTION — HITUNG % DELAY
print("\n=== Business Question ===")
order_date = pd.to_datetime(df["order date (DateOrders)"], errors="coerce")
actual_delivery_date = order_date + pd.to_timedelta(
    df["Days for shipping (real)"], unit="D"
)
expected_delivery_date = order_date + pd.to_timedelta(
    df["Days for shipment (scheduled)"], unit="D"
)
df["is_delayed"] = actual_delivery_date > expected_delivery_date
pct_delay = df["is_delayed"].sum() / len(df) * 100
print(f"% Delay: {pct_delay:.2f}%")

delay_by_mode = df.groupby("Shipping Mode")["is_delayed"].mean() * 100
print("\n=== Delay Rate per Shipping Mode (%) ===")
print(delay_by_mode.sort_values(ascending=False).round(2))

print("\n=== SUMMARY ===")
print(f"Total shipment: {len(df):,}")
print(f"Overall delay rate: {pct_delay:.2f}%")
print(f"Shipping mode paling bermasalah: {delay_by_mode.idxmax()}")
print("=" * 50)
