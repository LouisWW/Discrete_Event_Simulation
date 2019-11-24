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
mu = 0.50
l = 0.48
endtime = 8000
n_simulations = 100
sjf = False  # use shortest job first
main_program = False
different_rho_comparison = True

if main_program:
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

    total_average_queuelength = np.average(list_average_queuelength)
    variance_average_queuelength = 1. / (n_simulations - 1.) * sum(list_average_queuelength - total_average_queuelength)
    nf_confidence_average_queuelength = 1.96 * np.sqrt(variance_average_queuelength/n_simulations)
    print(nf_confidence_average_queuelength)

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

'''Run simulation for different values of rho'''
if different_rho_comparison:
    list_nf_confidence_average_queuetimes = []
    list_total_average_queuetimes = []
    mu_range = np.arange(l+0.01, 0.8, 0.04)
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
    plt.errorbar(mu_range, list_total_average_queuetimes, nf_confidence_average_queuetimes)
    plt.plot(mu_range, theoretical_waitingtime, 'r')
    plt.title("Average queueing times versus rho")
    plt.xlabel("value of mu (a.u.)", fontsize=20)
    plt.ylabel("Average time spent in queue (a.u.)", fontsize=20)
    plt.savefig("queueingtimedifferentrhoscomparison.png", dpi=300)


plt.show()