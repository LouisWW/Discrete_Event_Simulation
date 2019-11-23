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

n_server = 2
mu = 0.50
l = 0.48
endtime = 5000
n_simulations = 1500
sjf = False # use shortest job first


list_average_queuelength = []
list_average_queuingtimes = []
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
    list_average_queuelength.append(average_queuelength)

    average_queuingtimes = np.average(global_variables.time_spend_in_queue_list)
    list_average_queuingtimes.append(average_queuingtimes)

    print("Now at simulation {}".format(i))


########################################################################################################

# plot the distribution of the average queueing times
onesim_queueingtimes = plt.figure()
entries, bin_edges, patches = plt.hist(global_variables.time_spend_in_queue_list, bins=100, normed=True)
plt.title("The distribution of queueing times", fontsize=14)
plt.xlabel("Queueing times (a.u.)", fontsize=20)
plt.ylabel("Occurrence (#)", fontsize=20)
plt.savefig("onesim_queueingtimes_distribution.png", dpi=300)

########################################################################################################


# plot the distribution of the average queue lengths
plt.figure()
entries, bin_edges, patches = plt.hist(list_average_queuelength, bins = 100, normed=True)
plt.title("The distribution of the average queue lengths\n of the different simulations", fontsize=14)
plt.xlabel("Average queueing lengths (#)", fontsize=20)
plt.ylabel("Occurrence (#)", fontsize=20)
# fit poisson distribution to data
# x_plot = np.linspace(1, 60, 1000)
# plt.plot(x_plot, poisson_fit(entries, bin_edges, x_plot), 'r-', lw=2)


########################################################################################################

# plot the distribution of servicing times
plt.figure()
plt.title("A histogram of the time helping costs \n of one simulation")
plt.ylabel("Occurrence (#)", fontsize=20)
plt.xlabel("Helping times (a.u.)", fontsize=20)
plt.hist(global_variables.list_helptime)

########################################################################################################

# plot the distribution of the interarrival times
plt.figure()
plt.title("A histogram of the time inbetween arrivals of tasks")
plt.ylabel("Occurrence (#)", fontsize=20)
plt.xlabel("Inter-arrival times (a.u.)", fontsize=20)
plt.hist(global_variables.list_arrivaltime)

########################################################################################################


# plot the queue length at different times
plt.figure()
plt.title("Queue length versus time")
plt.ylabel("Queue length (#)", fontsize=20)
plt.xlabel("Time (a.u.)", fontsize=20)
plt.plot(global_variables.queue_time_list, global_variables.queue_length_list)

########################################################################################################

plt.figure()
entries, bin_edges, patches = plt.hist(list_average_queuingtimes, bins = 100)
plt.title("The distribution of the average waiting times\n of the different simulations", fontsize=14)
plt.xlabel("Average queueing times (#)", fontsize=20)
plt.ylabel("Occurrence (#)", fontsize=20)
# x_plot = np.linspace(0, 60, 1000)
# plt.plot(x_plot, poisson_fit(entries, bin_edges, x_plot), 'r-', lw=2)


########################################################################################################



plt.show()

