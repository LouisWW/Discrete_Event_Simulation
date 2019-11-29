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
from scipy.optimize import curve_fit
from scipy.special import factorial

n_server = 1
mu = 0.80
l = 0.64
end_n_actions = 60000
repetitions = 30
initialisation_period = 10000
n_simulations = 1
LT_value = 5
sjf = False  # use shortest job first

list_average_queuelength = []
list_average_queuingtimes = []
list_stddev = []

diff_batchsizes = np.arange(1,30000,6000)

# run the simulation multiple times
for i in diff_batchsizes:
    total_standard_deviation = 0
    for j in range(repetitions):
        print("current batch size: ", i)
        print("current repetition: ", j)
        n_batches = (end_n_actions - initialisation_period) / i / 2.

        # initialize the global lists
        init_global()

        # create a simpy environment
        env = simpy.Environment()

        # set up the system
        env.process(setup(env, n_server, mu, l, sjf, end_n_actions, "M", LT_value))

        # run the program
        env.run()
        # print("The number of measurements: ", len(global_variables.queue_length_list))

        average_queuelength = np.average(global_variables.queue_length_list)
        list_average_queuelength.append(average_queuelength)

        list_batch_averages = batch_averages(i, initialisation_period)
        average_queuingtimes = np.average(global_variables.time_spend_in_queue_list)
        list_average_queuingtimes.append(average_queuingtimes)

        variance = 1 / (n_batches - 1) * np.sum((list_batch_averages - np.average(list_batch_averages))**2)
        total_standard_deviation += np.sqrt(variance)
    list_stddev.append(total_standard_deviation/repetitions)

# np.save(list_stddev, "list_stddev")
# np.save(diff_batchsizes, "diff_batchsizes")

plt.figure()
ax = plt.gca()

plt.plot(diff_batchsizes, list_stddev, linewidth=3)
plt.xlabel("batch size (#)", fontsize=16, fontweight='bold')
plt.ylabel("standard deviation (a.u.)", fontsize=16, fontweight='bold')
ax.xaxis.set_tick_params(labelsize=14)
ax.yaxis.set_tick_params(labelsize=14)
plt.show()
########################################################################################################
