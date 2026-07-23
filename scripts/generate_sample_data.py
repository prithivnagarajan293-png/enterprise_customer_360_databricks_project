from utils.config import RANDOM_SEED
from utils.helpers import initialize_seed
from generators.products import generate_products

from generators.customers import generate_customers


def main():

    initialize_seed(RANDOM_SEED)

    print("=" * 60)
    print("RetailMart Enterprise Dataset Generator")
    print("=" * 60)

    generate_customers()
    generate_products()

    print()
    print("Generation Complete.")


if __name__ == "__main__":
    main()