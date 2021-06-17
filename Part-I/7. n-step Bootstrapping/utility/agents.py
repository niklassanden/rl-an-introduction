import numpy as np

from .misc import *

class PredeterminedActions(object):
    def __init__(self, env, max_actions=1000000):
        self.max_actions = max_actions
        self.actions = np.random.choice(env.get_actions(0), size=max_actions, replace=True)
        self.reset()

    def __call__(self, s):
        action = self.actions[self.iterator]
        self.iterator = (self.iterator + 1) % self.max_actions
        return action

    def reset(self):
        self.iterator = 0

class EpsilonGreedyAgent(object):
    '''
    This agent will keep track of the number of calls made to it which is used to see how many time steps it took to complete
    each episode.
    '''
    def __init__(self, env, epsilon=0.1):
        self.env = env
        self.epsilon = epsilon
        self.counter = 0
    
    def __call__(self, state, Q):
        self.counter += 1
        actions = self.env.get_actions(state)
        if np.random.rand() < self.epsilon:
            return actions[np.random.choice(np.arange(len(actions)))]
        else:
            best_index = argmax(np.array([Q[(state, a)] for a in actions]))
            return actions[best_index]
    
    def get_probs(self, state, Q):
        '''
        technically each tie of argmax should share the 1.0 - epsilon but this is fine since the 
        use case is to multiply the probability with the Q value which are the same in case of a tie.
        '''
        actions = self.env.get_actions(state)
        probs = [self.epsilon / len(actions)] * len(actions)
        best_index = np.argmax(np.array([Q[(state, a)] for a in actions]))
        probs[best_index] += 1.0 - self.epsilon
        return (actions, probs)
