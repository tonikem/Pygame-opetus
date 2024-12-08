import os, sys
import pygame
from PIL import Image, ImageChops

BASE_IMG_PATH = "assets/sprites/"


def pillow_image_to_surface(pillow_image):
    return pygame.image.frombytes(pillow_image.tobytes(), pillow_image.size, pillow_image.mode)

def load_image(path):
    img = pygame.image.load(BASE_IMG_PATH + path).convert()
    img.set_colorkey((0, 0, 0))
    return img

def load_tile_images(tile_size=16):
    images = []
    img = Image.open(BASE_IMG_PATH + "World-Tiles.png")
    empty_img = Image.open(BASE_IMG_PATH + "tyhjä.png")
    for y in range(0, 1392, 16):
        for x in range(0, 288, 16):
            cropped_img = img.crop((x, y, x + 16, y + 16))
            resized_img = cropped_img.resize((tile_size, tile_size))
            diff = ImageChops.difference(resized_img, empty_img)
            surf = pillow_image_to_surface(resized_img)
            if diff.getbbox():
                images.append(surf)
    return images

def load_hero_idle_images():
    images = []
    img = Image.open(BASE_IMG_PATH + "Hero.png")
    idle_images = [
        img.crop((0, 17, 14, 48)),
        img.crop((16, 17, 30, 48)),
        img.crop((32, 17, 46, 48)),
        img.crop((48, 17, 62, 48)),
        img.crop((64, 17, 78, 48)),
        img.crop((80, 17, 94, 48)),
        img.crop((96, 17, 110, 48)),
        img.crop((112, 17, 126, 48))
    ]
    for img in idle_images:
        surf = pillow_image_to_surface(img)
        images.append(surf)
    return images

def load_hero_run_images():
    images = []
    img = Image.open(BASE_IMG_PATH + "Hero.png")
    run_images = [
        img.crop((0, 81, 16, 112)),
        img.crop((16, 81, 31, 112)),
        img.crop((33, 81, 46, 112)),
        img.crop((49, 81, 63, 112))
    ]
    for img in run_images:
        surf = pillow_image_to_surface(img)
        images.append(surf)
    return images

def load_hero_jump_images():
    images = []
    img = Image.open(BASE_IMG_PATH + "Hero.png")
    run_images = [
        img.crop((0, 52, 16, 80)),
        img.crop((16, 52, 30, 80)),
        img.crop((32, 52, 48, 80)),
        img.crop((48, 52, 64, 80))
    ]
    for img in run_images:
        surf = pillow_image_to_surface(img)
        images.append(surf)
    return images


class Animation:
    def __init__(self, images, img_dur=5, loop=True):
        self.images = images
        self.img_dur = img_dur
        self.loop = loop
        self.done = False
        self.frame = 0

    def copy(self):
        return Animation(self.images, self.img_dur, self.loop)

    def update(self):
        if self.loop:
            self.frame = (self.frame + 1) % (self.img_dur * len(self.images))
        else:
            self.frame = min(self.frame + 1, self.img_dur * len(self.images) - 1)
            if self.frame >= self.img_dur * len(self.images) - 1:
                self.done = True

    def img(self):
        return self.images[int(self.frame / self.img_dur)]


