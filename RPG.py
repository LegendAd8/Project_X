import pygame
import random
import sys


pygame.init()

WIDTH, HEIGHT = 500, 700
FPS = 60
WHITE = (255, 255, 255)
BLACK = (10, 10, 20)
RED = (220, 70, 70)
YELLOW = (255, 210, 70)
GRAY = (180, 180, 180)
CYAN = (120, 220, 255)
GREEN = (100, 220, 120)
BROWN = (120, 72, 40)
DARK_GREEN = (30, 110, 50)
SAND = (194, 178, 128)
PURPLE = (130, 80, 170)
ICE = (180, 230, 255)
ORANGE = (255, 140, 60)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Rocket Escape")
clock = pygame.time.Clock()
font = pygame.font.SysFont("arial", 28)
small_font = pygame.font.SysFont("arial", 20)
large_font = pygame.font.SysFont("arial", 46, bold=True)
menu_font = pygame.font.SysFont("arial", 34, bold=True)


LEVEL_THEMES = [
    {
        "name": "Stone Canyon",
        "top": (70, 70, 90),
        "bottom": (130, 130, 150),
        "obstacle_colors": [(110, 110, 110), (150, 150, 150), (90, 90, 90)],
        "star_color": (230, 230, 230),
    },
    {
        "name": "Jungle Sky",
        "top": (20, 80, 40),
        "bottom": (90, 170, 90),
        "obstacle_colors": [(50, 120, 50), (90, 60, 30), (30, 150, 80)],
        "star_color": (220, 255, 220),
    },
    {
        "name": "Desert Storm",
        "top": (170, 120, 50),
        "bottom": (240, 200, 120),
        "obstacle_colors": [(180, 130, 80), (210, 160, 90), (150, 100, 60)],
        "star_color": (255, 245, 210),
    },
    {
        "name": "Ice World",
        "top": (100, 170, 220),
        "bottom": (220, 245, 255),
        "obstacle_colors": [(170, 220, 255), (120, 190, 235), (210, 240, 255)],
        "star_color": (255, 255, 255),
    },
    {
        "name": "Volcano Zone",
        "top": (70, 20, 20),
        "bottom": (220, 80, 30),
        "obstacle_colors": [(140, 30, 20), (220, 90, 20), (255, 140, 60)],
        "star_color": (255, 220, 180),
    },
    {
        "name": "Space Rift",
        "top": (10, 10, 40),
        "bottom": (70, 30, 120),
        "obstacle_colors": [(120, 90, 180), (80, 160, 255), (170, 120, 240)],
        "star_color": (255, 255, 255),
    },
]


class Rocket:
    def __init__(self):
        self.width = 40
        self.height = 70
        self.rect = pygame.Rect(WIDTH // 2 - 20, HEIGHT - 120, self.width, self.height)
        self.speed = 7

    def move_keyboard(self, keys):
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.rect.x += self.speed
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.rect.y += self.speed
        self.clamp()

    def move_mouse(self, mouse_pos):
        mouse_x, mouse_y = mouse_pos
        self.rect.centerx += int((mouse_x - self.rect.centerx) * 0.18)
        self.rect.centery += int((mouse_y - self.rect.centery) * 0.18)
        self.clamp()

    def clamp(self):
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT

    def draw(self, surface):
        body = [
            (self.rect.centerx, self.rect.top),
            (self.rect.left, self.rect.bottom - 12),
            (self.rect.right, self.rect.bottom - 12),
        ]
        pygame.draw.polygon(surface, WHITE, body)
        pygame.draw.rect(surface, RED, (self.rect.x + 8, self.rect.y + 20, 24, 28))
        pygame.draw.circle(surface, CYAN, (self.rect.centerx, self.rect.y + 20), 8)
        pygame.draw.polygon(surface, YELLOW, [
            (self.rect.x + 10, self.rect.bottom - 12),
            (self.rect.x + 18, self.rect.bottom + 12),
            (self.rect.x + 22, self.rect.bottom - 12),
        ])
        pygame.draw.polygon(surface, YELLOW, [
            (self.rect.x + 18, self.rect.bottom - 12),
            (self.rect.x + 24, self.rect.bottom + 15),
            (self.rect.x + 30, self.rect.bottom - 12),
        ])


class Obstacle:
    def __init__(self, x, y, width, height, speed, color):
        self.rect = pygame.Rect(x, y, width, height)
        self.speed = speed
        self.color = color

    def update(self):
        self.rect.y += self.speed

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect, border_radius=8)
        pygame.draw.rect(surface, WHITE, self.rect, 2, border_radius=8)


