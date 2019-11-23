# Test #

import simpy
import random as rd
import numpy as np
import global_variables
import os
from scipy.optimize import curve_fit
from scipy.special import factorial

class Serversystem(object):
    "A server has n desks at which tasks can be carried out, if all desks are in use, a task has to wait"

    def __init__(self, env, n_server, mu):
        self.env = env
        self.server = simpy.PriorityResource(env, n_server)
        self.mu = mu # the average help time is 1/mu, so need to incorporate that

    def help(self, task, helptime):
        yield self.env.timeout(helptime) # randomness needs to be added here
        #print("Carrying out the task took {}".format(self.env.now))


def task(env, name, ss, mu, sjf):
    "A task process that will be carried out by a serversystem (ss) after having waited for a server to become available"
    # wait for server to become available
    global_variables.queue_length += 1
    global_variables.queue_length_list.append(global_variables.queue_length)
    global_variables.queue_time_list.append(env.now)

    # calculate how long helping is going to take
    helptime = np.random.exponential(1 / mu)

    # append the helptime of a task to a global list
    global_variables.list_helptime.append(helptime)

    if sjf:
        prio = int(helptime * 1000)
    else:
        prio = 0

    with ss.server.request(prio) as request:
        time_before = env.now
        yield request
        #print("{} started by server at {}".format(name, env.now))
        global_variables.time_spend_in_queue_list.append(env.now - time_before)

        # wait until someone moves out of the queue
        yield env.process(ss.help(name, helptime))
        global_variables.queue_length -= 1
        #print("{} carried out by server at {}".format(name, env.now))

def setup(env, n_server, mu, l, sjf):
    '''Here we create a server system with a certain number of servers. We start creating cars at random'''
    serversystem = Serversystem(env, n_server, mu)

    i = 0
    # create task until the simulation time is over
    while True:

        # calculate the arrival time for the next task
        arrivaltime = np.random.exponential(1/l)

        # append the arrival time to a global list
        global_variables.list_arrivaltime.append(arrivaltime)

        # wait until new task arrives
        yield env.timeout(arrivaltime) # arrival time needs to be made random
        i += 1
        env.process(task(env, 'Task{}'.format(i), serversystem, mu, sjf))


# poisson function, parameter lamb is the fit parameter
def poisson(k, lamb, scale):
    return scale*(lamb**k/factorial(k))*np.exp(-lamb)


def poisson_fit(entries, bin_edges, x_plot):
    # calculate binmiddles
    bin_middles = 0.5 * (bin_edges[1:] + bin_edges[:-1])
    # fit with curve_fit
    parameters, cov_matrix = curve_fit(poisson, bin_middles, entries, p0=[0.5, 50])
    # plot poisson-deviation with fitted parameter
    return poisson(x_plot, *parameters)




