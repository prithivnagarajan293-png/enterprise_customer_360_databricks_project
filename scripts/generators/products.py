import random
import pandas as pd

from faker import Faker

from utils.config import (
    NUM_PRODUCTS,
    BATCH_DATA_DIR
)

fake = Faker()


def generate_products():

    categories = {
        "Electronics": ["Laptop", "Phone", "Tablet", "Headphones", "Monitor"],
        "Home": ["Chair", "Table", "Sofa", "Lamp", "Shelf"],
        "Fashion": ["Shirt", "Jeans", "Shoes", "Jacket", "Cap"],
        "Sports": ["Football", "Cricket Bat", "Tennis Racket", "Yoga Mat"],
        "Beauty": ["Perfume", "Cream", "Lipstick", "Face Wash"],
        "Grocery": ["Rice", "Coffee", "Tea", "Juice", "Snacks"]
    }

    brands = [
        "Nova",
        "Elite",
        "Prime",
        "Vision",
        "Apex",
        "Urban",
        "Fusion",
        "Zenith",
        "EcoLife",
        "Nimbus"
    ]

    products = []

    for i in range(1, NUM_PRODUCTS + 1):

        category = random.choice(list(categories.keys()))

        product_name = random.choice(categories[category])

        products.append({

            "product_id": f"P{i:06d}",

            "product_name": product_name,

            "category": category,

            "brand": random.choice(brands),

            "unit_price": round(random.uniform(100, 50000), 2),

            "cost_price": round(random.uniform(50, 30000), 2),

            "is_active": random.choice([True, True, True, False])

        })

    df = pd.DataFrame(products)

    # Dirty Data

    df.loc[df.sample(frac=0.01).index, "brand"] = None

    df.loc[df.sample(frac=0.005).index, "unit_price"] = -1

    df.loc[df.sample(frac=0.01).index, "product_name"] = (
        " " + df["product_name"] + " "
    )

    output = BATCH_DATA_DIR / "products.csv"

    df.to_csv(output, index=False)

    print(f"Products generated  : {len(df):,}")
    print(f"Saved to            : {output}")