class Star:
    def __init__(self):
        self.reset()

    def reset(self):
        self.x = random.randint(0, WIDTH)
        self.y = random.randint(0, HEIGHT)
        self.speed = random.randint(2, 7)
        self.size = random.randint(1, 3)

    def update(self):
        self.y += self.speed
        if self.y > HEIGHT:
            self.x = random.randint(0, WIDTH)
            self.y = 0
            self.speed = random.randint(2, 7)
            self.size = random.randint(1, 3)

    def draw(self, surface, color):
        pygame.draw.circle(surface, color, (self.x, self.y), self.size)


class Button:
    def __init__(self, x, y, w, h, text):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text

    def draw(self, surface, active=False):
        bg = (90, 90, 150) if active else (50, 50, 90)
        pygame.draw.rect(surface, bg, self.rect, border_radius=12)
        pygame.draw.rect(surface, WHITE, self.rect, 2, border_radius=12)
        txt = font.render(self.text, True, WHITE)
        surface.blit(txt, (self.rect.centerx - txt.get_width() // 2, self.rect.centery - txt.get_height() // 2))

    def clicked(self, pos):
        return self.rect.collidepoint(pos)


class Game:
    def __init__(self):
        self.stars = [Star() for _ in range(70)]
        self.control_mode = None
        self.state = "menu"
        self.keyboard_button = Button(WIDTH // 2 - 120, HEIGHT // 2 - 10, 240, 55, "Keyboard Mode")
        self.mouse_button = Button(WIDTH // 2 - 120, HEIGHT // 2 + 70, 240, 55, "Mouse Mode")
        self.reset()

    def reset(self):
        self.rocket = Rocket()
        self.obstacles = []
        self.score = 0
        self.level = 1
        self.spawn_timer = 0
        self.pattern_index = 0
        self.game_over = False
        self.flash_timer = 0
        self.level_message_timer = 120

    def theme(self):
        idx = min(self.level - 1, len(LEVEL_THEMES) - 1)
        return LEVEL_THEMES[idx]

    def obstacle_palette(self):
        return self.theme()["obstacle_colors"]

    def current_speed(self):
        return 4 + self.level

    def spawn_interval(self):
        return max(18, 70 - self.level * 4)

    def update_level(self):
        new_level = min(int(self.score) // 15 + 1, len(LEVEL_THEMES))
        if new_level != self.level:
            self.level = new_level
            self.level_message_timer = 120

    def generate_pattern(self):
        speed = self.current_speed()
        color_choices = self.obstacle_palette()
        pattern_type = (self.level - 1) % 6

        if pattern_type == 0:
            gap_x = random.randint(90, WIDTH - 170)
            self.obstacles.append(Obstacle(0, -40, gap_x, 40, speed, random.choice(color_choices)))
            self.obstacles.append(Obstacle(gap_x + 80, -40, WIDTH - (gap_x + 80), 40, speed, random.choice(color_choices)))

        elif pattern_type == 1:
            lane_width = WIDTH // 4
            safe_lane = random.randint(0, 3)
            for lane in range(4):
                if lane != safe_lane:
                    self.obstacles.append(Obstacle(lane * lane_width + 6, -80, lane_width - 12, 80, speed, random.choice(color_choices)))

        elif pattern_type == 2:
            for _ in range(3 + min(self.level, 4)):
                width = random.randint(45, 95)
                x = random.randint(0, WIDTH - width)
                y = random.randint(-220, -40)
                self.obstacles.append(Obstacle(x, y, width, 34, speed + 1, random.choice(color_choices)))

        elif pattern_type == 3:
            side = self.pattern_index % 2
            if side == 0:
                self.obstacles.append(Obstacle(0, -120, WIDTH - 120, 120, speed, random.choice(color_choices)))
            else:
                self.obstacles.append(Obstacle(120, -120, WIDTH - 120, 120, speed, random.choice(color_choices)))
            self.pattern_index += 1

        elif pattern_type == 4:
            center_gap = random.randint(110, WIDTH - 110)
            gap_size = 100
            left_w = center_gap - gap_size // 2
            right_x = center_gap + gap_size // 2
            if left_w > 0:
                self.obstacles.append(Obstacle(0, -55, left_w, 55, speed + 1, random.choice(color_choices)))
            if right_x < WIDTH:
                self.obstacles.append(Obstacle(right_x, -55, WIDTH - right_x, 55, speed + 1, random.choice(color_choices)))
            pillar_x = random.choice([40, WIDTH // 2 - 25, WIDTH - 90])
            self.obstacles.append(Obstacle(pillar_x, -160, 50, 90, speed + 1, random.choice(color_choices)))

        else:
            lane_width = WIDTH // 5
            safe_lanes = random.sample(range(5), 2)
            for lane in range(5):
                if lane not in safe_lanes:
                    h = random.choice([60, 90, 120])
                    self.obstacles.append(Obstacle(lane * lane_width + 4, -h, lane_width - 8, h, speed + 2, random.choice(color_choices)))

    def update(self):
        for star in self.stars:
            star.update()

        if self.state != "playing":
            if self.flash_timer > 0:
                self.flash_timer -= 1
            return

        self.score += 0.03
        self.update_level()
        self.spawn_timer += 1

        if self.spawn_timer >= self.spawn_interval():
            self.generate_pattern()
            self.spawn_timer = 0

        for obstacle in self.obstacles:
            obstacle.update()

        self.obstacles = [obs for obs in self.obstacles if obs.rect.top < HEIGHT + 20]

        for obstacle in self.obstacles:
            if self.rocket.rect.colliderect(obstacle.rect):
                self.game_over = True
                self.state = "game_over"
                self.flash_timer = 18
                break

        if self.level_message_timer > 0:
            self.level_message_timer -= 1

    def draw_background(self):
        theme = self.theme()
        top = theme["top"]
        bottom = theme["bottom"]
        for y in range(HEIGHT):
            ratio = y / HEIGHT
            r = int(top[0] * (1 - ratio) + bottom[0] * ratio)
            g = int(top[1] * (1 - ratio) + bottom[1] * ratio)
            b = int(top[2] * (1 - ratio) + bottom[2] * ratio)
            pygame.draw.line(screen, (r, g, b), (0, y), (WIDTH, y))
        for star in self.stars:
            star.draw(screen, theme["star_color"])
        self.draw_theme_decor(theme["name"])

    def draw_theme_decor(self, name):
        if name == "Stone Canyon":
            for i in range(0, WIDTH, 90):
                pygame.draw.polygon(screen, (80, 80, 90), [(i, HEIGHT), (i + 50, HEIGHT - 90), (i + 100, HEIGHT)])
        elif name == "Jungle Sky":
            for i in range(0, WIDTH, 80):
                pygame.draw.rect(screen, (40, 90, 40), (i, HEIGHT - 130, 20, 130))
                pygame.draw.circle(screen, (20, 130, 50), (i + 10, HEIGHT - 140), 40)
        elif name == "Desert Storm":
            pygame.draw.ellipse(screen, (210, 180, 110), (30, HEIGHT - 120, 220, 80))
            pygame.draw.ellipse(screen, (190, 160, 100), (220, HEIGHT - 100, 250, 70))
        elif name == "Ice World":
            for i in range(0, WIDTH, 120):
                pygame.draw.polygon(screen, (220, 245, 255), [(i, HEIGHT), (i + 40, HEIGHT - 100), (i + 80, HEIGHT)])
        elif name == "Volcano Zone":
            pygame.draw.polygon(screen, (70, 30, 20), [(50, HEIGHT), (170, HEIGHT - 150), (290, HEIGHT)])
            pygame.draw.polygon(screen, (90, 35, 20), [(250, HEIGHT), (360, HEIGHT - 190), (480, HEIGHT)])
            pygame.draw.circle(screen, (255, 130, 60), (360, HEIGHT - 210), 16)
        elif name == "Space Rift":
            pygame.draw.circle(screen, (210, 210, 255), (80, 100), 35)
            pygame.draw.circle(screen, (160, 100, 255), (390, 160), 50, 4)

    def draw_hud(self):
        score_text = font.render(f"Score: {int(self.score)}", True, WHITE)
        level_text = font.render(f"Level: {self.level}", True, WHITE)
        control_text = small_font.render(f"Mode: {self.control_mode.title() if self.control_mode else 'None'}", True, WHITE)
        theme_text = small_font.render(self.theme()["name"], True, WHITE)
        screen.blit(score_text, (15, 12))
        screen.blit(level_text, (WIDTH - 130, 12))
        screen.blit(control_text, (15, 48))
        screen.blit(theme_text, (WIDTH - theme_text.get_width() - 15, 48))
        if self.control_mode == "keyboard":
            help_text = small_font.render("Move: Arrow keys or WASD", True, WHITE)
        else:
            help_text = small_font.render("Move: Mouse", True, WHITE)
        screen.blit(help_text, (15, 76))
        if self.level_message_timer > 0 and self.state == "playing":
            msg = menu_font.render(self.theme()["name"], True, WHITE)
            screen.blit(msg, (WIDTH // 2 - msg.get_width() // 2, 110))

    def draw_menu(self):
        self.draw_background()
        title = large_font.render("ROCKET ESCAPE", True, WHITE)
        subtitle = font.render("Choose your control mode", True, WHITE)
        info = small_font.render("Each level changes obstacle pattern, background, and theme", True, WHITE)
        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 140))
        screen.blit(subtitle, (WIDTH // 2 - subtitle.get_width() // 2, 220))
        screen.blit(info, (WIDTH // 2 - info.get_width() // 2, 260))
        self.keyboard_button.draw(screen)
        self.mouse_button.draw(screen)

    def draw_game_over(self):
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))
        screen.blit(overlay, (0, 0))
        title = large_font.render("GAME OVER", True, WHITE)
        info1 = font.render(f"Final Score: {int(self.score)}", True, WHITE)
        info2 = font.render(f"Reached Level: {self.level}", True, WHITE)
        info3 = small_font.render("Press R to restart menu or Q to quit", True, WHITE)
        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, HEIGHT // 2 - 90))
        screen.blit(info1, (WIDTH // 2 - info1.get_width() // 2, HEIGHT // 2 - 20))
        screen.blit(info2, (WIDTH // 2 - info2.get_width() // 2, HEIGHT // 2 + 20))
        screen.blit(info3, (WIDTH // 2 - info3.get_width() // 2, HEIGHT // 2 + 70))

    def draw(self):
        if self.state == "menu":
            self.draw_menu()
            return
        self.draw_background()
        for obstacle in self.obstacles:
            obstacle.draw(screen)
        if not (self.game_over and self.flash_timer % 4 < 2):
            self.rocket.draw(screen)
        self.draw_hud()
        if self.state == "game_over":
            self.draw_game_over()



def main():
    game = Game()

    while True:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if game.state == "menu":
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if game.keyboard_button.clicked(event.pos):
                        game.control_mode = "keyboard"
                        game.reset()
                        game.state = "playing"
                    elif game.mouse_button.clicked(event.pos):
                        game.control_mode = "mouse"
                        game.reset()
                        game.state = "playing"

            elif game.state == "game_over":
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        game.reset()
                        game.state = "menu"
                        game.control_mode = None
                    elif event.key == pygame.K_q:
                        pygame.quit()
                        sys.exit()

        if game.state == "playing":
            keys = pygame.key.get_pressed()
            if game.control_mode == "keyboard":
                game.rocket.move_keyboard(keys)
            elif game.control_mode == "mouse":
                game.rocket.move_mouse(pygame.mouse.get_pos())
            game.update()
        else:
            game.update()

        game.draw()
        pygame.display.flip()


if __name__ == "__main__":
    main()
