import random
import pandas as pd

from faker import Faker

from utils.config import (
    NUM_CUSTOMERS,
    NUM_STORES,
    NUM_EMPLOYEES,
    NUM_ORDERS,
    BATCH_DATA_DIR
)

fake = Faker()


def generate_orders():

    payment_methods = [
        "Credit Card",
        "Debit Card",
        "UPI",
        "Cash",
        "Net Banking"
    ]

    order_status = [
        "Completed",
        "Completed",
        "Completed",
        "Completed",
        "Cancelled",
        "Returned"
    ]

    orders = []

    for i in range(1, NUM_ORDERS + 1):

        order_date = fake.date_time_between(
            start_date="-2y",
            end_date="now"
        )

        orders.append({

            "order_id": f"O{i:08d}",

            "customer_id": f"C{random.randint(1, NUM_CUSTOMERS):07d}",

            "store_id": f"S{random.randint(1, NUM_STORES):03d}",

            "employee_id": f"E{random.randint(1, NUM_EMPLOYEES):05d}",

            "order_timestamp": order_date,

            "payment_method": random.choice(payment_methods),

            "order_status": random.choice(order_status)

        })

    df = pd.DataFrame(orders)

    df.to_csv(
        BATCH_DATA_DIR / "orders.csv",
        index=False
    )

    print(f"Orders generated    : {len(df):,}")