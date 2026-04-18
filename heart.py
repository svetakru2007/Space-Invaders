import pygame
from pygame.sprite import Sprite

class Heart(Sprite):

    def __init__(self, screen):
        """инициализация жизни"""

        super(Heart, self).__init__()
        self.screen = screen
        # Загрузка изображения сердечка
        self.image = pygame.image.load('images/heart.png')
        self.rect = self.image.get_rect()