from functions import *
from global_variables import init_global


import simpy
import matplotlib.pyplot as plt
import random as rd
import numpy as np
import os
from scipy.optimize import curve_fit
from scipy.special import factorial

n_server = 1
mu = 0.80
l = 0.64
end_n_actions = 12000
batch_size = 8000
initialisation_period = 10000
n_simulations = 1
n_batches = (end_n_actions-initialisation_period)/batch_size/2.
print("this is the number of batches", n_batches)
sjf = False  # use shortest job first
db_helptime = "LT"  # choice between M, D, LT
LT_values = [1, 1.5, 3, 4, 5]

list_average_queuelength = []
list_average_queuingtimes = []
all_queue_lengths_overtime = np.zeros((len(LT_values), end_n_actions+1))

# run the simulation multiple times
i = 0
for LT_value in LT_values:

    # initialize the global lists
    init_global(end_n_actions)

    # create a simpy environment
    env = simpy.Environment()

    # set up the system
    env.process(setup(env, n_server, mu, l, sjf, end_n_actions, db_helptime, LT_value))

    # run the program
    env.run()
    # print("The number of measurements: ", len(global_variables.queue_length_list))

    average_queuelength = np.average(global_variables.queue_length_list)
    list_average_queuelength.append(average_queuelength)

    list_batch_averages = batch_averages(batch_size, initialisation_period)
    average_queuingtimes = np.average(global_variables.time_spend_in_queue_list)
    list_average_queuingtimes.append(average_queuingtimes)

    all_queue_lengths_overtime[i] = global_variables.queue_length_list

    i += 1
    print("Now at simulation {}".format(i))

# calculate the variance
standard_deviation, confidence_interval = calc_varci(list_batch_averages, n_batches)

########################################################################################################

print("The average queueing time is {} +- {}".format(np.average(list_batch_averages), confidence_interval))

# plot the queue length over time
plt.figure()
plt.plot(global_variables.queue_time_list, np.transpose(all_queue_lengths_overtime))
plt.legend(LT_values)
ax = plt.gca()
plt.xlabel("Time (a.u.)", fontsize=16, fontweight='bold')
plt.ylabel("Queue length (# of tasks)", fontsize=16, fontweight='bold')
ax.xaxis.set_tick_params(labelsize=14)
ax.yaxis.set_tick_params(labelsize=14)
plt.show()


