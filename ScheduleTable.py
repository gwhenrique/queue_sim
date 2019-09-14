import pandas as pd
from Event import Event

class ScheduleTable:
    """
    Class that implements an event execution table.
    """
    def __init__(self, capacity):
        self.cols = ['Event', 'Size', 'Arriving Queue', 'Departing Queue', 'Time']
        self.mapping = {}
        self.table = []
        if capacity < 0:
            capacity = 0
        null_ev = ['None', 0, None, None, 0]
        for i in range(0, capacity+1):
            # print('APPENDING '+str(i))
            self.cols.append(i)
            null_ev.append(0.)
        i = 0
        for col in self.cols:
            self.mapping[col] = i
            i += 1
        self.table.append(null_ev)

    def register_event(self, time, event_type, curr_size, arriving_queue=None, departing_queue=None):
        """
        When registering an event on the table, some tricky things must be done:
        First, it gets the last event and alters time, event type, current queue size
        and queues that were affected.

        Second, it needs to check if the current state already exists on the last event.
        Since a queue can be infinite, it is not guaranteed that the current state has happened
        before.
        """
        # print(len(self.table), 'TABLE LEN')
        # print(time, event_type, curr_size, arriving_queue, departing_queue)
        last_event = self.table[-1]
        last_time = last_event[self.mapping['Time']]
        elapsed_time = time - last_time
        self.table.append(self.table[-1])
        self.table[-1][self.mapping['Event']] = event_type
        self.table[-1][self.mapping['Size']] = curr_size
        self.table[-1][self.mapping['Time']] = time
        self.table[-1][self.mapping['Arriving Queue']] = arriving_queue
        self.table[-1][self.mapping['Departing Queue']] = departing_queue
        if curr_size not in self.mapping:
            # print(curr_size, 'not in', self.mapping)
            self.mapping[curr_size] = self.mapping[curr_size-1]+1
            self.table[-1].append(0.)
        # print(self.mapping[curr_size])
        # print(self.table[-1])
        self.table[-1][self.mapping[curr_size]] += elapsed_time

    def get_last(self):
        return self.table[-1]
