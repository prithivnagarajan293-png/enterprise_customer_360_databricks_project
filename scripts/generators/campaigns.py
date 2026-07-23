import random
import pandas as pd

from faker import Faker

from utils.config import (
    NUM_CAMPAIGNS,
    BATCH_DATA_DIR
)

fake = Faker()


def generate_campaigns():

    campaign_types = [
        "Email",
        "SMS",
        "Social Media",
        "Festival Sale",
        "Loyalty"
    ]

    campaigns = []

    for i in range(1, NUM_CAMPAIGNS + 1):

        start = fake.date_between(
            start_date="-2y",
            end_date="today"
        )

        campaigns.append({

            "campaign_id": f"M{i:04d}",
            "campaign_name": fake.catch_phrase(),
            "campaign_type": random.choice(campaign_types),
            "budget": round(random.uniform(10000, 500000), 2),
            "start_date": start,
            "end_date": start + pd.Timedelta(days=random.randint(15, 60))

        })

    df = pd.DataFrame(campaigns)

    df.to_csv(
        BATCH_DATA_DIR / "marketing_campaigns.csv",
        index=False
    )

    print(f"Campaigns generated : {len(df):,}")