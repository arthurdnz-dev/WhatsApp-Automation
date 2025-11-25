import random
import time

def human_delay():
    base = random.uniform(2.5, 4.5)
    jitter = random.uniform(0.1, 0.8)
    delay = base + jitter
    time.sleep(delay)
    return delay
