import sys
import pygame


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Platform Game")
        self.screen = pygame.display.set_mode((640, 480))
        self.clock = pygame.time.Clock()

        self.hero_img = pygame.image.load("assets/sprites/Hero.png").convert()

    def run(self):
        while True:
            cropped_region = (0, 20, 14, 28)
            self.screen.blit(self.hero_img, (0, 0), cropped_region)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            pygame.display.update()
            self.clock.tick(60)



Game().run()


