from pathlib import Path

# -----------------------------
# Project Paths
# -----------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[2]

BATCH_DATA_DIR = PROJECT_ROOT / "sample_data" / "batch"

STREAMING_DATA_DIR = PROJECT_ROOT / "sample_data" / "streaming" / "events"

# -----------------------------
# Dataset Sizes
# -----------------------------

NUM_CUSTOMERS = 10_000
NUM_PRODUCTS = 1_000
NUM_STORES = 50
NUM_EMPLOYEES = 500
NUM_CAMPAIGNS = 100
NUM_ORDERS = 100_000
AVG_ITEMS_PER_ORDER = 3.5

# -----------------------------
# Random Seed
# -----------------------------

RANDOM_SEED = 42