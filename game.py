import sys
import pygame


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Platform Game")
        self.screen = pygame.display.set_mode((640, 480))
        self.clock = pygame.time.Clock()

        # Main character
        self.hero_img = pygame.image.load("assets/sprites/Hero.png").convert()
        self.hero_pos = [0, 0]
        self.movement = [False, False]
        self.speed = 1

    def run(self):
        while True:
            self.screen.fill((14, 219, 248))

            if self.movement[0]:
                self.hero_pos[1] += -self.speed
            if self.movement[1]:
                self.hero_pos[1] += self.speed

            cropped_region = (0, 20, 14, 28)
            self.screen.blit(self.hero_img, self.hero_pos, cropped_region)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.movement[0] = True
                    if event.key == pygame.K_DOWN:
                        self.movement[1] = True

                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_UP:
                        self.movement[0] = False
                    if event.key == pygame.K_DOWN:
                        self.movement[1] = False

            pygame.display.update()
            self.clock.tick(60)



Game().run()


