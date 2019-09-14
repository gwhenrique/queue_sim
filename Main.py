import OutputHandler, json
from Queue import Queue
from Simulator import Simulator
import JSONHandler
import sys

def main(json_name):
    """
    Main method

    Starts parsing the JSON and creating the network with the help of JSONHandler

    Created the simulator

    Executes a simulation for every seed

    Prints results
    """
    queues, first_arrivals, n_randoms, seeds = JSONHandler.open_json(json_name)
    sim = Simulator(queues, n_randoms)
    for queue in queues:
        sim.add_queue(queue)
    for seed in seeds:
        print('Simulating seed {0}...'.format(seed))
        sim.simulate(seed, first_arrivals)
        sim.reset_simulator()
    print(sim.get_averages())



if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python Main.py <json_file>")
        sys.exit(-1)
    main(sys.argv[1])
