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
    root_path = r"assets/sprites/"
    img = Image.open(root_path + "World-Tiles.png")
    empty_img = Image.open(root_path + "tyhjä.png")

    for y in range(0, 1392, 16):
        for x in range(0, 288, 16):
            cropped_img = img.crop((x, y, x + 16, y + 16))
            resized_img =cropped_img.resize((tile_size, tile_size))
            diff = ImageChops.difference(resized_img, empty_img)
            surf = pillow_image_to_surface(resized_img)
            if diff.getbbox():
                images.append(surf)

    return images

