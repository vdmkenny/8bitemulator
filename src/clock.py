import time

class Clock:
    def __init__(self, hertz):
        self.hertz = hertz
        self.period = 1 / hertz
        self.last_tick = time.time()

    def tick(self):
        now = time.time()
        time_since_last_tick = now - self.last_tick
        if time_since_last_tick >= self.period:
            self.last_tick = now
            return True
        else:
            return False
