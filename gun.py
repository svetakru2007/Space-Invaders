import pygame

class Gun():

    def __init__(self, screen):
        """инициализация пушки"""
        self.screen = screen
        # Загрузка изображения пушки
        self.image = pygame.image.load('images/gun.png')
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()

        # Размещение внизу по центру
        self.rect.centerx = self.screen_rect.centerx
        self.center = float(self.rect.centerx)
        self.rect.bottom = self.screen_rect.bottom

        # Флаги движения
        self.mright = False # вправо
        self.mleft = False # влево

    def output(self):
        """рисование пушки"""
        self.screen.blit(self.image, self.rect)

    def update_gun(self):
        """обновление позиции пушки"""
        # Движение вправо с проверкой границ
        if self.mright and self.rect.right < self.screen_rect.right:
            self.center += 2.25
        # Движение влево с проверкой границ
        elif self.mleft and self.rect.left > self.screen_rect.left:
            self.center -= 2.25
        self.rect.centerx = self.center

    def create_gun(self):
        """размещает пушку внизу по центру"""
        self.center = self.screen_rect.centerx

    def reset_flags(self):
        """сброс флагов движения (при перезапуске)"""
        self.mright = False
        self.mleft = False