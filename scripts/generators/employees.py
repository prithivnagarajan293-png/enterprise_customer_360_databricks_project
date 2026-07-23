import random
import pandas as pd

from faker import Faker

from utils.config import (
    NUM_EMPLOYEES,
    NUM_STORES,
    BATCH_DATA_DIR
)

fake = Faker()


def generate_employees():

    employees = []

    roles = [
        "Cashier",
        "Sales Associate",
        "Store Manager",
        "Supervisor",
        "Inventory Executive"
    ]

    for i in range(1, NUM_EMPLOYEES + 1):

        employees.append({

            "employee_id": f"E{i:05d}",
            "first_name": fake.first_name(),
            "last_name": fake.last_name(),
            "store_id": f"S{random.randint(1, NUM_STORES):03d}",
            "role": random.choice(roles),
            "hire_date": fake.date_between(
                start_date="-10y",
                end_date="today"
            )

        })

    df = pd.DataFrame(employees)

    df.to_csv(
        BATCH_DATA_DIR / "employees.csv",
        index=False
    )

    print(f"Employees generated : {len(df):,}")