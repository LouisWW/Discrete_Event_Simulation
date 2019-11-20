# Test #

class Serversystem(object):
    "A server has n desks at which tasks can be carried out, if all desks are in use, a task has to wait"

    def __init__(self, env, n_server, helptime, capacity):
        self.env = env
        self.server = simpy.Resource(env, n_server)
        self.helptime = helptime # the average help time is 1/capacity, so need to incorporate that
        self.capacity = capacity

    def help(self, task):
        yield self.env.timeout(HELPTIME) # randomness needs to be added here
        print("Carrying out the task took {}".format(self.env.now))



def task(env, name, ss):
    "A task process that will be carried out by a serversystem (ss) after having waited for a server to become available"
    with ss.server.request() as request:

        # wait for server to become available
        yield request
        print("{} started by server at {}".format(name, env.now))

        # wait for task to be finished
        yield env.process(ss.help(name))
        print("{} carried out by server at {}".format(name, env.now))

def setup(env, n_server, helptime, arrivaltime):
    '''Here we create a server system with a certain number of servers. We start creating cars at random'''
    serversystem = Serversystem(env, n_server, helptime, capacity)

    i = 0
    # create task until the simulation time is over
    while True:

        # wait until new task arrives
        yield env.timeout(arrivaltime) # arrival time needs to be made random
        i += 1
        env.process(task(env, 'Task{}'.format(i), serversystem))


# create a simpy environment
env = simpy.Environment()

# set up the system
env.process(setup(env, n_server, helptime, arrivaltime))

# run the program
env.run(until=endtime)








