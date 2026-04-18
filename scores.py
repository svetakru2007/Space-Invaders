import pygame.font
from heart import Heart
from pygame.sprite import Group

class Scores():
    """класс для вывода игровой информации"""

    def __init__(self, screen, stats):
        """инициализация подсчета очков"""
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.stats = stats
        self.text_color = (128, 255, 0)
        self.font = pygame.font.SysFont(None, 36)
        self.image_score()
        self.image_high_score()
        self.image_harts()

    def image_score(self):
        """преобразование текста счета в графическое изображение"""
        self.score_img = self.font.render(str(self.stats.score), True, self.text_color, (0, 0, 0))
        self.score_rect = self.score_img.get_rect()

        # Размещение счета в правом верхнем углу
        self.score_rect.right = self.screen_rect.right - 40
        self.score_rect.top = 20

    def image_high_score(self):
        """преобразование рекорда в графическое изображение"""
        self.high_score_image = self.font.render(str(self.stats.high_score), True, self.text_color, (0, 0, 0))
        self.high_score_rect = self.high_score_image.get_rect()

        # Размещение рекорда по центру вверху
        self.high_score_rect.centerx = self.screen_rect.centerx
        self.high_score_rect.top = self.score_rect.top

    def image_harts(self):
        """количество жизней"""
        self.harts = Group()
        self.harts.empty()

        # Создание сердечек в зависимости от количества жизней
        for hart_number in range(self.stats.guns_left):
            heart = Heart(self.screen)
            # Размещение сердечек в левом верхнем углу
            heart.rect.x = 40 + hart_number * heart.rect.width
            heart.rect.y = 15
            self.harts.add(heart)

    def show_score(self):
        """вывод счета на экран"""
        self.screen.blit(self.score_img, self.score_rect)
        self.screen.blit(self.high_score_image, self.high_score_rect)
        self.harts.draw(self.screen)

