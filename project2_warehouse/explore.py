import pandas as pd

# Baca dataset
orders = pd.read_csv("data/olist/olist_orders_dataset.csv")
payments = pd.read_csv("data/olist/olist_order_payments_dataset.csv")

print("=== ORDERS ===")
print(f"Shape: {orders.shape}")
print(orders.head(3))
print(orders.dtypes)

print("\n=== PAYMENTS ===")
print(f"Shape: {payments.shape}")
print(payments.head(3))
print(payments.dtypes)
