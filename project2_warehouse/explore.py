import pandas as pd

# Baca dataset
orders = pd.read_csv("data/olist_orders_dataset.csv")          # data pesanan
payments = pd.read_csv("data/olist_order_payments_dataset.csv")  # data pembayaran

print("=== ORDERS ===")
print(f"Shape: {orders.shape}")
print(orders.head(3))
print(orders.dtypes)

print("\n=== PAYMENTS ===")
print(f"Shape: {payments.shape}")
print(payments.head(3))
print(payments.dtypes)