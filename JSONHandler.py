import json
from Queue import Queue

def open_json(json_name):
    with open(json_name, 'r') as f:
        return parse_network(json.load(f))



def parse_network(info):

    """
    JSON Parsing, creating the required network of queues.
    """

    curr_q_name = ''
    try:
        n_randoms = info['n_randoms']
        seeds = info['seeds']
        queues = []
        for queue in info['queues']:
            queues.append(parse_queue(queue))
        first_arrivals = {}
        for arrival in info['arrivals']:
            curr_q_name = arrival['name']
            arr_time = arrival['time']
            queue = [q for q in queues if q.name == arrival['name']]
            if len(queue) < 1:
                raise QueueDoesntExistError
            first_arrivals[curr_q_name] = arr_time
    except KeyError as err:
        print('ERROR! Expecting key {0}'.format(err.args[0]))
        exit(1)
    return queues, first_arrivals, n_randoms, seeds

def parse_queue(queue):
    if 'capacity' not in queue:
        queue['capacity'] = -1
    if 'min_arrival' not in queue:
        queue['min_arrival'] = None
    if 'max_arrival' not in queue:
        queue['max_arrival'] = None
    instanced_queue = Queue(
                    queue['name'],
                    queue['servers'], queue['capacity'],
                    queue['min_arrival'], queue['max_arrival'],
                    queue['min_service'], queue['max_service'])
    if 'connections' in queue:
        for connection in queue['connections']:
            name = connection['name']
            probability = connection['probability']
            instanced_queue.add_connection(name, probability)
    return instanced_queue
