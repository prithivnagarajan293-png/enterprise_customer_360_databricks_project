from utils.config import RANDOM_SEED
from utils.helpers import initialize_seed
from generators.products import generate_products
from generators.stores import generate_stores
from generators.employees import generate_employees
from generators.campaigns import generate_campaigns
from generators.orders import generate_orders
from generators.order_items import generate_order_items

from generators.customers import generate_customers


def main():

    initialize_seed(RANDOM_SEED)

    print("=" * 60)
    print("RetailMart Enterprise Dataset Generator")
    print("=" * 60)

    generate_customers()
    generate_products()
    generate_stores()
    generate_employees()
    generate_campaigns()
    generate_orders()
    generate_order_items()

    print()
    print("Generation Complete.")


if __name__ == "__main__":
    main()