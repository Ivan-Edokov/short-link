from random import choices
from string import ascii_letters, digits


def short_url_generator():
    return ''.join(choices(list(ascii_letters + digits), k=6))