import pygame
import random
import sys


pygame.init()

WIDTH, HEIGHT = 600, 600
CELL_SIZE = 20
GRID_WIDTH = WIDTH // CELL_SIZE
GRID_HEIGHT = HEIGHT // CELL_SIZE

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 200, 0)
RED = (220, 0, 0)
GRAY = (40, 40, 40)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 36)
large_font = pygame.font.SysFont(None, 56)


def random_apple(snake):
    while True:
        pos = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))
        if pos not in snake:
            return pos


class SnakeGame:
    def __init__(self):
        self.reset()

    def reset(self):
        self.snake = [(10, 10), (9, 10), (8, 10)]
        self.direction = (1, 0)
        self.next_direction = (1, 0)
        self.apple = random_apple(self.snake)
        self.score = 0
        self.game_over = False

    def change_direction(self, new_direction):
        if (new_direction[0] * -1, new_direction[1] * -1) != self.direction:
            self.next_direction = new_direction

    def move(self):
        if self.game_over:
            return

        self.direction = self.next_direction
        head_x, head_y = self.snake[0]
        dx, dy = self.direction
        new_head = (head_x + dx, head_y + dy)

        if (
            new_head[0] < 0
            or new_head[0] >= GRID_WIDTH
            or new_head[1] < 0
            or new_head[1] >= GRID_HEIGHT
        ):
            self.game_over = True
            return

        if new_head in self.snake:
            self.game_over = True
            return

        self.snake.insert(0, new_head)

        if new_head == self.apple:
            self.score += 1
            self.apple = random_apple(self.snake)
        else:
            self.snake.pop()

    def draw(self):
        screen.fill(BLACK)

        for x in range(0, WIDTH, CELL_SIZE):
            pygame.draw.line(screen, GRAY, (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, CELL_SIZE):
            pygame.draw.line(screen, GRAY, (0, y), (WIDTH, y))

        apple_rect = pygame.Rect(
            self.apple[0] * CELL_SIZE,
            self.apple[1] * CELL_SIZE,
            CELL_SIZE,
            CELL_SIZE,
        )
        pygame.draw.rect(screen, RED, apple_rect)

        for i, segment in enumerate(self.snake):
            rect = pygame.Rect(
                segment[0] * CELL_SIZE,
                segment[1] * CELL_SIZE,
                CELL_SIZE,
                CELL_SIZE,
            )
            pygame.draw.rect(screen, GREEN, rect)
            if i == 0:
                pygame.draw.rect(screen, WHITE, rect, 2)

        score_text = font.render(f"Score: {self.score}", True, WHITE)
        screen.blit(score_text, (10, 10))

        if self.game_over:
            game_over_text = large_font.render("Game Over", True, RED)
            restart_text = font.render("Press R to Restart or Q to Quit", True, WHITE)
            screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2 - 50))
            screen.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, HEIGHT // 2 + 10))

        pygame.display.flip()


def main():
    game = SnakeGame()
    move_event = pygame.USEREVENT + 1
    pygame.time.set_timer(move_event, 120)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    game.change_direction((0, -1))
                elif event.key == pygame.K_DOWN:
                    game.change_direction((0, 1))
                elif event.key == pygame.K_LEFT:
                    game.change_direction((-1, 0))
                elif event.key == pygame.K_RIGHT:
                    game.change_direction((1, 0))
                elif event.key == pygame.K_r and game.game_over:
                    game.reset()
                elif event.key == pygame.K_q and game.game_over:
                    pygame.quit()
                    sys.exit()

            if event.type == move_event:
                game.move()

        game.draw()
        clock.tick(60)


if __name__ == "__main__":
    main()
5
