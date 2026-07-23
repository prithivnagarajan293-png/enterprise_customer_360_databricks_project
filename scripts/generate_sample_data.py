from utils.config import RANDOM_SEED
from utils.helpers import initialize_seed

def main():

    initialize_seed(RANDOM_SEED)

    print("=" * 60)
    print("RetailMart Enterprise Dataset Generator")
    print("=" * 60)
    print("Seed initialized successfully.")
    print()
    print("Dataset generation will begin in the next sprint.")

if __name__ == "__main__":
    main()