import json
import os
from time import sleep

import redis

from rgb_desk.desk import Desk
from rgb_desk.utils import conf


class Worker:
    """Worker to process the lighting jobs."""

    def __init__(self):
        """Construct."""
        self.redis = redis.Redis()

        desk_conf = conf["segments"]
        if "TEST_SEGMENTS" in os.environ:  # nocov
            desk_conf = json.loads(os.environ["TEST_SEGMENTS"])

        self.desk = Desk(desk_conf)

    def process(self, job):
        """Process a job."""
        try:
            args = json.loads(job.decode("utf-8"))
            self.desk.light_up(args["colour"], args)

        except json.decoder.JSONDecodeError:  # nocov
            print("Your data is bad")

    def poll(self):
        """If there's a job on the queue, pull it off and process it."""
        data = self.redis.lpop("jobs")
        if data:
            self.process(data)

        else:  # nocov
            sleep(conf["worker"]["interval"])

    def work(self):  # nocov
        """Keep working forever."""
        while True:
            self.poll()


if __name__ == "__main__":  # nocov
    print("worker starting")
    worker = Worker()
    worker.work()
