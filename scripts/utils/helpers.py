import random
import numpy as np

from faker import Faker

fake = Faker()

def initialize_seed(seed: int):
    random.seed(seed)
    np.random.seed(seed)
    Faker.seed(seed)