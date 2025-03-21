import random

def generate_random_color():
    color = "#{:06x}".format(random.randint(0, 0xFFFFFF))
    return color