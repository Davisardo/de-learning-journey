import pandas as pd
import logging

logging.basicConfig(level=logging.INFO, format="%(message)s")
logger = logging.getLogger(__name__)


def load_data():
    filepath = "data/DataCoSupplyChainDataset.csv"  # path relative dari project5_routewise-logistics
    df = pd.read_csv(filepath, encoding="latin-1")
    logger.info(f"[LOAD] Loaded {len(df):,} baris dari CSV")
    return df


def create_fact_shipments(df):
    logger.info("\n[FACT] Membuat fact_shipments...")

    # STEP 1 - SELECT kolom yang relevan
    fact = df[
        [
            "Order Id",
            "Shipping Mode",
            "Order City",
            "Customer City",
            "order date (DateOrders)",
            "Days for shipping (real)",
            "Days for shipment (scheduled)",
            "Delivery Status",
            "Late_delivery_risk",
        ]
    ].copy()

    # STEP 2 - RENAME kolom ke snake_case
    fact = fact.rename(
        columns={
            "Order Id": "shipment_id",
            "Shipping Mode": "carrier",
            "Order City": "origin",
            "Customer City": "destination",
            "order date (DateOrders)": "order_date",
            "Days for shipping (real)": "days_shipping_real",
            "Days for shipment (scheduled)": "days_shipping_scheduled",
            "Delivery Status": "delivery_status",
            "Late_delivery_risk": "late_delivery_risk",
        }
    )

    # STEP 3 - DERIVE kolom turunan
    order_date = pd.to_datetime(fact["order_date"], errors="coerce")
    # tanggal sampai sebenarnya = tanggal order + hari pengiriman aktual
    actual_delivery_date = order_date + pd.to_timedelta(
        fact["days_shipping_real"], unit="D"
    )
    # tanggal sampai yang dijadwalkan = tanggal order + hari yang dijadwalkan
    expected_delivery_date = order_date + pd.to_timedelta(
        fact["days_shipping_scheduled"], unit="D"
    )
    fact["delay_days"] = (actual_delivery_date - expected_delivery_date).dt.days

    # kategorikan delay jadi 3 level
    fact["delay_category"] = fact["delay_days"].apply(
        lambda x: (
            "On time" if x <= 0 else "Slight Delay" if 1 <= x <= 3 else "Major Delay"
        )
    )

    # STEP 5 - LOGGING
    logger.info(f"[FACT_SHIPMENTS] Created: {len(fact):,} baris berhasil di proses")
    return fact


def create_dim_carrier(df):
    logger.info("\n[DIM] Membuat dim_carrier...")

    # STEP 1 - SELECT
    df_carrier = df[["Shipping Mode"]]

    # STEP 2 - RENAME
    df_carrier = df_carrier.rename(columns={"Shipping Mode": "carrier"})

    # STEP 3 - DEDUPLICATE (1 carrier = 1 baris, meski punya ratusan shipment di fact)
    df_carrier = df_carrier.drop_duplicates().reset_index(drop=True)

    # STEP 4 - TAMBAH carrier_id sebagai primary key
    df_carrier["carrier_id"] = df_carrier.index + 1

    # STEP 5 - LOGGING
    logger.info(f"[DIM_CARRIER] Created: {len(df_carrier):,} baris unik berhasil di buat")
    return df_carrier


def create_dim_route(df):
    logger.info("\n[DIM] Membuat dim_route...")

    # STEP 1 - SELECT
    dim_route = df[["Order City", "Customer City"]]

    # STEP 2 - RENAME
    dim_route = dim_route.rename(
        columns={"Order City": "origin", "Customer City": "destination"}
    )

    # STEP 3 - DEDUPLICATE (1 kombinasi origin-destination = 1 baris)
    dim_route = dim_route.drop_duplicates().reset_index(drop=True)

    # STEP 4 - TAMBAH route_id sebagai primary key
    dim_route["route_id"] = dim_route.index + 1

    # STEP 5 - LOGGING
    logger.info(f"[DIM_ROUTE] Created: {len(dim_route):,} baris unik berhasil di buat")
    return dim_route


if __name__ == "__main__":
    df = load_data()
    fact_shipments = create_fact_shipments(df)
    dim_carrier = create_dim_carrier(df)
    dim_route = create_dim_route(df)

    print(fact_shipments.head(3))
    print(dim_carrier.head(3))
    print(dim_route.head(3))