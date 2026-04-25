import pygame, controls
from gun import Gun
from pygame.sprite import Group
from stats import Stats
from scores import Scores

def run():
    """главная функция запуска игры"""
    pygame.init()
    # Создание окна игры
    screen = pygame.display.set_mode((700, 700))
    pygame.display.set_caption('Космо бой')
    icon = pygame.image.load('images/icon.png')
    pygame.display.set_icon(icon)
    bg_color = (0, 0, 0)
    bg = pygame.image.load('images/bgg.jpg')

    # Инициализация статистики и счета
    stats = Stats()
    sc = Scores(screen, stats)

    # Создание игровых объектов
    gun = Gun(screen) # пушка
    bullets = Group() # группа для хранения пуль
    aliens = Group() # группа для хранения пришельцев
    controls.create_army(screen, aliens, alien_speed=0.03, stats=stats)  # армия пришельцев

    # Главный игровой цикл
    while True:
        controls.events(screen, gun, bullets) # обработка событий

        # Проверка: активна ли игра
        if stats.run_game:
            gun.update_gun()
            bullets.update()
            controls.update(bg_color, screen, stats, sc, gun, aliens, bullets)
            controls.update_bullets(screen, stats, sc, aliens, bullets)
            controls.update_aliens(stats, screen, bg, sc, gun, aliens, bullets)
        else:
            controls.game_over_screen(stats, sc, gun, aliens, bullets, screen)

run()