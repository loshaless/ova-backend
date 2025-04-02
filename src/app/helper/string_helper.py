import string
import random

def generate_random_string(length):
    # Define the character set (letters, digits, and/or special characters)
    chars = string.ascii_letters + string.digits  # Add string.punctuation if you want special characters

    # Generate a random string of the specified length
    random_string = ''.join(random.choice(chars) for _ in range(length))

    return random_string