from functions import *
from packages import *

import_packages()

import simpy
import random as rd
import numpy as np
import os

n_server  = 1
mu = 1
l = 1
endtime = 15
# create a simpy environment
env = simpy.Environment()

# set up the system
env.process(setup(env, n_server, mu, l))

# run the program
env.run(until=endtime)

