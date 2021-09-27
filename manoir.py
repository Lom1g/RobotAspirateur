import pygame

from agent import Agent
from environnement import Environnement


class Manoir:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((600, 600))
        self.background = pygame.image.load("assets\\grille.jpg")
        self.environnement = Environnement()
        self.agent = Agent(self.environnement)

    # execution de l'environnement et de l'agent
    def run(self):
        self.environnement.start()
        self.agent.start()


def main():
    running = True
    manoir = Manoir()
    manoir.run()
    while running:
        manoir.screen.blit(manoir.background, (0, 0))
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                running = False


if __name__ == "__main__":
    main()
