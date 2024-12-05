import sys
import pygame


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Platform Game")
        self.screen = pygame.display.set_mode((640, 480))
        self.clock = pygame.time.Clock()

        # Main character
        self.img = pygame.image.load("assets/sprites/Hero.png").convert()
        self.img.set_colorkey((0, 0, 0))
        self.img_pos = [100, 100]
        self.movement = [False, False]
        self.speed = 2
        self.cropped_region = (0, 20, 14, 28)

        self.collision_area = pygame.Rect(50, 50, 100, 50)

    def run(self):
        while True:
            self.screen.fill((10, 100, 100))

            if self.movement[0]:
                self.img_pos[1] += -self.speed
            if self.movement[1]:
                self.img_pos[1] += self.speed

            cropped_width = self.cropped_region[2]
            cropped_height = self.cropped_region[3]

            img_r = pygame.Rect(self.img_pos[0], self.img_pos[1], cropped_width, cropped_height)

            if img_r.colliderect(self.collision_area):
                pygame.draw.rect(self.screen, (0, 100, 255), self.collision_area)
            else:
                pygame.draw.rect(self.screen, (0, 50, 155), self.collision_area)

            self.screen.blit(self.img, self.img_pos, self.cropped_region)

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


