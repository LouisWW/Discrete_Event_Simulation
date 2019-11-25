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
endtime = 8000
n_simulations = 1500
sjf = False  # use shortest job first

'''Run simulation for different values of rho'''
list_nf_confidence_average_queuetimes = []
list_total_average_queuetimes = []
mu_range = np.arange(l+0.01, 0.8, 0.03)
for mu in mu_range:
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

    total_average_queuetimes = np.average(list_average_queuingtimes)
    list_total_average_queuetimes.append(total_average_queuetimes)
    variance_average_queuetimes = len(global_variables.queue_length_list) / (n_simulations - 1.) * sum((list_average_queuingtimes - total_average_queuetimes)**2)
    nf_confidence_average_queuetimes = 1.96 * np.sqrt(variance_average_queuetimes/n_simulations)
    list_nf_confidence_average_queuetimes.append(nf_confidence_average_queuetimes)

theoretical_waitingtime = (l/mu_range)/(l*(1.-(l/mu_range)**2))
print(l/mu_range)
print(l*(1.-(l/mu_range)**2))

plt.figure()
plt.errorbar(l/mu_range, list_total_average_queuetimes, nf_confidence_average_queuetimes)
plt.plot(l/mu_range, theoretical_waitingtime, 'r')
plt.title("Average queueing times versus rho")
plt.xlabel("value of rho (a.u.)", fontsize=16)
plt.ylabel("Average time spent in queue (a.u.)", fontsize=16)
plt.savefig("queueingtimedifferentrhoscomparison.png", dpi=300)


plt.show()