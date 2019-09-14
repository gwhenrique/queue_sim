class OutputHandler:
    def __init__(self, queues):
        self.final_states = {}
        for q in queues:
            self.final_states[q.name] = []
        self.loss = []
        self.total_time = []

    def add_final_state(self, states, loss, total_time):
        for key in self.final_states:
            self.final_states[key].append(states[key])
        # self.final_states.append(state[2:])
        self.loss.append(loss)
        self.total_time.append(total_time)

    def get_averages(self):
        """
        Method that calculates the averages of every queue


        """
        result = '\n\n\nRESULTS:\n\n'
        total_loss = sum(self.loss)
        av_loss = round(total_loss/len(self.loss))
        av_time = round(sum(self.total_time)/len(self.total_time), 4)
        # total_time = round(averages[0], 4)
        result += 'Time average: {0}\n'.format(str(av_time))
        result += 'Total loss: {0}\n'.format(str(total_loss))
        result += 'Average loss: {0}\n'.format(str(av_loss))
        queue_ordered = list(self.final_states.keys())
        queue_ordered.sort()
        for queue in queue_ordered:
            result += '\nQueue {0}:\n'.format(queue)
            states = self.final_states[queue]
            states = self._normalize_size(states)
            averages = [sum(zipped_state)/len(states) for zipped_state in zip(*states)]
            i = 0
            for st_av in averages:
                result += '\tAverage of state {0}: {1} - '.format(str(i), str(round(st_av, 4)))
                percent = round(st_av/av_time*100, 4)
                result += '{0} % of time\n'.format(str(percent))
                i += 1
        return result

    def _normalize_size(self, states):
        """
        Method that normalizes state size of queues, in case some queue has infinite capacity,
        which means that it isn't guaranteed that the highest queue size is equal for every seed
        """
        max_size = 0
        for l in states:
            if len(l) > max_size:
                max_size = len(l)
        for l in states:
            while len(l) < max_size:
                l.append(0.)
        return states
