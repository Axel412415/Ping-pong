import pygame
import sys
from random import randint

# Инициализация Pygame
pygame.init()

# Класс GameSprite
class GameSprite(pygame.sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        pygame.sprite.Sprite.__init__(self)
        # Если изображение не найдено, создаем прямоугольник
        try:
            self.image = pygame.transform.scale(pygame.image.load(player_image), (size_x, size_y))
        except:
            self.image = pygame.Surface((size_x, size_y))
            self.image.fill((255, 255, 255))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    
    def reset(self, surface):
        surface.blit(self.image, (self.rect.x, self.rect.y))

# Класс ракетки
class Paddle(GameSprite):
    def update_left(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w] and self.rect.y > 5:
            self.rect.y -= self.speed
        if keys[pygame.K_s] and self.rect.y < win_height - self.rect.height:
            self.rect.y += self.speed
    
    def update_right(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] and self.rect.y > 5:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN] and self.rect.y < win_height - self.rect.height:
            self.rect.y += self.speed

# Класс мяча
class Ball(GameSprite):
    def __init__(self, player_x, player_y, size_x, size_y, speed_x, speed_y):
        super().__init__("", player_x, player_y, size_x, size_y, 0)
        self.image.fill((255, 255, 255))  # Белый мяч
        self.speed_x = speed_x
        self.speed_y = speed_y
        self.initial_speed_x = speed_x
        self.initial_speed_y = speed_y
    
    def update(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y
        
        # Отскок от верхней и нижней границы
        if self.rect.y <= 0 or self.rect.y >= win_height - self.rect.height:
            self.speed_y *= -1
        
        # Если мяч ушел за границы
        if self.rect.x < 0:
            return "right"
        if self.rect.x > win_width:
            return "left"
        return None
    
    def reset_ball(self):
        self.rect.x = win_width // 2 - self.rect.width // 2
        self.rect.y = win_height // 2 - self.rect.height // 2
        self.speed_x = self.initial_speed_x * (1 if randint(0, 1) else -1)
        self.speed_y = self.initial_speed_y * (1 if randint(0, 1) else -1)

# Параметры экрана
win_width = 700
win_height = 500
window = pygame.display.set_mode((win_width, win_height))
pygame.display.set_caption("Ping Pong")

# Цвета
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# Создание спрайтов без изображений
left_paddle = Paddle("", 30, win_height//2 - 50, 20, 100, 8)
left_paddle.image.fill(RED)
right_paddle = Paddle("", win_width - 50, win_height//2 - 50, 20, 100, 8)
right_paddle.image.fill(RED)
ball = Ball(win_width//2 - 15, win_height//2 - 15, 20, 20, 5, 5)

# Группы спрайтов
paddles = pygame.sprite.Group()
paddles.add(left_paddle)
paddles.add(right_paddle)
balls = pygame.sprite.Group()
balls.add(ball)

# Счет
left_score = 0
right_score = 0
font = pygame.font.Font(None, 74)
small_font = pygame.font.Font(None, 36)

# Игровой цикл
run = True
finish = False
clock = pygame.time.Clock()

while run:
    # Обработка событий
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                run = False
            if event.key == pygame.K_r and finish:
                # Перезапуск игры
                finish = False
                left_score = 0
                right_score = 0
                ball.reset_ball()
    
    if not finish:
        # Обновление спрайтов
        left_paddle.update_left()
        right_paddle.update_right()
        result = ball.update()
        
        # Проверка, кто получил очко
        if result == "left":
            left_score += 1
            ball.reset_ball()
        elif result == "right":
            right_score += 1
            ball.reset_ball()
        
        # Проверка на победу
        if left_score >= 5 or right_score >= 5:
            finish = True
        
        # Проверка столкновения мяча с ракетками
        if pygame.sprite.spritecollide(ball, paddles, False):
            ball.speed_x *= -1.1
            # Добавляем небольшой случайный угол отскока
            ball.speed_y += randint(-2, 2)
            # Ограничиваем максимальную скорость по Y
            ball.speed_y = max(-10, min(10, ball.speed_y))
        
        # Отрисовка
        window.fill(BLACK)
        
        # Рисуем центральную линию
        for i in range(0, win_height, 30):
            pygame.draw.rect(window, WHITE, (win_width//2 - 2, i, 4, 15))
        
        # Отрисовка спрайтов
        left_paddle.reset(window)
        right_paddle.reset(window)
        ball.reset(window)
        
        # Отрисовка счета
        left_text = font.render(str(left_score), True, WHITE)
        right_text = font.render(str(right_score), True, WHITE)
        window.blit(left_text, (win_width//4 - left_text.get_width()//2, 20))
        window.blit(right_text, (win_width*3//4 - right_text.get_width()//2, 20))
    else:
        # Экран окончания игры
        window.fill(BLACK)
        winner_text = font.render("LEFT WINS!" if left_score >= 5 else "RIGHT WINS!", True, WHITE)
        restart_text = small_font.render("Press R to restart or ESC to quit", True, WHITE)
        window.blit(winner_text, (win_width//2 - winner_text.get_width()//2, win_height//2 - 50))
        window.blit(restart_text, (win_width//2 - restart_text.get_width()//2, win_height//2 + 50))
    
    pygame.display.update()
    clock.tick(60)

pygame.quit()
sys.exit()
