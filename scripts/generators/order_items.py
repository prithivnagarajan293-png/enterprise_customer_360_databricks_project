import random
import pandas as pd

from utils.config import (
    NUM_ORDERS,
    MAX_ITEMS_PER_ORDER,
    BATCH_DATA_DIR,
)


def build_product_pool(products_df):
    """
    Build a weighted product pool using popularity_score.
    Popular products will naturally appear more often.
    """

    pool = []

    for _, row in products_df.iterrows():

        popularity = max(1, int(row["popularity_score"] * 100))

        pool.extend([row["product_id"]] * popularity)

    return pool


def generate_order_items():

    products = pd.read_csv(
        BATCH_DATA_DIR / "products.csv"
    )

    active_products = products[
        (products["is_active"] == True)
        & (products["unit_price"] > 0)
    ].copy()

    product_pool = build_product_pool(active_products)

    product_lookup = (
        active_products
        .set_index("product_id")
        .to_dict("index")
    )

    rows = []

    order_item_id = 1

    for order in range(1, NUM_ORDERS + 1):

        basket_size = random.choices(
            population=[1, 2, 3, 4, 5],
            weights=[40, 30, 15, 10, 5],
            k=1,
        )[0]

        basket_size = min(
            basket_size,
            MAX_ITEMS_PER_ORDER
        )

        selected_products = random.sample(
            product_pool,
            basket_size,
        )

        for product_id in selected_products:

            product = product_lookup[product_id]

            quantity = random.choices(
                [1, 2, 3, 4, 5],
                weights=[55, 25, 10, 7, 3],
                k=1,
            )[0]

            unit_price = round(
                float(product["unit_price"]),
                2,
            )

            discount = round(
                random.choice(
                    [0, 0, 0.05, 0.10, 0.15, 0.20]
                ),
                2,
            )

            gross_amount = quantity * unit_price

            line_amount = round(
                gross_amount * (1 - discount),
                2,
            )

            rows.append(
                {
                    "order_item_id": order_item_id,
                    "order_id": f"O{order:08d}",
                    "product_id": product_id,
                    "quantity": quantity,
                    "unit_price": unit_price,
                    "discount": discount,
                    "line_amount": line_amount,
                }
            )

            order_item_id += 1

    df = pd.DataFrame(rows)

    # ----------------------------
    # Dirty Data for Silver Layer
    # ----------------------------

    df.loc[
        df.sample(frac=0.005).index,
        "quantity",
    ] = -1

    df.loc[
        df.sample(frac=0.005).index,
        "discount",
    ] = None

    output = BATCH_DATA_DIR / "order_items.csv"

    df.to_csv(
        output,
        index=False,
    )

    print(f"Order Items generated : {len(df):,}")
    print(f"Saved to              : {output}")