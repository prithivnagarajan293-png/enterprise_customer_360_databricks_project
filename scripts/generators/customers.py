import random
import pandas as pd

from faker import Faker

from utils.config import (
    NUM_CUSTOMERS,
    BATCH_DATA_DIR
)

fake = Faker()


def generate_customers():

    customers = []

    cities = [
        "Chennai",
        "Bengaluru",
        "Hyderabad",
        "Mumbai",
        "Delhi",
        "Pune",
        "Kolkata",
        "Ahmedabad",
        "Coimbatore",
        "Jaipur"
    ]

    states = [
        "Tamil Nadu",
        "Karnataka",
        "Telangana",
        "Maharashtra",
        "Delhi",
        "Maharashtra",
        "West Bengal",
        "Gujarat",
        "Tamil Nadu",
        "Rajasthan"
    ]

    loyalty_levels = [
        "Bronze",
        "Silver",
        "Gold",
        "Platinum"
    ]

    for i in range(1, NUM_CUSTOMERS + 1):

        customers.append({

            "customer_id": f"C{i:07d}",

            "first_name": fake.first_name(),

            "last_name": fake.last_name(),

            "email": fake.email(),

            "phone": fake.msisdn()[:10],

            "city": random.choice(cities),

            "state": random.choice(states),

            "country": "India",

            "date_of_birth": fake.date_between(
                start_date="-65y",
                end_date="-18y"
            ),

            "registration_date": fake.date_between(
                start_date="-5y",
                end_date="today"
            ),

            "loyalty_level": random.choices(
                loyalty_levels,
                weights=[45,30,20,5]
            )[0]

        })

    df = pd.DataFrame(customers)

    # -------------------------
    # Dirty Data
    # -------------------------

    # Missing emails

    df.loc[df.sample(frac=0.01).index, "email"] = None

    # Missing cities

    df.loc[df.sample(frac=0.005).index, "city"] = None

    # Mixed Case

    df.loc[df.sample(frac=0.01).index, "first_name"] = (
        df["first_name"].str.upper()
    )

    # Extra Spaces

    df.loc[df.sample(frac=0.01).index, "last_name"] = (
        " " + df["last_name"] + " "
    )

    # Duplicate Customers

    duplicates = df.sample(100)

    df = pd.concat(
        [df, duplicates],
        ignore_index=True
    )

    output = BATCH_DATA_DIR / "customers.csv"

    df.to_csv(
        output,
        index=False
    )

    print(f"Customers generated : {len(df):,}")
    print(f"Saved to            : {output}")