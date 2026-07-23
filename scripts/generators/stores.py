import random
import pandas as pd

from utils.config import NUM_STORES, BATCH_DATA_DIR


def generate_stores():

    cities = [
        ("Chennai", "Tamil Nadu"),
        ("Bengaluru", "Karnataka"),
        ("Hyderabad", "Telangana"),
        ("Mumbai", "Maharashtra"),
        ("Delhi", "Delhi"),
        ("Pune", "Maharashtra"),
        ("Kolkata", "West Bengal"),
        ("Ahmedabad", "Gujarat"),
        ("Coimbatore", "Tamil Nadu"),
        ("Jaipur", "Rajasthan")
    ]

    stores = []

    for i in range(1, NUM_STORES + 1):

        city, state = random.choice(cities)

        stores.append({

            "store_id": f"S{i:03d}",
            "store_name": f"{city} Store {i}",
            "city": city,
            "state": state,
            "region": random.choice(
                ["North", "South", "East", "West"]
            ),
            "opening_date": pd.Timestamp.today().date()
        })

    df = pd.DataFrame(stores)

    df.to_csv(
        BATCH_DATA_DIR / "stores.csv",
        index=False
    )

    print(f"Stores generated    : {len(df):,}")