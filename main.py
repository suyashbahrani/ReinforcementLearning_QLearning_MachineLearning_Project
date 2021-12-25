import sys
import time
import pygame
from Agent import qLearningAgent
from Environment import Playground, BuildPlayground

# initializing colors
GREEN = (0, 150, 0)
WHITE = (254, 254, 254)
ORANGE = (254, 165, 0)
RED = (254, 0, 0)
BLACK = (0, 0, 0)

displayH, displayW = 700, 600

pygame.init()
pygame.display.set_caption('Heist Playground')
gameDisplay = pygame.display.set_mode((displayW, displayH))


game_matrix = BuildPlayground(rows=10, columns=10)
env = Playground(gameDisplay, game_matrix)

# agents are initialized
police = qLearningAgent(env, alpha=0.1, nA=4)
thief = qLearningAgent(env, alpha=0.1, nA=4)

# Intializing Clock
clock = pygame.time.Clock()

# displaying function
def show_info(money, burglar):
    pygame.draw.rect(gameDisplay, BLACK, [0, 600, 600, 5])
    font = pygame.font.SysFont(None, 40)
    text1 = font.render("Thief gets the money: " + str(money), True, GREEN)
    text2 = font.render("Thief gets caught: " + str(burglar), True, RED)

    gameDisplay.blit(text1, (50, 610))
    gameDisplay.blit(text2, (50, 655))


# indicative rectangle to show money grabbed or thief caught
def draw_rect(color, x, y, width, height):
    pygame.draw.rect(gameDisplay, color, [x * width, y * height, width, height], 10)
    pygame.display.update()
    time.sleep(2)


total_thief_caught = 0
total_money_grabbed = 0

epsilon, eps_decay, eps_min = 1.0, 0.99, 0.05

# number of escapes in one run
numEscapes = 2000

# loop over escapes
for escape in range(1, numEscapes + 1):

    if escape % 100 == 0:
        print("\rRounds {}/{}".format(escape, numEscapes), end="")
        # sys.stdout.flush()

    if escape % 500 == 0:
        print("\nMoney Grabbed: " + str(total_money_grabbed) + "\n" + "Thief Caught: " + str(total_thief_caught))
        # sys.stdout.flush()

    epsilon = max(epsilon * eps_decay, eps_min)

    state = env.reset()
    action_thief = thief.greedyApproach(state['thief'], epsilon)
    action_police = police.greedyApproach(state['police'], epsilon)

    # render the playground
    env.render(escape)

    while True:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        next_state, reward, done, info = env.step(action_thief, action_police)

        # learning calls for agent
        thief.learn(state['thief'], action_thief, reward['thief'], next_state['thief'])
        police.learn(state['police'], action_police, reward['police'], next_state['police'])

        # render the playground
        gameDisplay.fill(WHITE)
        env.render(escape)
        show_info(total_money_grabbed, total_thief_caught)

        # display updated
        pygame.display.update()
        clock.tick(1000)

        if done:
            if info['money_grabbed']:
                total_money_grabbed += 1
                draw_rect(GREEN, info['x'], info['y'], info['width'], info['height'])

            if info['thief_caught']:
                total_thief_caught += 1
                draw_rect(RED, info['x'], info['y'], info['width'], info['height'])
            break

        state = next_state
        action_thief = thief.greedyApproach(state['thief'], epsilon)
        action_police = police.greedyApproach(state['police'], epsilon)

police.savePolicy()
thief.savePolicy()
police.save('_police')
thief.save('_thief')
# Saving policy as pickle file
