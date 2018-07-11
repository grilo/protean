#!/usr/bin/env python

import time
import random

import protean
from protean.decorators import *

@counter('a_special_counter', 'a description')
def something(*args):
    return 10

@histogram('anhistogram', [25, 50, 100])
def histo():
    time.sleep(random.randint(1, 4))
    return random.randint(1, 100)

@histogram('abb_anhistogram', [25, 50, 100])
def anotherhisto():
    time.sleep(random.randint(1, 4))
    return random.randint(1, 100), {'hello': 'world'}


protean.start()
