import random
import pandas as pd

from utils.config import (
    NUM_ORDERS,
    NUM_PRODUCTS,
    MAX_ITEMS_PER_ORDER,
    BATCH_DATA_DIR
)


def generate_order_items():

    rows = []

    item_id = 1

    for order in range(1, NUM_ORDERS + 1):

        number_of_items = random.randint(
            1,
            MAX_ITEMS_PER_ORDER
        )

        for _ in range(number_of_items):

            quantity = random.randint(1, 5)

            unit_price = round(
                random.uniform(100, 50000),
                2
            )

            rows.append({

                "order_item_id": item_id,

                "order_id": f"O{order:08d}",

                "product_id": f"P{random.randint(1, NUM_PRODUCTS):06d}",

                "quantity": quantity,

                "unit_price": unit_price,

                "discount": round(
                    random.uniform(0, 0.30),
                    2
                ),

                "line_amount": round(
                    quantity * unit_price,
                    2
                )

            })

            item_id += 1

    df = pd.DataFrame(rows)

    # ---------- Dirty Data ----------

    bad_rows = df.sample(frac=0.005).index

    df.loc[bad_rows, "quantity"] = -1

    bad_rows = df.sample(frac=0.005).index

    df.loc[bad_rows, "discount"] = None

    df.to_csv(
        BATCH_DATA_DIR / "order_items.csv",
        index=False
    )

    print(f"Order Items generated : {len(df):,}")