"""
Random Number List Generator
----------------------------
Creates a txt file with a list of random numbers
"""

import random

FILENAME = "random_numbers.txt"
NO_OF_NUMS = 100

def store_random_numbers(no, filename):
    """ Stores random numbers to a certain txt file """
    # create a new txt file
    f = open(filename, "w")

    # add 100 random numbers to the txt file
    for _ in range(100):
        random_number = random.randint(0, 100)
        f.write(str(random_number) + "\n")

    # close the file
    f.close()

if __name__ == "__main__":
    store_random_numbers(NO_OF_NUMS, FILENAME)