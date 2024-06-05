import pygame
from pygame.locals import *


class Game:
    def __init__(self):
        pygame.font.init()
        pygame.init()
        self.width = 505
        self.height = 905
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.wood_color = (222, 184, 135)
        self.black2 = (120, 0, 0)
        self.caption = "Python Breakout Game"
        self.clock = pygame.time.Clock()
        self.running = True
        self.game_over = False
        self.game_status = "start"
        self.score = 0
        self.score_increment = 10
        self.font = pygame.font.Font(None, 36)

        self.paddle = Paddle(self.screen, 190, 880, 120, 15)
        self.ball = Ball(self.screen, 250, 870, 1, 1)
        self.bricks = self.create_bricks()

        self.img = pygame.image.load('horse.jpg')
        self.img = pygame.transform.scale(self.img, (510, 1400))
        self.img.convert()
        self.img_rect = Rect(0, 0, 250, 500)

    def create_bricks(self):
        bricks = []
        color = (135, 206, 250)
        for i in range(35, 440, 55):
            for j in range(50, 250, 55):
                bricks.append(Brick(self.screen, i, j, 48, 15, color))
        return bricks

    def reset_game(self):
        self.score = 0
        self.game_over = False
        self.paddle = Paddle(self.screen, 190, 880, 120, 15)
        self.ball = Ball(self.screen, 250, 870, 1, 1)
        self.bricks = self.create_bricks()
        self.game_status = "start"

    def draw_game_over(self):
        self.screen.fill((0, 0, 0))
        font1 = pygame.font.SysFont('arial', 40)
        title = font1.render("Game OVER", True, (255, 255, 255))
        restart_button = font1.render('R - Restart', True, (255, 255, 255))
        quit_button = font1.render('Q - Quit', True, (255, 255, 255))
        self.screen.blit(title, (self.width / 2 - title.get_width() / 2, self.height / 2 - title.get_height() / 3))
        self.screen.blit(restart_button, (
        self.width / 2 - restart_button.get_width() / 2, self.height / 1.9 + restart_button.get_height()))
        self.screen.blit(quit_button,
                         (self.width / 2 - quit_button.get_width() / 2, self.height / 2 + quit_button.get_height() / 2))
        pygame.display.update()

    def draw_restart_over(self):
        self.screen.fill((0, 0, 0))
        font1 = pygame.font.SysFont('arial', 40)
        title = font1.render("WINNER CHICKEN", True, (255, 255, 255))
        restart_button = font1.render('R - Restart', True, (255, 255, 255))
        quit_button = font1.render('Q - Quit', True, (255, 255, 255))
        self.screen.blit(title, (self.width / 2 - title.get_width() / 2, self.height / 2 - title.get_height() / 3))
        self.screen.blit(restart_button, (
        self.width / 2 - restart_button.get_width() / 2, self.height / 1.9 + restart_button.get_height()))
        self.screen.blit(quit_button,
                         (self.width / 2 - quit_button.get_width() / 2, self.height / 2 + quit_button.get_height() / 2))
        pygame.display.update()

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            if self.game_over and self.game_status == "stop":
                self.draw_game_over()
                keys = pygame.key.get_pressed()
                if keys[pygame.K_r]:
                    self.reset_game()
                if keys[pygame.K_q]:
                    self.running = False
                    pygame.quit()

            elif self.game_over and self.game_status == "start":
                self.draw_restart_over()
                keys = pygame.key.get_pressed()
                if keys[pygame.K_r]:
                    self.reset_game()
                if keys[pygame.K_q]:
                    self.running = False
                    pygame.quit()

            elif not self.game_over:
                keys = pygame.key.get_pressed()
                if keys[pygame.K_RIGHT]:
                    self.paddle.move_right(1, 0)
                if keys[pygame.K_LEFT]:
                    self.paddle.move_left(1, 0)

                self.screen.fill(self.wood_color)
                self.screen.blit(self.img, self.img_rect)

                for brick in self.bricks:
                    brick.draw()

                self.ball.move()
                if self.ball.check_collision(self.paddle.rect):
                    self.ball.bounce()

                for brick in self.bricks:
                    if self.ball.check_collision(brick.rect):
                        self.ball.bounce()
                        self.score += self.score_increment
                        self.bricks.remove(brick)

                if self.ball.is_out_of_bounds(self.height):
                    self.game_over = True
                    self.game_status = "stop"

                if not self.bricks:
                    self.game_over = True
                    self.game_status = "start"

                self.clock.tick(250)
                score_text = self.font.render(f'Score: {self.score}', True, (255, 255, 255))
                self.screen.blit(score_text, (10, 10))
                self.ball.draw()
                self.paddle.draw()
                pygame.display.set_caption(self.caption)
                pygame.display.update()

        pygame.quit()


class Paddle:
    def __init__(self, screen, x, y, width, height):
        self.screen = screen
        self.rect = pygame.Rect(x, y, width, height)
        self.color = (120, 0, 0)

    def move_left(self, x, y):
        if self.rect.left - x > 3:
            self.rect.move_ip(-x, y)

    def move_right(self, x, y):
        if self.rect.right + x < 503:
            self.rect.move_ip(x, y)

    def draw(self):
        pygame.draw.rect(self.screen, self.color, self.rect)


class Ball:
    def __init__(self, screen, x, y, vx, vy):
        self.screen = screen
        self.rect = pygame.Rect(x, y, 10, 10)
        self.speed = [vx, vy]
        self.color = (128, 128, 128)

    def move(self):
        self.rect = self.rect.move(self.speed)
        if self.rect.left < 0 or self.rect.right > 505:
            self.speed[0] = -self.speed[0]
        if self.rect.top < 0:
            self.speed[1] = -self.speed[1]

    def bounce(self):
        self.speed[1] = -self.speed[1]

    def check_collision(self, other_rect):
        return self.rect.colliderect(other_rect)

    def is_out_of_bounds(self, height):
        return self.rect.bottom > height

    def draw(self):
        pygame.draw.ellipse(self.screen, self.color, self.rect)


class Brick:
    def __init__(self, screen, x, y, width, height, color):
        self.screen = screen
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color

    def draw(self):
        pygame.draw.rect(self.screen, self.color, self.rect)


if __name__ == "__main__":
    game = Game()
    game.run()
