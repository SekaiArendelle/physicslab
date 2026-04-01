import os
import sys

SCRIPT_DIR: str = os.path.dirname(os.path.abspath(__file__))
PHYSICS_LAB_DIR: str = os.path.dirname(os.path.dirname(SCRIPT_DIR))
sys.path.append(PHYSICS_LAB_DIR)

from physicslab.web._threadpool import ThreadPool


def wait():
    while True:
        pass


if __name__ == "__main__":
    pool = ThreadPool(max_workers=4)
    task = pool.submit(wait)
    task.result()
