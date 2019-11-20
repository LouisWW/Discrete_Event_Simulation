# Test #

import simpy
import random as rd
import numpy as np
import os

class Serversystem(object):
    "A server has n desks at which tasks can be carried out, if all desks are in use, a task has to wait"

    def __init__(self, env, n_server, mu):
        self.env = env
        self.server = simpy.Resource(env, n_server)
        self.mu = mu # the average help time is 1/mu, so need to incorporate that

    def help(self, task, helptime):
        yield self.env.timeout(helptime) # randomness needs to be added here
        print("Carrying out the task took {}".format(self.env.now))


def task(env, name, ss, mu):
    "A task process that will be carried out by a serversystem (ss) after having waited for a server to become available"
    with ss.server.request() as request:

        # wait for server to become available
        yield request
        print("{} started by server at {}".format(name, env.now))

        # wait for task to be finished
        t = rd.random()
        helptime = mu * np.exp(-mu * t)

        yield env.process(ss.help(name, helptime))
        print("{} carried out by server at {}".format(name, env.now))

def setup(env, n_server, mu, l):
    '''Here we create a server system with a certain number of servers. We start creating cars at random'''
    serversystem = Serversystem(env, n_server, mu)

    list_arrival = []

    i = 0
    # create task until the simulation time is over
    while True:
        t = rd.random()
        arrivaltime = 1 - np.exp(-l * t)
        list_arrival.append(arrivaltime)
        # wait until new task arrives
        yield env.timeout(arrivaltime) # arrival time needs to be made random
        i += 1
        env.process(task(env, 'Task{}'.format(i), serversystem, mu))

        print(list_arrival)

        if False:
            yield list_arrival
            return






