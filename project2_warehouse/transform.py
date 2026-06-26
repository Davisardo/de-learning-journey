import pandas as pd
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)


def load_data():
    # baca 4 dataset mentah Olist
    orders = pd.read_csv("data/olist_orders_dataset.csv")
    payments = pd.read_csv("data/olist_order_payments_dataset.csv")
    customers = pd.read_csv("data/olist_customers_dataset.csv")
    products = pd.read_csv("data/olist_products_dataset.csv")

    logging.info(f"Orders: {len(orders)} baris")
    logging.info(f"Payments: {len(payments)} baris")
    logging.info(f"Customers: {len(customers)} baris")
    logging.info(f"Products: {len(products)} baris")
    return orders, payments, customers, products


def create_dim_orders(orders):
    # SELECT - ambil kolom yang relevan
    dim = orders[[
        'order_id', 'customer_id',
        'order_status', 'order_purchase_timestamp'
    ]].copy()

    # RENAME - standarkan nama kolom
    dim.columns = ['order_id', 'customer_id', 'status', 'purchase_date']

    # CLEAN - order_id wajib ada, drop kalau kosong
    dim = dim.dropna(subset=['order_id'])

    logging.info(f"dim_orders: {len(dim)} baris")
    return dim


def create_fact_payments(payments):
    # SELECT - ambil kolom yang relevan
    fact = payments[[
        'order_id', 'payment_type',
        'payment_installments', 'payment_value'
    ]].copy()

    # RENAME - standarkan nama kolom
    fact.columns = ['order_id', 'payment_type', 'installments', 'value']

    # CLEAN - drop missing values
    fact = fact.dropna()

    # VALIDATE - buang transaksi dengan payment_type tidak valid
    fact = fact[fact['payment_type'] != 'not_defined']

    logging.info(f"fact_payments: {len(fact)} baris")
    return fact


def create_dim_customers(customers):
    # SELECT - ambil kolom yang relevan
    dim = customers[[
        'customer_id', 'customer_city', 'customer_state'
    ]].copy()

    # DEDUPLICATE - 1 customer harus 1 baris di dimension table
    dim = dim.drop_duplicates(subset=['customer_id'])
    dim = dim.dropna()

    logging.info(f"dim_customer: {len(dim)} baris")
    return dim


def create_dim_products(products):
    # SELECT - ambil kolom yang relevan
    dim = products[[
        'product_id', 'product_category_name',
        'product_weight_g', 'product_length_cm'
    ]].copy()

    # DEDUPLICATE - 1 produk harus 1 baris di dimension table
    dim = dim.drop_duplicates(subset=['product_id'])
    dim = dim.dropna(subset=['product_id'])

    logging.info(f"dim_products: {len(dim)} baris")
    return dim


if __name__ == "__main__":
    orders, payments, customers, products = load_data()  # ambil 4 dataset mentah

    # transformasi jadi fact & dimension table
    dim_orders = create_dim_orders(orders)
    fact_payments = create_fact_payments(payments)
    dim_customers = create_dim_customers(customers)
    dim_product = create_dim_products(products)

    print(dim_orders.head(3))
    print(fact_payments.head(3))