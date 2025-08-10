from faker import Faker
import random


def get_faker(locale="en_US", seed=None):
    """
    Returns a Faker instance with optional locale and seed.
    """
    fake = Faker(locale)
    if seed is not None:
        Faker.seed(seed)
        random.seed(seed)
    return fake