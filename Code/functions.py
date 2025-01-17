# Test #

import simpy
import random as rd
import numpy as np
import global_variables
import os
from scipy.optimize import curve_fit
from scipy.special import factorial
import random as rd


class Serversystem(object):
    "A server has n desks at which tasks can be carried out, if all desks are in use, a task has to wait"

    def __init__(self, env, n_server, mu):
        self.env = env
        self.server = simpy.PriorityResource(env, n_server)
        self.mu = mu  # the average help time is 1/mu, so need to incorporate that

    def help(self, task, helptime):
        yield self.env.timeout(helptime)  # randomness needs to be added here


def task(env, name, ss, mu, sjf, db_helptime, counter, LT_value):
    "A task process that will be carried out by a serversystem (ss) after having waited for a server to become available"
    # wait for server to become available
    global_variables.queue_length += 1
    global_variables.queue_length_list[counter] = global_variables.queue_length
    global_variables.queue_time_list[counter] = env.now

    # calculate how long helping is going to take
    if db_helptime == "M":
        helptime = np.random.exponential(1/mu)  # generates pdf mu * exp(-mu*x)
    if db_helptime == "D":
        helptime = 1/mu
    if db_helptime == "LT":
        if np.random.rand() < 0.75:
            helptime = np.random.exponential(1)  # average helptime of 1.0
            print("this mu = 1")
        else:
            helptime = np.random.exponential(LT_value)  # average helptime of 5.
            print("this mu = 0.2")

    # append the helptime of a task to a global list
    global_variables.list_helptime[counter] = helptime

    # set priority for different tasks
    if sjf:
        prio = int(helptime * 1000)  # request only integers
    else:
        prio = 0

    # put in request to be serviced
    with ss.server.request(prio) as request:
        time_before = env.now
        yield request
        global_variables.time_spend_in_queue_list[counter] = env.now - time_before

        # wait until someone moves out of the queue
        yield env.process(ss.help(name, helptime))
        global_variables.queue_length -= 1


# this function creates the serversystem and produces the tasks
def setup(env, n_server, mu, l, sjf, end_n_actions, db_helptime, LT_value):
    serversystem = Serversystem(env, n_server, mu)

    counter = 0

    # create task until the simulation time is over
    while True:

        # calculate the arrival time for the next task
        arrivaltime = np.random.exponential(1/l)  # generates pdf l * exp(-l*x)

        # append the arrival time to a global list
        global_variables.list_arrivaltime[counter]=arrivaltime

        # wait until new task arrives
        yield env.timeout(arrivaltime) # arrival time needs to be made random

        counter += 1
        task_ref = env.process(task(env, 'Task{}'.format(counter), serversystem, mu, sjf, db_helptime, counter, LT_value))

        # if certain number of tasks is produced, quit
        print(counter)
        if counter == end_n_actions:
            yield task_ref
            break


def batch_averages(batch_size, initialisation_period):
    shortened_queuing_times = global_variables.time_spend_in_queue_list[initialisation_period:-1]
    list_batch_averages = []
    for i in range(0, len(shortened_queuing_times)/batch_size,2):
        list_batch_averages.append(np.average(shortened_queuing_times[i*batch_size:(i+1)*batch_size]))

    return list_batch_averages


def calc_varci(list_batch_averages, n_batches):
    variance = 1 / (n_batches - 1) * np.sum((list_batch_averages - np.average(list_batch_averages)) ** 2)
    standard_deviation = np.sqrt(variance)
    confidence_interval = 1.96 * variance/np.sqrt(n_batches)

    return standard_deviation, confidence_interval
