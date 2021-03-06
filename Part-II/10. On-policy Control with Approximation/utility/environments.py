import math

from .misc import *

class Environment(object):
    def get_actions(self, state):
        '''
        Returns the available actions for the state
        '''
        raise NotImplementedError()

    def step(self, action):
        '''
        Returns the observation of the next state, the reward, a terminal flag and a dictionary with debug information
        '''
        raise NotImplementedError()

    def render(self):
        pass

    def reset(self):
        '''
        Returns the initial observation of the starting state
        '''
        raise NotImplementedError()

class MountainCar(Environment):
    def __init__(self, min_x=-1.2, max_x=0.5, min_v=-0.07, max_v=0.07, speed=0.001, gravity=0.0025, freq=3, start_x_min=-0.6, 
                 start_x_max=-0.4, start_v_min=0.0, start_v_max=0.0):
        self.min_x = min_x
        self.max_x = max_x
        self.min_v = min_v
        self.max_v = max_v
        self.speed = speed
        self.gravity = gravity
        self.freq = freq
        self.start_x_min = start_x_min
        self.start_x_max = start_x_max
        self.start_v_min = start_v_min
        self.start_v_max = start_v_max
        self.reset()

    def get_actions(self, state):
        return [-1, 0, 1]
    
    def step(self, action):
        unclipped_pos = self.pos + self.v
        self.pos = clip(unclipped_pos, self.min_x, self.max_x)
        self.v = clip(self.v + self.speed * action - self.gravity * math.cos(self.freq * self.pos), self.min_v, self.max_v)
        
        terminal = unclipped_pos > self.max_x
        if unclipped_pos < self.min_x:
            self.v = 0.0
        
        return ((self.pos, self.v), -1, terminal, {})

    def reset(self):
        r = np.random.rand(2)
        self.pos = r[0] * (self.start_x_max - self.start_x_min) + self.start_x_min
        self.v = r[1] * (self.start_v_max - self.start_v_min) + self.start_v_min
        return (self.pos, self.v)

class ServerAssignment(Environment):
    '''
    This is a continous task, so terminal will always be False.
    '''
    def __init__(self, max_servers=10, priorities=[1, 2, 4, 8], free_server_p=0.06):
        self.max_servers = max_servers
        self.priorities = priorities
        self.free_server_p = free_server_p
        self.reset()

    def get_actions(self, state):
        return [0, 1] # 0 = reject, 1 = approve
    
    def step(self, action):
        new_servers = np.sum(np.random.rand(self.max_servers - self.num_free_servers) < self.free_server_p)
        reward = 0
        if self.num_free_servers != 0 and action == 1:
            reward = self.front_priority
            self.num_free_servers -= 1
        self.num_free_servers += new_servers
        self.front_priority = np.random.choice(self.priorities)
        return ((self.num_free_servers, self.front_priority), reward, False, {})

    def reset(self):
        self.num_free_servers = np.random.randint(0, 11)
        self.front_priority = np.random.choice(self.priorities)
        return (self.num_free_servers, self.front_priority)
