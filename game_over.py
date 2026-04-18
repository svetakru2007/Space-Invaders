import pygame
import sys


class GameOver:
    """класс для экран окончания игры"""

    def __init__(self, screen):
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.bg_color = pygame.image.load('images/bgg.jpg')
        self.button_color = (0, 150, 0)
        self.button_color_exit = (150, 0, 0)
        self.text_color = (255, 255, 255)
        self.font_title = pygame.font.SysFont(None, 72)
        self.font_button = pygame.font.SysFont(None, 48)

        # Текст "Игра окончена"
        self.game_over_text = self.font_title.render("ИГРА ОКОНЧЕНА", True, self.text_color)
        self.game_over_rect = self.game_over_text.get_rect(center=(self.screen_rect.centerx, 250))

        # Кнопка "Играть ещё"
        self.play_button = pygame.Rect(0, 0, 230, 60)
        self.play_button.center = (self.screen_rect.centerx - 97, 350)
        self.play_text = self.font_button.render("Играть ещё", True, self.text_color)
        self.play_text_rect = self.play_text.get_rect(center=self.play_button.center)

        # Кнопка "Выход"
        self.exit_button = pygame.Rect(0, 0, 150, 60)
        self.exit_button.center = (self.screen_rect.centerx + 140, 350)
        self.exit_text = self.font_button.render("Выход", True, self.text_color)
        self.exit_text_rect = self.exit_text.get_rect(center=self.exit_button.center)

    def draw(self):
        """отрисовка экрана окончания игры"""
        self.screen.blit(self.bg_color, (0, 0))

        # Отрисовка кнопок
        pygame.draw.rect(self.screen, self.button_color, self.play_button)
        pygame.draw.rect(self.screen, self.button_color_exit, self.exit_button)

        # Отрисовка текстов
        self.screen.blit(self.game_over_text, self.game_over_rect)
        self.screen.blit(self.play_text, self.play_text_rect)
        self.screen.blit(self.exit_text, self.exit_text_rect)

        pygame.display.flip()

    def handle_events(self, stats, sc, gun, aliens, bullets, screen):
        """обработка событий на экране окончания игры"""
        for event in pygame.event.get():
            # Закрытие окна
            if event.type == pygame.QUIT:
                sys.exit()

            # Обработка нажатия кнопки мыши
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                # Проверка нажатия на кнопку "Играть ещё"
                if self.play_button.collidepoint(mouse_pos):
                    self.restart_game(stats, sc, gun, aliens, bullets, screen)
                    return True
                # Проверка нажатия на кнопку "Выход"
                elif self.exit_button.collidepoint(mouse_pos):
                    sys.exit()
        return False

    def restart_game(self, stats, sc, gun, aliens, bullets, screen):
        """перезапуск игры"""

        # Сброс статистики
        stats.reset_stats()
        stats.run_game = True

        # Обновление счёта
        sc.image_score()
        sc.image_harts()
        sc.image_high_score()

        # Очистка списков
        aliens.empty()
        bullets.empty()

        # Создание новой армии
        from controls import create_army
        create_army(screen, aliens)

        # Сброс позиции пушки
        gun.create_gun()