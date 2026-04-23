class Stats():
    """отслеживание статисткики"""

    def __init__(self):
        """инициализирует статистику"""
        self.reset_stats()
        self.run_game = True # Флаг активности игры

        # Загрузка рекорда из файла
        with open('high_score.txt', 'r') as f:
            self.high_score = int(f.readline())

    def reset_stats(self):
        """статистика, изменяющаяся во время игры"""
        self.guns_left = 3 # Кол-во жизней
        self.score = 0 # Счет