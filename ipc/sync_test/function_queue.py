import time


class FunctionQueue:
    def __init__(self):
        self.queue = []

    def enqueue(self, func, timestamp=None, *args, **kwargs):
        if timestamp is None:
            timestamp = time.time()
        self.queue.append((timestamp, func, args, kwargs))

    def execute(self):
        self.queue.sort()
        for _, func, args, kwargs in self.queue:
            if func != None:
                func(*args, **kwargs)
