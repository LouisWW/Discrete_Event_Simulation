from functions import *
from packages import *
from global_variables import init_global

# initialize global variables, probably also an idea for the other variables that need to be used
import_packages()

import simpy
import matplotlib.pyplot as plt
import random as rd
import numpy as np
import os

n_server = 2
mu = 0.25
l = 0.48
endtime = 5000
n_simulations = 1
sjf = False # use shortest job first


list_average_queuelength = []
# run the simulation multiple times
for i in range(n_simulations):

    # initialize the global lists
    init_global()

    # create a simpy environment
    env = simpy.Environment()

    # set up the system
    env.process(setup(env, n_server, mu, l, sjf))

    # run the program
    env.run(until=endtime)

    average_queuelength = np.average(global_variables.queue_length_list)
    print(average_queuelength)
    list_average_queuelength.append(average_queuelength)

# plot the distribution of the average queueing times
plt.figure()
plt.hist(global_variables.time_spend_in_queue_list, bins = 100)
plt.title("The distribution of the average time spend in a queue")

# plot the distribution of the average queue lengths
plt.figure()
plt.hist(list_average_queuelength, bins = 100)
plt.title("The distribution of the average queue lengths of the different simulations")

# plot the distribution of servicing times
plt.figure()
plt.title("A histogram of the time helping costs")
plt.hist(global_variables.list_helptime)

# plot the distribution of the interarrival times
plt.figure()
plt.title("A histogram of the time inbetween arrivals of tasks")
plt.hist(global_variables.list_arrivaltime)

# plot the queue length at different times
plt.figure()
plt.title("Queue length versus time")
plt.plot(global_variables.queue_time_list, global_variables.queue_length_list)
plt.show()

