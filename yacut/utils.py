from string import ascii_letters, digits
from random import choices


def short_url_generator():
    return ''.join(choices(list(ascii_letters + digits), k=6))