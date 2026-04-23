import pygame, sys
from bullet import Bullet
from alien import Alien
from game_over import GameOver
import time

def events(screen, gun, bullets):
    """обработка событий"""
    for event in pygame.event.get():
        # Закрытие окна игры
        if event.type == pygame.QUIT:
            sys.exit()

        # Обработка нажатия клавиш
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT or event.key == pygame.K_d: # Вправо
                gun.mright = True
            elif event.key == pygame.K_LEFT or event.key == pygame.K_a: # Влево
                gun.mleft = True
            elif event.key == pygame.K_SPACE: # Пробел
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
        create_army(screen, aliens)

def gun_kill(stats, screen, bg, sc, gun, aliens, bullets):
    """столкновение пушки и армии пришельцев"""
    # Если жизни остались
    if stats.guns_left > 1:
        stats.guns_left -= 1
        screen.blit(bg, (0, 0))
        sc.image_harts()
        aliens.empty()
        bullets.empty()
        create_army(screen, aliens)
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

def create_army(screen, aliens):
    """создание армии пришельцев"""
    alien = Alien(screen)
    alien_width = alien.rect.width
    number_alien_x = int((700 - 2 * alien_width) / alien_width)
    alien_height = alien.rect.height
    number_alien_y = int((700 - 100 - 2 * alien_height) / alien_height)

    for row_number in range(number_alien_y - 2):
        for alien_number in range(number_alien_x):
            alien = Alien(screen)
            alien.x = alien_width + (alien_width * alien_number)
            alien.y = alien_height + (alien_height * row_number)
            alien.rect.x = alien.x
            alien.rect.y = alien.rect.height + (alien.rect.height * row_number)
            alien.add(aliens)

def check_high_score(stats, sc):
    """проверка новых рекордов"""
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sc.image_high_score()

        # Созранение обновленного рекорда в файл
        with open('high_score.txt', 'w') as f:
            f.write(str(stats.high_score))