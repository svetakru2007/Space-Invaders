import pygame, sys
from bullet import Bullet
from alien import Alien
from game_over import GameOver
import time
import random

army_shapes = {
    'rectangle': 'прямоугольник',
    'triangle': 'треугольник',
    'circle': 'круг',
    'two_squares': 'два квадрата',
    'heart': 'сердце'
}

def events(screen, gun, bullets):
    """обработка событий"""
    for event in pygame.event.get():
        # Закрытие окна игры
        if event.type == pygame.QUIT:
            sys.exit()

        # Обработка нажатия клавиш
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT or event.key == pygame.K_d: # вправо
                gun.mright = True
            elif event.key == pygame.K_LEFT or event.key == pygame.K_a: # влево
                gun.mleft = True
            elif event.key == pygame.K_SPACE: # пробел
                new_bullet = Bullet(screen, gun)
                bullets.add(new_bullet)

        # Оработка отпускания клавиш
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT or event.key == pygame.K_d: # Вправо
                gun.mright = False
            elif event.key == pygame.K_LEFT or event.key == pygame.K_a: # Влево
                gun.mleft = False

def update(bg_color, screen, stats, sc, gun, aliens, bullets):
    """обновление экрана"""
    screen.fill(bg_color)
    sc.show_score()

    for bullet in bullets.sprites():
        bullet.draw_bullet()

    gun.output()
    aliens.draw(screen)
    pygame.display.flip()

def update_bullets(screen, stats, sc,  aliens, bullets):
    """обновление позиции пуль"""
    bullets.update()

    # Удаление пуль, вышедших за границы экрана
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)

    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)

    # Начисление очков за поподания в пришельца
    if collisions:
        for aliens in collisions.values():
            stats.score += 10 * len(aliens)
        sc.image_score()
        check_high_score(stats, sc)
        sc.image_harts()

    # Если все пришельцы уничтожены
    if len(aliens) == 0:
        bullets.empty()
        stats.level += 1
        sc.image_level()
        stats.alien_current_speed = stats.alien_base_speed + (stats.level - 1) * 0.02
        stats.alien_current_speed = min(stats.alien_current_speed, 0.5)
        new_shape = random.choice(list(army_shapes.keys()))
        create_army(screen, aliens, stats.alien_current_speed, new_shape, stats)

def gun_kill(stats, screen, bg, sc, gun, aliens, bullets):
    """столкновение пушки и армии пришельцев"""
    # Если жизни остались
    if stats.guns_left > 1:
        stats.guns_left -= 1
        screen.blit(bg, (0, 0))
        sc.image_harts()
        aliens.empty()
        bullets.empty()
        create_army(screen, aliens, stats.alien_current_speed, stats.current_shape, stats)
        gun.create_gun()
        time.sleep(1)
    # Если жизни закончились
    else:
        stats.run_game = False

def game_over_screen(stats, sc, gun, aliens, bullets, screen):
    """экран окончания игры"""
    game_over = GameOver(screen)
    while not stats.run_game:
        game_over.draw()
        if game_over.handle_events(stats, sc, gun, aliens, bullets, screen):
            break

def update_aliens(stats, screen, bg, sc, gun, aliens, bullets):
    """обновление позиции пришельцев"""
    aliens.update()

    # Проверка столкновения пушки с пришельцами
    if pygame.sprite.spritecollideany(gun, aliens):
        gun_kill(stats, screen, bg, sc, gun, aliens, bullets)

    # Проверка, достигли ли пришельцы нижнего края
    aliens_check(stats, screen, bg, sc, gun, aliens, bullets)

def aliens_check(stats, screen, bg, sc, gun, aliens, bullets):
    """проверка: добралась ли армия до края экрана"""
    screen_rect = screen.get_rect()

    for alien in aliens.sprites():
        # Если добралась
        if alien.rect.bottom >= screen_rect.bottom:
            gun_kill(stats, screen, bg, sc, gun, aliens, bullets)
            break

def create_army(screen, aliens, alien_speed=0.03, shape=None, stats=None):
    """создание армии пришельцев различной формы"""
    # Если форма не указана
    if shape is None:
        shape = random.choice(['rectangle', 'triangle', 'circle', 'two_squares', 'heart'])

    # Сохраняем выбранную форму в статистику
    if stats is not None:
        stats.current_shape = shape

    alien = Alien(screen)
    alien.speed = alien_speed
    w = alien.rect.width  # ширина пришельца
    h = alien.rect.height  # высота пришельца
    screen_width = 700 # ширина окна
    max_cols = int((screen_width - 2 * w) / w) # максимальное количество по горизонтали и вертикали
    start_row = 1  # отступ сверху
    selected_positions = []

    # Прямоугольник
    if shape == 'rectangle':
        form_map = [
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
        ]

    # Треугольник
    elif shape == 'triangle':
        form_map = [
            [1, 1, 1, 1, 1, 1, 1, 1, 1],
            [0, 1, 1, 1, 1, 1, 1, 1, 0],
            [0, 0, 1, 1, 1, 1, 1, 0, 0],
            [0, 0, 0, 1, 1, 1, 0, 0, 0],
            [0, 0, 0, 0, 1, 0, 0, 0, 0]
        ]

    # Круг
    elif shape == 'circle':
        form_map = [
            [0, 1, 1, 1, 0],
            [1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1],
            [0, 1, 1, 1, 0]
        ]

    # Два квадрата
    elif shape == 'two_squares':
        form_map = [
            [1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1],
            [1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1],
            [1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1],
            [1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1]
        ]

    # Сердце
    elif shape == 'heart':
        form_map = [
            [0, 1, 0, 0, 0, 1, 0],
            [1, 1, 1, 0, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1],
            [0, 1, 1, 1, 1, 1, 0],
            [0, 0, 1, 1, 1, 0, 0],
            [0, 0, 0, 1, 0, 0, 0]
        ]

    # Преобразование матрицы в координаты
    height = len(form_map)
    width = len(form_map[0])
    offset_col = (max_cols - width) // 2
    for row in range(height):
        for col in range(width):
            if form_map[row][col] == 1:
                x = w + (w * (offset_col + col))
                y = h + (h * (start_row + row))
                selected_positions.append((x, y))

    # Создание пришельцев
    for x, y in selected_positions:
        new_alien = Alien(screen)
        new_alien.speed = alien_speed
        new_alien.x = x
        new_alien.y = y
        new_alien.rect.x = x
        new_alien.rect.y = y
        aliens.add(new_alien)

def check_high_score(stats, sc):
    """проверка новых рекордов"""
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sc.image_high_score()

        # Созранение обновленного рекорда в файл
        with open('high_score.txt', 'w') as f:
            f.write(str(stats.high_score))