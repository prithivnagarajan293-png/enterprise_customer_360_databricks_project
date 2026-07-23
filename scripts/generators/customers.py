import random
import pandas as pd

from faker import Faker

from simulations.customer_profiles import CUSTOMER_SEGMENTS
from utils.config import NUM_CUSTOMERS, BATCH_DATA_DIR

fake = Faker()


INCOME_BY_SEGMENT = {
    "Bronze": (5000, 40000),
    "Silver": (40000, 120000),
    "Gold": (120000, 400000),
    "Platinum": (400000, 1500000),
}


def generate_customers():

    customers = []

    locations = [
        ("Chennai", "Tamil Nadu"),
        ("Bengaluru", "Karnataka"),
        ("Hyderabad", "Telangana"),
        ("Mumbai", "Maharashtra"),
        ("Delhi", "Delhi"),
        ("Pune", "Maharashtra"),
        ("Kolkata", "West Bengal"),
        ("Ahmedabad", "Gujarat"),
        ("Coimbatore", "Tamil Nadu"),
        ("Jaipur", "Rajasthan"),
    ]

    segment_names = list(CUSTOMER_SEGMENTS.keys())

    segment_weights = [
        CUSTOMER_SEGMENTS[s]["weight"]
        for s in segment_names
    ]

    channels = [
        "Store",
        "Website",
        "Mobile App"
    ]

    payment_methods = [
        "UPI",
        "Credit Card",
        "Debit Card",
        "Cash",
        "Net Banking"
    ]

    for i in range(1, NUM_CUSTOMERS + 1):

        city, state = random.choice(locations)

        segment = random.choices(
            segment_names,
            weights=segment_weights,
            k=1
        )[0]

        min_ltv, max_ltv = INCOME_BY_SEGMENT[segment]

        customers.append({

            "customer_id": f"C{i:07d}",

            "first_name": fake.first_name(),

            "last_name": fake.last_name(),

            "email": fake.email(),

            "phone": fake.msisdn()[:10],

            "city": city,

            "state": state,

            "country": "India",

            "date_of_birth": fake.date_between(
                start_date="-65y",
                end_date="-18y"
            ),

            "registration_date": fake.date_between(
                start_date="-5y",
                end_date="today"
            ),

            "customer_segment": segment,

            "annual_income": random.choice([
                "Low",
                "Middle",
                "Upper Middle",
                "High"
            ]),

            "preferred_channel": random.choice(channels),

            "preferred_payment": random.choice(payment_methods),

            "marketing_opt_in": random.choice(
                [True, True, True, False]
            ),

            "estimated_lifetime_value": round(
                random.uniform(min_ltv, max_ltv),
                2
            ),

            "loyalty_level": segment

        })

    df = pd.DataFrame(customers)

    # ---------------- Dirty Data ----------------

    df.loc[df.sample(frac=0.01).index, "email"] = None

    df.loc[df.sample(frac=0.005).index, "city"] = None

    df.loc[df.sample(frac=0.01).index, "first_name"] = (
        df["first_name"].str.upper()
    )

    df.loc[df.sample(frac=0.01).index, "last_name"] = (
        " " + df["last_name"] + " "
    )

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