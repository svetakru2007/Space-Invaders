class Stats():
    """отслеживание статистики"""

    def __init__(self):
        """инициализирует статистику"""
        self.reset_stats()
        self.run_game = True # флаг активности игры

        # Загрузка рекорда из файла
        with open('high_score.txt', 'r') as f:
            self.high_score = int(f.readline())

    def reset_stats(self):
        """статистика, изменяющаяся во время игры"""
        self.guns_left = 3 # кол-во жизней
        self.score = 0 # счет
        self.level = 1  # текущий уровень
        self.alien_base_speed = 0.03  # начальная скорость пришельца
        self.alien_current_speed = 0.03  # текущая скорость пришельца
        self.current_shape = 'rectangle' # форма армии по умолчанию