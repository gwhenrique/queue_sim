from Event import Event
from bisect import bisect

class PriorityQueue:

    """
    Class that simulates an ordered event queue.
    """
    def __init__(self):
        self.queue = []
        self.count = 0



    def insert_event(self, ev_type, time, departing_queue=None, arriving_queue=None):
        event = Event(ev_type, time,
                      departing_queue=departing_queue,
                      arriving_queue=arriving_queue)
        i = bisect(self.queue, event)
        self.queue.insert(i, event)
        self.count += 1

    def pop(self):
        return self.queue.pop(0)

    def __str__(self):
        result = ''
        for e in self.queue:
            result += str(e)
        return result
