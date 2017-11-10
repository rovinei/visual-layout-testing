from __future__ import (unicode_literals, absolute_import)

import random
import string
from datetime import datetime
today = datetime.today()


def generate_random_string(length, **kwargs):
    if 'mix' in kwargs and kwargs[str('mix')] is True:
        characters = string.ascii_letters + string.digits
    elif 'only_lower' in kwargs and kwargs[str('only_lower')] is True:
        characters = string.ascii_lowercase
    elif 'only_upper' in kwargs and kwargs[str('only_upper')] is True:
        characters = string.ascii_uppercase
    elif 'only_digit' in kwargs and kwargs[str('only_digit')] is True:
        characters = string.digits
    else:
        characters = string.ascii_letters + string.digits

    return ''.join(random.choice(characters) for x in range(length))


def upload_screenshot(instance, filename):
    file_name = generate_random_string(32, only_lower=True) + "-" + str(filename).replace(' ', '-').lower() + ".png"
    return "{}/{}/{}".format(
        'screenshot',
        today.strftime('%Y/%m'),
        file_name
    )
