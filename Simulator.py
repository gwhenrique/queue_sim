from congruente.congruentialLinearGenerator import CongruentialLinearGenerator as clg
from RandomException import OutOfRandomsError
from PriorityQueue import PriorityQueue
from ScheduleTable import ScheduleTable
from OutputHandler import OutputHandler
import time

ARRIVAL   = 'arrival'
DEPARTURE = 'departure'
PASSING   = 'passing'

EXIT      = 'SYSTEM_EXIT'
INFINITE  = -1

class Simulator:
    """
    Class that simulates an execution on the system.
    """
    def __init__(self, queue, randoms):
        self.queues       = {}
        self.event_queue  = PriorityQueue()
        self.clg          = clg()
        self.output       = OutputHandler(queue)
        self.randoms      = randoms
        self.time         = 0.
        self.loss         = 0
        self.randoms_used = 0

    def reset_simulator(self):
        """
        After every seed change, the simulator needs to be reset.
        """
        del self.event_queue
        self.event_queue     = PriorityQueue()
        self.time            = 0.
        self.loss            = 0
        self.randoms_used    = 0
        for queue in self.queues:
            i_queue = self.queues[queue]
            i_queue.curr_size = 0
            del i_queue.schedule
            i_queue.schedule = ScheduleTable(i_queue.capacity)

    def add_queue(self, queue):
        self.queues[queue.name] = queue

    def _base_conversion(self, a, b, u):
        return (b - a) * u + a

    def _consume_random(self):
        if self.randoms_used < self.randoms:
            self.randoms_used += 1
            return self.clg.uniform()
        else:
            raise OutOfRandomsError

    def _arrival(self, arr_time, queue):
        """
        Arrival method

        First, update every queue schedule table

        Then the arrival algorithm is executed
        """
        queue = self.queues[queue]
        self.time = arr_time
        for q in self.queues:
            instanced_queue = self.queues[q]
            instanced_queue.register_event(arr_time, 'arrival', arriving_queue=instanced_queue.name, departing_queue=None)
        if queue.curr_size < queue.capacity or queue.capacity == INFINITE:
            queue.curr_size += 1
            if queue.curr_size <= queue.servers:
                self._define_next_event(queue)
        else:
            self.loss += 1
        next_arr = self._get_next_arrival_time(queue)
        # add a new event to the priority queue
        self.event_queue.insert_event('arrival', arr_time + next_arr, arriving_queue=queue.name)

    def _passing(self, pass_time, departing_queue, arriving_queue):
        """
        A method that simulates a transfer from one queue to another

        Register the current state of the system in every schedule table

        After that, the default algorithm is executed
        """
        departing_queue = self.queues[departing_queue]
        arriving_queue = self.queues[arriving_queue]
        self.time = pass_time
        for queue in self.queues:
            instanced_queue = self.queues[queue]
            instanced_queue.register_event(pass_time, 'passing', departing_queue, arriving_queue)
        departing_queue.curr_size -= 1
        if departing_queue.curr_size >= departing_queue.servers:
            self._define_next_event(departing_queue)
        if arriving_queue.curr_size < arriving_queue.capacity or arriving_queue.capacity == INFINITE:
            arriving_queue.curr_size += 1
            if arriving_queue.curr_size <= arriving_queue.servers:
                self._define_next_event(arriving_queue)
        else:
            self.loss += 1



    def _departure(self, dep_time, queue):
        """
        Method to simulate a departure of a queue

        :param Queue queue: the departing queue
        :param float dep_time: current simulation time
        """
        queue = self.queues[queue]
        self.time = dep_time
        for q in self.queues:
            instanced_queue = self.queues[q]
            instanced_queue.register_event(dep_time, 'departure', departing_queue=queue.name, arriving_queue=None)
        queue.curr_size -= 1
        if queue.curr_size >= queue.servers:
            self._define_next_event(queue)

    def _define_next_event(self, queue):
        """
        This method chooses which event should be inserted on the event scheduler.

        :param Queue queue: the departing queue who the event will leave
        """

        next_time = self._get_next_departure_time(queue)
        # add a new event to the priority queue
        next = self._select_next_queue(queue)
        if next == EXIT:
            self.event_queue.insert_event('departure', self.time + next_time, departing_queue=queue.name)
        else:
            self.event_queue.insert_event('passing', self.time + next_time, departing_queue=queue.name, arriving_queue=next)


    def _select_next_queue(self, queue):
        """
        Method that decides if a passing or a departure event should be executed.
        This method consumes a random number to choose que next queue the event will
        pass. the exit is also being considered a queue here.


        :param Queue queue: the departing queue

        :return: the name of the next queue, which can be either a queue name or the constant SYSTEM_EXIT
        """

        random = self._consume_random()
        c_prob = 0
        name = ''
        for q in queue.connections:
            prob = q[1]
            c_prob += prob
            if random < c_prob:
                name = q[0]
                return name
        if name == '':
            return EXIT


    def simulate(self, seed, first_arrivals):
        """
        Main simulation method.

        sets a seed, inserts the initial events and then simulates until the maximum number
        of randoms was used (indicated with a OutOfRandomsError)

        In the error handling, every last state computed for the queues is added to an OutputHandler,
        that will later handle all of the final states to generate an output.
        """
        self.clg.set_seed(seed)
        for queue in first_arrivals:
            arr_time = first_arrivals[queue]
            self.event_queue.insert_event('arrival', arr_time, arriving_queue=queue)
        try:
            while True:
                ev = self.event_queue.pop()
                if ev.event_type == ARRIVAL:
                    self._arrival(ev.time, ev.arriving_queue)
                elif ev.event_type == PASSING:
                    self._passing(ev.time, ev.departing_queue, ev.arriving_queue)
                else:
                    self._departure(ev.time, ev.departing_queue)
        except OutOfRandomsError:
            final_states = {}
            for queue in self.queues:
                final_states[queue] = self.queues[queue].get_last()
            self.output.add_final_state(final_states, self.loss, self.time)

    def get_averages(self):
        """
        Method to get the results of the simulations
        """
        return self.output.get_averages()

    def _get_next_arrival_time(self, queue):
        min_arr      = queue.min_arrival
        max_arr      = queue.max_arrival
        next_arrival = self._base_conversion(min_arr, max_arr, self._consume_random())

        return next_arrival

    def _get_next_departure_time(self, queue):
        min_dep        = queue.min_service
        max_dep        = queue.max_service
        next_departure = self._base_conversion(min_dep, max_dep, self._consume_random())

        return next_departure
