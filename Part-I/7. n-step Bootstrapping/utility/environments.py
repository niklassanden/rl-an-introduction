import numpy as np

class Environment(object):
    def __init__(self):
        pass

    def get_actions(self, state):
        '''
        Returns the available actions for the state
        '''
        NotImplementedError()

    def step(self, action):
        '''
        Returns the observation of the next state, the reward, a terminal flag and a dictionary with debug information
        '''
        NotImplementedError()

    def render(self):
        pass

    def reset(self):
        '''
        Returns the initial observation of the starting state
        '''
        NotImplementedError()

class RandomWalk(Environment):
    def __init__(self, num_states=19):
        '''
        num_states is excluding the two terminal states on the left and right
        This is slightly different than the Random Walk in chapter 6 since it gives a reward of -1 at the far left.
        '''
        assert num_states >= 1 and (num_states % 2) == 1, str(num_states) + ' is not a valid num_states'
        self.num_states = num_states
        self.reset()

    def get_actions(self, state):
        return [-1, 1]
    
    def step(self, action):
        self.state += action
        terminal = False
        reward = 0.0
        if self.state < 0:
            terminal = True
            reward = -1.0
        elif self.state >= self.num_states:
            terminal = True
            reward = 1.0
        return (self.state, reward, terminal, {})

    def reset(self):
        self.state = self.num_states // 2
        return self.state

class WindyGridworld(Environment):
    '''
    Although you can choose the wind_values exactly, is_stochastic will always use the stochasticity described in the book:
    1/3 above, 1/3 below, 1/3 expected.
    This is copied from chapter 6.
    '''
    def __init__(self, rows, cols, wind_values, is_stochastic=False, king_moves=False, can_pass=False):
        '''
        wind_values should be a list with a value (int) for each column. Positive signifies up, negative down.
        '''
        self.rows = rows
        self.cols = cols
        self.wind_values = wind_values
        self.is_stochastic = is_stochastic
        self.king_moves = king_moves
        self.can_pass = can_pass
        self.start = (rows // 2, 0)
        self.end = (rows // 2, cols - 3)
        self.reset()

        # We precalculate all of the legal moves from the combination of rules once to use whenever get_actions is called
        self._calculate_moves()

    def get_actions(self, state):
        return self.moves
    
    def step(self, action):
        wind_value = self.wind_values[self.pos[1]]
        if self.is_stochastic and wind_value != 0:
            wind_value += np.random.choice(np.arange(-1, 2))
        self.pos = (self.pos[0] + action[0] - wind_value, self.pos[1] + action[1])
        self._keep_pos_in_bounds()
        
        terminal = self.end == self.pos
        return (self.pos, -1, terminal, {})

    def reset(self):
        self.pos = self.start
        return self.pos

    def _calculate_moves(self):
        self.moves = [(1, 0), (0, 1), (-1, 0), (0, -1)] # adjacent moves
        if self.king_moves:
            self.moves = self.moves + [(1, 1), (1, -1), (-1, 1), (-1, -1)]
        if self.can_pass:
            self.moves.append((0, 0))
    
    def _keep_pos_in_bounds(self):
        self.pos = (min(self.rows - 1, max(0, self.pos[0])), min(self.cols - 1, max(0, self.pos[1])))

class WindyGridworldPositiveRewardWrapper(WindyGridworld):
    def step(self, action):
        next_state, reward, terminal, info = super(WindyGridworldPositiveRewardWrapper, self).step(action)
        reward = 1.0 if terminal else 0.0
        return (next_state, reward, terminal, info)
