import random
import pandas as pd

from faker import Faker

from utils.config import (
    NUM_ORDERS,
    NUM_CUSTOMERS,
    NUM_STORES,
    NUM_EMPLOYEES,
    BATCH_DATA_DIR,
)

fake = Faker()


SEGMENT_WEIGHTS = {
    "Bronze": 1,
    "Silver": 2,
    "Gold": 4,
    "Platinum": 8,
}


def build_customer_pool():

    pool = []

    customer_ranges = {
        "Bronze": (1, 5000),
        "Silver": (5001, 8000),
        "Gold": (8001, 9500),
        "Platinum": (9501, NUM_CUSTOMERS),
    }

    for segment, (start, end) in customer_ranges.items():

        weight = SEGMENT_WEIGHTS[segment]

        for customer_id in range(start, end + 1):
            pool.extend([customer_id] * weight)

    return pool


def generate_orders():

    payment_methods = [
        "UPI",
        "Credit Card",
        "Debit Card",
        "Cash",
        "Net Banking",
    ]

    order_statuses = [
        "Completed",
        "Completed",
        "Completed",
        "Completed",
        "Cancelled",
        "Returned",
    ]

    customer_pool = build_customer_pool()

    orders = []

    for i in range(1, NUM_ORDERS + 1):

        order_time = fake.date_time_between(
            start_date="-2y",
            end_date="now",
        )

        weekday = order_time.weekday()

        if weekday >= 5:
            store_upper = NUM_STORES
        else:
            store_upper = max(NUM_STORES - 10, 1)

        orders.append(
            {
                "order_id": f"O{i:08d}",
                "customer_id": f"C{random.choice(customer_pool):07d}",
                "store_id": f"S{random.randint(1, store_upper):03d}",
                "employee_id": f"E{random.randint(1, NUM_EMPLOYEES):05d}",
                "order_timestamp": order_time,
                "payment_method": random.choice(payment_methods),
                "order_status": random.choice(order_statuses),
                "is_weekend": weekday >= 5,
                "order_year": order_time.year,
                "order_month": order_time.month,
                "order_hour": order_time.hour,
            }
        )

    df = pd.DataFrame(orders)

    output = BATCH_DATA_DIR / "orders.csv"

    df.to_csv(
        output,
        index=False,
    )

    print(f"Orders generated    : {len(df):,}")
    print(f"Saved to            : {output}")