import random
import pandas as pd

from faker import Faker

from utils.config import NUM_PRODUCTS, BATCH_DATA_DIR

fake = Faker()


def generate_products():

    categories = {
        "Electronics": [
            ("Laptop", 0.20),
            ("Phone", 0.35),
            ("Tablet", 0.10),
            ("Headphones", 0.20),
            ("Monitor", 0.15),
        ],
        "Home": [
            ("Chair", 0.30),
            ("Table", 0.20),
            ("Sofa", 0.10),
            ("Lamp", 0.25),
            ("Shelf", 0.15),
        ],
        "Fashion": [
            ("Shirt", 0.35),
            ("Jeans", 0.25),
            ("Shoes", 0.20),
            ("Jacket", 0.10),
            ("Cap", 0.10),
        ],
        "Sports": [
            ("Football", 0.30),
            ("Cricket Bat", 0.35),
            ("Tennis Racket", 0.15),
            ("Yoga Mat", 0.20),
        ],
        "Beauty": [
            ("Perfume", 0.30),
            ("Cream", 0.25),
            ("Lipstick", 0.25),
            ("Face Wash", 0.20),
        ],
        "Grocery": [
            ("Rice", 0.30),
            ("Coffee", 0.20),
            ("Tea", 0.20),
            ("Juice", 0.10),
            ("Snacks", 0.20),
        ],
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
        "Nimbus",
    ]
    products = []

    for i in range(1, NUM_PRODUCTS + 1):

        category = random.choice(list(categories.keys()))

        items = categories[category]

        names = [x[0] for x in items]
        weights = [x[1] for x in items]

        product_name = random.choices(names, weights=weights, k=1)[0]

        products.append(
            {
                "product_id": f"P{i:06d}",
                "product_name": product_name,
                "category": category,
                "brand": random.choice(brands),
                "popularity_score": round(random.triangular(0.05, 1.0, 0.75), 3),
                "inventory_quantity": random.randint(0, 1500),
                "supplier_name": random.choice(
                    [
                        "Global Supplies Ltd",
                        "Prime Distribution",
                        "Vertex Imports",
                        "Apex Manufacturing",
                        "Retail Source India",
                    ]
                ),
                "unit_price": round(random.uniform(100, 50000), 2),
                "cost_price": round(random.uniform(50, 30000), 2),
                "is_active": random.choice([True, True, True, False]),
            }
        )

    df = pd.DataFrame(products)

    # Dirty Data

    df.loc[df.sample(frac=0.01).index, "brand"] = None

    df.loc[df.sample(frac=0.005).index, "unit_price"] = -1

    df.loc[df.sample(frac=0.01).index, "product_name"] = " " + df["product_name"] + " "

    output = BATCH_DATA_DIR / "products.csv"

    df.to_csv(output, index=False)

    print(f"Products generated  : {len(df):,}")
    print(f"Saved to            : {output}")
