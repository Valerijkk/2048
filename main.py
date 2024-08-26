import pygame
import random

# Настройки Pygame
pygame.init()
tile_size = 100  # Размер плитки
board_size = 4  # Размер доски (4x4)
width = board_size * tile_size  # Ширина окна
height = board_size * tile_size + 50  # Высота окна (с запасом для отображения счета)
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("2048")

# Определение цветов для плиток и текста
colors = {
    0: (205, 193, 180),  # Пустая плитка
    2: (238, 228, 218),
    4: (237, 224, 200),
    8: (242, 177, 121),
    16: (245, 149, 99),
    32: (246, 124, 95),
    64: (246, 94, 59),
    128: (237, 207, 114),
    256: (237, 204, 97),
    512: (237, 200, 80),
    1024: (237, 197, 63),
    2048: (237, 194, 46),
    'light_text': (249, 246, 242),  # Светлый текст для темных плиток
    'dark_text': (119, 110, 101),   # Тёмный текст для светлых плиток
    'bg': (187, 173, 160)           # Фон игрового поля
}

# Загрузка шрифтов
font = pygame.font.SysFont(None, 55)  # Основной шрифт для чисел на плитках
score_font = pygame.font.SysFont(None, 35)  # Шрифт для отображения счета
game_over_font = pygame.font.SysFont(None, 75)  # Шрифт для отображения текста "Game Over"

def initialize_game():
    """Инициализация игровой доски"""
    board = [[0] * board_size for _ in range(board_size)]  # Создание пустой доски 4x4
    add_new_tile(board)  # Добавление первой случайной плитки
    add_new_tile(board)  # Добавление второй случайной плитки
    return board

def add_new_tile(board):
    """Добавление новой плитки на доску"""
    empty_cells = [(i, j) for i in range(board_size) for j in range(board_size) if board[i][j] == 0]
    # Если есть пустые ячейки, добавляем плитку 2 или 4 в случайную из них
    if empty_cells:
        i, j = random.choice(empty_cells)
        board[i][j] = random.choice([2, 4])

def rotate_board(board):
    """Поворот доски на 90 градусов"""
    return [list(row) for row in zip(*board[::-1])]

def compress(board):
    """Сжатие плиток влево"""
    new_board = [[0] * board_size for _ in range(board_size)]
    for i in range(board_size):
        pos = 0  # Позиция для перемещения плиток влево
        for j in range(board_size):
            if board[i][j] != 0:
                new_board[i][pos] = board[i][j]
                pos += 1
    return new_board

def merge(board):
    """Объединение плиток одинаковых значений и подсчет очков"""
    score = 0
    for i in range(board_size):
        for j in range(board_size - 1):
            if board[i][j] == board[i][j + 1] and board[i][j] != 0:
                board[i][j] *= 2  # Удваиваем значение плитки
                score += board[i][j]  # Добавляем значение к счету
                board[i][j + 1] = 0  # Удаляем объединённую плитку
    return board, score

def move_left(board):
    """Ход влево"""
    new_board = compress(board)  # Сжимаем плитки влево
    new_board, score = merge(new_board)  # Объединяем плитки и считаем очки
    new_board = compress(new_board)  # Снова сжимаем после объединения
    return new_board, score

def move_right(board):
    """Ход вправо"""
    board = rotate_board(rotate_board(board))  # Поворачиваем доску на 180 градусов
    board, score = move_left(board)  # Делаем ход влево (что соответствует ходу вправо)
    board = rotate_board(rotate_board(board))  # Возвращаем доску в исходное положение
    return board, score

def move_up(board):
    """Ход вверх"""
    board = rotate_board(rotate_board(rotate_board(board)))  # Поворачиваем доску на 270 градусов
    board, score = move_left(board)  # Делаем ход влево (что соответствует ходу вверх)
    board = rotate_board(board)  # Возвращаем доску в исходное положение
    return board, score

def move_down(board):
    """Ход вниз"""
    board = rotate_board(board)  # Поворачиваем доску на 90 градусов
    board, score = move_left(board)  # Делаем ход влево (что соответствует ходу вниз)
    board = rotate_board(rotate_board(rotate_board(board)))  # Возвращаем доску в исходное положение
    return board, score

def draw_board(board, score):
    """Отрисовка игровой доски и текущего счета"""
    screen.fill(colors['bg'])  # Заливаем фон цветом
    for i in range(board_size):
        for j in range(board_size):
            value = board[i][j]  # Получаем значение плитки
            color = colors[value]  # Получаем цвет плитки
            pygame.draw.rect(screen, color, (j * tile_size, i * tile_size + 50, tile_size, tile_size))  # Рисуем плитку
            if value != 0:  # Если плитка не пустая, рисуем на ней число
                text_color = colors['light_text'] if value > 4 else colors['dark_text']
                label = font.render(str(value), True, text_color)
                text_rect = label.get_rect(center=(j * tile_size + tile_size // 2, i * tile_size + tile_size // 2 + 50))
                screen.blit(label, text_rect)

    # Отображение текущего счета
    score_label = score_font.render(f"Счёт: {score}", True, colors['dark_text'])
    screen.blit(score_label, (10, 10))

def check_game_over(board):
    """Проверка окончания игры"""
    for i in range(board_size):
        for j in range(board_size):
            if board[i][j] == 0:
                return False  # Если есть пустая клетка, игра не окончена
            if i < board_size - 1 and board[i][j] == board[i + 1][j]:
                return False  # Если есть возможность слияния, игра не окончена
            if j < board_size - 1 and board[i][j] == board[i][j + 1]:
                return False
    return True  # Если нет пустых клеток и возможных слияний, игра окончена

def game_over_screen(score):
    """Отображение экрана окончания игры"""
    label = game_over_font.render("Ты проиграл!", True, colors['dark_text'])
    score_label = score_font.render(f"Финальный счёт: {score}", True, colors['dark_text'])
    text_rect = label.get_rect(center=(width // 2, height // 2 - 50))
    score_rect = score_label.get_rect(center=(width // 2, height // 2 + 20))
    screen.blit(label, text_rect)  # Отображаем сообщение об окончании игры
    screen.blit(score_label, score_rect)  # Отображаем итоговый счет
    pygame.display.update()
    pygame.time.wait(2000)  # Ждем 2 секунды перед завершением игры

def play_game():
    """Основной цикл игры"""
    board = initialize_game()  # Инициализируем игровую доску
    score = 0  # Начальный счет
    running = True
    while running:
        draw_board(board, score)  # Отрисовываем доску
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False  # Выход из игры при закрытии окна
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    board, move_score = move_up(board)
                elif event.key == pygame.K_DOWN:
                    board, move_score = move_down(board)
                elif event.key == pygame.K_LEFT:
                    board, move_score = move_left(board)
                elif event.key == pygame.K_RIGHT:
                    board, move_score = move_right(board)
                else:
                    continue

                score += move_score  # Обновляем счет
                add_new_tile(board)  # Добавляем новую плитку после хода

                if check_game_over(board):
                    draw_board(board, score)
                    pygame.display.update()
                    game_over_screen(score)  # Отображаем экран окончания игры
                    running = False

    pygame.quit()  # Завершаем работу Pygame

if __name__ == "__main__":
    play_game()
