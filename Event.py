class Event:
    """
    Events class
    """
    def __init__(self, event_type, time, arriving_queue=None, departing_queue=None):
        self.time            = time
        self.event_type      = event_type
        self.arriving_queue  = arriving_queue
        self.departing_queue = departing_queue

    def __str__(self):
        return 'event of type {0} @ {1}: {2} -> {3}'.format(self.event_type, self.time, self.departing_queue, self.arriving_queue)

    def _cmp(self, other):
        return self.time - other.time

    #comparison methods
    def __lt__(self, other):
        return self._cmp(other) < 0

    def __le__(self, other):
        return self._cmp(other) <= 0

    def __eq__(self, other):
        return self._cmp(other) == 0

    def __ne__(self, other):
        return self._cmp(other) != 0

    def __gt__(self, other):
        return self._cmp(other) > 0

    def __ge__(self, other):
        return self._cmp(other) >= 0
