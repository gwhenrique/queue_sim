import Event
from ScheduleTable import ScheduleTable


class Queue:
    """
    Simple queue class
    """
    def __init__(self, name, servers, capacity, min_arrival, max_arrival, min_service, max_service):
        self.name        = name
        self.servers     = servers
        self.capacity    = capacity
        self.schedule    = ScheduleTable(capacity)
        self.curr_size   = 0
        self.min_arrival = min_arrival
        self.max_arrival = max_arrival
        self.min_service = min_service
        self.max_service = max_service
        self.connections = []

    def add_connection(self, queue, routing_prob):
        self.connections.append((queue, routing_prob))

    def get_last(self):
        return self.schedule.get_last()[5:]

    def register_event(self, time, ev_type, arriving_queue, departing_queue):
        self.schedule.register_event(time, ev_type, self.curr_size, arriving_queue, departing_queue)

    def __str__(self):
        return 'Queue {0}:\n\tCapacity: {1}\n\tServers: {2}\n\tArr: {3}~{4}\n\tService: {5}~{6}'.format(
            self.name, self.capacity, self.servers, self.min_arrival, self.max_arrival,
            self.min_service, self.max_service
        )
