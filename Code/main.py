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

n_server  = 1
mu = 0.5
l = 0.48
endtime = 10000

init_global()

# create a simpy environment
env = simpy.Environment()

# set up the system
env.process(setup(env, n_server, mu, l))

# run the program
env.run(until=endtime)

print(global_variables.list_helptime)
print(global_variables.list_arrivaltime)

plt.figure()
plt.title("A histogram of the time helping costs")
plt.hist(global_variables.list_helptime)
plt.show()

plt.figure()
plt.title("A histogram of the time inbetween arrivals of tasks")
plt.hist(global_variables.list_arrivaltime)
plt.show()

plt.figure()
plt.title("Queue length versus time")
plt.plot(global_variables.queue_time_list, global_variables.queue_length_list)
plt.show()
