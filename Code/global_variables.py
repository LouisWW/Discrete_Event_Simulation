# settings.py

import numpy as np

# initialise global variables they can be accessed from everywhere
def init_global(end_n_actions):
    global list_arrivaltime
    list_arrivaltime = np.zeros(end_n_actions+1)
    global list_helptime
    list_helptime = np.zeros(end_n_actions+1)
    global queue_length
    queue_length = 0
    global queue_length_list
    queue_length_list = np.zeros(end_n_actions+1)
    global queue_time_list
    queue_time_list = np.zeros(end_n_actions+1)
    global time_spend_in_queue_list
    time_spend_in_queue_list = np.zeros(end_n_actions+1)