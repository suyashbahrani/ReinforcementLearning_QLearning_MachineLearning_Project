# The Q-agent class can be extended to child classes

import pickle
import random
from collections import defaultdict

import numpy as np


class qLearningAgent:

    def __init__(self, env, alpha, nA, gamma=1.0, eps_start=1.0, eps_decay=0.9999, eps_min=0.05):
        self.env = env
        self.eps_start = eps_start
        self.gamma = gamma
        self.alpha = alpha
        self.eps_decay = eps_decay
        self.eps_min = eps_min
        self.nA = nA
        self.Q = defaultdict(lambda: np.zeros(self.nA))

    def greedyApproach(self, state, epsilon): #------------> This function is created to choose the best possible action (probability of 1-epsilon) or else provide random action
        prob = random.random()
        if prob > epsilon:
            return np.argmax(self.Q[state])
        else:
            return np.random.choice(np.arange(self.nA))

    def learn(self, state, action, reward, next_state): #---------> Agents should be learning and this funcion utilizes the Q-function to help them learn
        self.Q[state][action] += self.alpha * (reward + self.gamma * np.max(self.Q[next_state]) - self.Q[state][action])


    def savePolicy(self): #-----------> This function would set a policy once the agents have learned
        policy = defaultdict(lambda: 0)
        for state, action in self.Q.items():
            policy[state] = np.argmax(action)
        self.policy = policy


    def takeAction(self, state): #-----------> Mimic the policy that was earlier set
        return self.policy[state]

    def changePolicy(self, directory): #------------> Loading previous policies
        with open(directory, 'rb') as f:
            policy_new = pickle.load(f)
        self.policy = defaultdict(lambda: 0, policy_new)
        print('policy Loaded')

    def save(self, i): #----------> Save policy as a pickle file
        try:
            policy = dict(self.policy)
            with open(f'policy{i}.pickle', 'wb') as f:
                pickle.dump(policy, f)
        except:
            print('not saved')
