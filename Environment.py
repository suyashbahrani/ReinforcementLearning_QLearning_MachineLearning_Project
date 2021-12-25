# Environment
import numpy as np
import pygame
from police import Police
from thief import Thief

# Initializing colours
WHITE = (254, 254, 254)
BLUE = (0, 0, 254)
BLACK = (0, 0, 0)
RED = (254, 0, 0)
GREEN = (0, 255, 0)
TEXT_COLOR = (0, 0, 220)


class Playground:

    def __init__(self, gameDisplay, game_matrix):  # Setting up the environment to play in

        self.HEIGHT = game_matrix.ROWS
        self.WIDTH = game_matrix.COLUMNS

        self.DISPLAY = gameDisplay  # rendered

        display_width, display_height = gameDisplay.get_size()
        display_height -= 100  # Adding extra space for Data Display

        self.BLOCK_WIDTH = int(display_width / self.WIDTH)
        self.BLOCK_HEIGHT = int(display_height / self.HEIGHT)

        # Initializing the agents
        self.POLICE = Police(self.DISPLAY, self.BLOCK_WIDTH, self.BLOCK_HEIGHT)
        self.THIEF = Thief(self.DISPLAY, self.BLOCK_WIDTH, self.BLOCK_HEIGHT)
        self.MOVES = {'thief': 150, 'police': 150}

        self.OBSTACLES = game_matrix.OBSTACLES

        self.MONEY_IMG = pygame.transform.scale(pygame.image.load('pics/money.png'), (self.BLOCK_WIDTH, self.BLOCK_HEIGHT))

    # Function to get the state of playground
    def getState(self):
        self.STATE = {
            'thief': (self.THIEF_X - self.POLICE_X, self.THIEF_Y - self.POLICE_Y, self.THIEF_X - self.MONEY_X, self.THIEF_Y - self.MONEY_Y),
            'police': (self.POLICE_X - self.THIEF_X,self.POLICE_Y - self.THIEF_Y)}  # Money Bag state can also be shared with police to act as a guardian
        return self.STATE

    # Resetting the playground - After moves finished - After successful catch of Thief/Money
    def reset(self):
        self.MONEY_X, self.MONEY_Y = np.random.randint(0, 9, 2, 'int')
        self.POLICE_X, self.POLICE_Y = (8, 9)
        self.THIEF_X, self.THIEF_Y = (0, 0)
        # Confirming none of the agent and money bag is inside obstacle
        for obs in self.OBSTACLES:
            if self.MONEY_X == obs[0] and self.MONEY_Y == obs[1]:
                self.MONEY_Y -= 1
            if self.THIEF_X == obs[0] and self.THIEF_Y == obs[1]:
                self.THIEF_Y -= 1
            if self.POLICE_X == obs[0] and self.POLICE_Y == obs[1]:
                self.POLICE_Y -= 1
        self.MOVES['police'] = 150
        self.MOVES['police'] = 150
        return self.getState()

    # Create Playground

    def render(self, escape=-1):

        # drawing our agents
        self.THIEF.draw(self.THIEF_X, self.THIEF_Y)
        self.POLICE.draw(self.POLICE_X, self.POLICE_Y)

        self.DISPLAY.blit(self.MONEY_IMG, (self.MONEY_X * self.BLOCK_WIDTH, self.MONEY_Y * self.BLOCK_HEIGHT))

        # drawing obstacles
        for pos in self.OBSTACLES:
            pygame.draw.rect(self.DISPLAY, BLACK,
                             [pos[0] * self.BLOCK_WIDTH, pos[1] * self.BLOCK_HEIGHT, self.BLOCK_WIDTH,
                              self.BLOCK_HEIGHT])

        if escape >= 0:
            self.displayEscape(escape)

    # changing the playground with every movement
    def step(self, thief_action, police_action):

        reward = {'thief': -1, 'police': -1}
        done = False
        info = {
            'money_grabbed': False,
            'thief_caught': False,
            'x': -1, 'y': -1,
            'width': self.BLOCK_WIDTH,
            'height': self.BLOCK_HEIGHT
        }

        # decreasing the no. of moves
        self.MOVES['police'] -= 1
        self.MOVES['thief'] -= 1
        # done if moves = 0
        if self.MOVES['police'] == 0 or self.MOVES['thief'] == 0:
            done = True

        self.updateSteps(thief_action, police_action)

        # thief stole money
        if self.THIEF_X == self.MONEY_X and self.THIEF_Y == self.MONEY_Y:
            done = True
            reward['thief'] = 50
            info['money_grabbed'], info['x'], info['y'] = True, self.THIEF_X, self.THIEF_Y

        # police caught the thief
        if self.POLICE_X == self.THIEF_X and self.POLICE_Y == self.THIEF_Y:
            done = True
            reward['police'] = 50
            reward['thief'] = -20
            info['thief_caught'], info['x'], info['y'] = True, self.THIEF_X, self.THIEF_Y

        for obs in self.OBSTACLES:
            if self.THIEF_X == obs[0] and self.THIEF_Y == obs[1]:
                reward['thief'] = -20
                self.THIEF_X, self.THIEF_Y = (0, 0)

            if self.POLICE_X == obs[0] and self.POLICE_Y == obs[1]:
                reward['police'] = -20
                self.POLICE_X, self.POLICE_Y = (8, 9)

        return self.getState(), reward, done, info

    # Display the number of escapes attempted

    def displayEscape(self, escapes):
        font = pygame.font.SysFont(None, 25)
        text = font.render("Escape: " + str(escapes), True, TEXT_COLOR)
        self.DISPLAY.blit(text, (1, 1))

    # choosing a worthy step - 8 direction movement allowed

    def getChanges(self, action):
        x_change, y_change = 0, 0

        if action == 0:
            x_change = 1  # right
        elif action == 1:
            x_change = -1  # left
        elif action == 2:
            y_change = -1  # up
        elif action == 3:
            y_change = 1  # down
        elif action == 4:
            x_change == -1  # diagonal bottom left
            y_change == -1
        elif action == 5:
            x_change == -1  # diagonal top left
            y_change == 1
        elif action == 5:
            x_change == 1   # diagonal top right
            y_change == 1
        elif action == 5:
            x_change == 1   # diagonal bottom right
            y_change == -1

        return x_change, y_change

    # updating the positions of the agents with the step chosen

    def updateSteps(self, thief_action, police_action):
        x_change_thief, y_change_thief = self.getChanges(thief_action)
        x_change_police, y_change_police = self.getChanges(police_action)

        self.THIEF_X += x_change_thief
        self.THIEF_Y += y_change_thief

        self.POLICE_X += x_change_police
        self.POLICE_Y += y_change_police

        self.THIEF_X, self.THIEF_Y = self.fix(self.THIEF_X, self.THIEF_Y)
        self.POLICE_X, self.POLICE_Y = self.fix(self.POLICE_X, self.POLICE_Y)

    # Checking for the instances where the agent going out of bounds
    def fix(self, x, y):
        if x > self.WIDTH - 1:
            x = self.WIDTH - 1
        elif x < 0:
            x = 0

        if y > self.HEIGHT - 1 :
            y = self.HEIGHT - 1
        elif y < 0:
            y = 0

        return x, y


class BuildPlayground:

    def __init__(self, rows=10, columns=10):
        self.ROWS = rows
        self.COLUMNS = columns
        self.OBSTACLES = [[1, 1], [1, 3], [1, 5], [1, 7], [1, 9], [3, 2], [3, 4], [3, 6], [3, 8], [5, 1], [5, 3], [5, 5], [5, 7], [5, 9], [7, 2], [7, 4], [7, 6], [7, 8], [9, 1], [9, 3], [9, 5], [9, 7], [9, 9]]