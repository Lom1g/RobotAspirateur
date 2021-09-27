import pygame

from agent import Agent
from environnement import Environnement


class Manoir:

    def __init__(self):
        pygame.init()
        self.dustImage = pygame.image.load("assets\\dust.png")
        self.diamondImage = pygame.image.load("assets\\jewel.png")
        self.backgroundImage = pygame.image.load("assets\\grille.jpg")
        self.screen = pygame.display.set_mode((600, 600))
        self.environnement = Environnement()
        self.agent = Agent(self.environnement)

    # execution de l'environnement et de l'agent
    def run(self):
        self.environnement.start()
        self.agent.start()

    # affiche les différents assets du manoir
    def show(self):
        self.screen.blit(self.backgroundImage, (0, 0))
        for i in range(len(self.environnement.grid)):
            if self.environnement.grid[i]["dust"]:
                j = i % 5  # modulo
                k = i // 5  # floor division
                self.screen.blit(self.dustImage, (20 + (j * 120), 20 + (k * 120)))
            if self.environnement.grid[i]["diamond"]:
                j = i % 5  # modulo
                k = i // 5  # floor division
                self.screen.blit(self.diamondImage, (70 + (j * 120), 20 + (k * 120)))
        pygame.display.flip()


def main():
    running = True
    manoir = Manoir()
    manoir.run()
    while running:
        manoir.show()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                running = False


if __name__ == "__main__":
    main()
