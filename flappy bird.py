import math
import random
import sys
import array
import pygame


pygame.init()
pygame.mixer.init(frequency=44100, size=-16, channels=1)

WIDTH, HEIGHT = 520, 720
FPS = 60
GROUND_HEIGHT = 90
PIPE_WIDTH = 80
PIPE_GAP = 185
GRAVITY = 0.34
FLAP_STRENGTH = -7.1

WHITE = (255, 255, 255)
BLACK = (20, 20, 30)
YELLOW = (255, 215, 80)
ORANGE = (255, 145, 60)
RED = (220, 70, 70)
GREEN = (60, 180, 90)
DARK_GREEN = (35, 120, 60)
BLUE = (90, 170, 255)
BROWN = (120, 75, 45)
GRAY = (160, 160, 170)
PURPLE = (120, 90, 190)
ICE = (200, 235, 255)
GOLD = (245, 220, 90)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Sky Flap Adventure")
clock = pygame.time.Clock()
font = pygame.font.SysFont("arial", 28)
small_font = pygame.font.SysFont("arial", 20)
large_font = pygame.font.SysFont("arial", 50, bold=True)
menu_font = pygame.font.SysFont("arial", 34, bold=True)


LEVELS = [
    {
        "name": "Sunny Meadow",
        "sky_top": (120, 200, 255),
        "sky_bottom": (220, 245, 255),
        "ground": (110, 190, 90),
        "pipe": (65, 180, 90),
        "music": [262, 294, 330, 392, 330, 294],
    },
    {
        "name": "Jungle Falls",
        "sky_top": (50, 140, 100),
        "sky_bottom": (130, 220, 170),
        "ground": (70, 130, 60),
        "pipe": (50, 150, 70),
        "music": [220, 247, 262, 294, 262, 247],
    },
    {
        "name": "Desert Wind",
        "sky_top": (250, 190, 110),
        "sky_bottom": (255, 225, 170),
        "ground": (195, 155, 95),
        "pipe": (180, 125, 70),
        "music": [247, 277, 330, 370, 330, 277],
    },
    {
        "name": "Snow Peaks",
        "sky_top": (150, 200, 240),
        "sky_bottom": (240, 250, 255),
        "ground": (210, 230, 240),
        "pipe": (150, 190, 220),
        "music": [294, 330, 370, 440, 370, 330],
    },
    {
        "name": "Sunset Volcano",
        "sky_top": (120, 50, 70),
        "sky_bottom": (255, 120, 70),
        "ground": (85, 45, 35),
        "pipe": (150, 70, 50),
        "music": [196, 220, 247, 294, 247, 220],
    },
    {
        "name": "Moonlight Sky",
        "sky_top": (30, 35, 90),
        "sky_bottom": (120, 90, 180),
        "ground": (70, 65, 110),
        "pipe": (110, 100, 180),
        "music": [330, 370, 392, 494, 392, 370],
    },
]


CHARACTERS = [
    {
        "name": "Yellow Duck",
        "body": (255, 220, 90),
        "wing": (255, 180, 60),
        "beak": (255, 120, 50),
        "type": "duck",
    },
    {
        "name": "Blue Bird",
        "body": (100, 180, 255),
        "wing": (70, 130, 220),
        "beak": (255, 190, 70),
        "type": "bird",
    },
    {
        "name": "White Eagle",
        "body": (235, 235, 240),
        "wing": (150, 150, 160),
        "beak": (245, 210, 90),
        "type": "eagle",
    },
]


NOTE_CACHE = {}


def make_tone(frequency, duration=0.42, volume=0.11):
    key = (frequency, duration, volume)
    if key in NOTE_CACHE:
        return NOTE_CACHE[key]
    sample_rate = 44100
    total_samples = int(sample_rate * duration)
    buf = array.array("h")
    fade = int(sample_rate * 0.08)
    for i in range(total_samples):
        t = i / sample_rate
        wave = 0.72 * math.sin(2 * math.pi * frequency * t)
        wave += 0.18 * math.sin(2 * math.pi * frequency * 2 * t)
        wave += 0.10 * math.sin(2 * math.pi * frequency * 0.5 * t)
        env = 1.0
        if i < fade:
            env = i / fade
        elif i > total_samples - fade:
            env = max(0, (total_samples - i) / fade)
        value = int(32767 * volume * wave * env)
        buf.append(value)
    sound = pygame.mixer.Sound(buffer=buf.tobytes())
    NOTE_CACHE[key] = sound
    return sound


class Button:
    def __init__(self, x, y, w, h, text):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text

    def draw(self, surface, active=False):
        bg = (90, 100, 180) if active else (60, 70, 130)
        pygame.draw.rect(surface, bg, self.rect, border_radius=14)
        pygame.draw.rect(surface, WHITE, self.rect, 2, border_radius=14)
        txt = font.render(self.text, True, WHITE)
        surface.blit(txt, (self.rect.centerx - txt.get_width() // 2, self.rect.centery - txt.get_height() // 2))

    def clicked(self, pos):
        return self.rect.collidepoint(pos)


class Bird:
    def __init__(self, character):
        self.character = character
        self.x = 130
        self.y = HEIGHT // 2
        self.velocity = 0
        self.radius = 22
        self.angle = 0
        self.flap_phase = 0
        self.float_time = 0

    @property
    def rect(self):
        return pygame.Rect(self.x - self.radius, self.y - self.radius, self.radius * 2, self.radius * 2)

    def flap(self):
        self.velocity = FLAP_STRENGTH
        self.flap_phase = 1.0

    def update(self):
        self.float_time += 0.08
        self.velocity += GRAVITY
        self.velocity *= 0.992
        self.y += self.velocity
        self.angle = max(-22, min(42, self.velocity * 4.2))
        if self.flap_phase > 0:
            self.flap_phase *= 0.86

    def draw(self, surface):
        body = pygame.Surface((70, 60), pygame.SRCALPHA)
        body_color = self.character["body"]
        wing_color = self.character["wing"]
        beak_color = self.character["beak"]

        pygame.draw.ellipse(body, body_color, (10, 12, 40, 34))
        pygame.draw.ellipse(body, wing_color, (22, 18, 20, 18))
        pygame.draw.polygon(body, beak_color, [(48, 26), (65, 20), (65, 32)])
        pygame.draw.circle(body, BLACK, (40, 22), 3)

        if self.character["type"] == "duck":
            pygame.draw.circle(body, body_color, (25, 10), 10)
        elif self.character["type"] == "bird":
            pygame.draw.circle(body, body_color, (25, 12), 9)
            pygame.draw.polygon(body, wing_color, [(18, 13), (25, 5), (32, 14)])
        else:
            pygame.draw.circle(body, body_color, (25, 11), 10)
            pygame.draw.ellipse(body, wing_color, (14, 35, 34, 10))

        rotated = pygame.transform.rotate(body, -self.angle)
        surface.blit(rotated, (self.x - rotated.get_width() // 2, int(self.y) - rotated.get_height() // 2))


class PipePair:
    def __init__(self, x, gap_y, gap_size, speed, color):
        self.x = x
        self.gap_y = gap_y
        self.gap_size = gap_size
        self.speed = speed
        self.color = color
        self.passed = False

    def update(self):
        self.x -= self.speed

    def offscreen(self):
        return self.x + PIPE_WIDTH < 0

    def rects(self):
        top_height = self.gap_y
        bottom_y = self.gap_y + self.gap_size
        bottom_height = HEIGHT - GROUND_HEIGHT - bottom_y
        top_rect = pygame.Rect(self.x, 0, PIPE_WIDTH, top_height)
        bottom_rect = pygame.Rect(self.x, bottom_y, PIPE_WIDTH, bottom_height)
        return top_rect, bottom_rect

    def collides(self, bird_rect):
        top_rect, bottom_rect = self.rects()
        return bird_rect.colliderect(top_rect) or bird_rect.colliderect(bottom_rect)

    def draw(self, surface):
        top_rect, bottom_rect = self.rects()
        pygame.draw.rect(surface, self.color, top_rect, border_radius=8)
        pygame.draw.rect(surface, self.color, bottom_rect, border_radius=8)
        pygame.draw.rect(surface, WHITE, top_rect, 2, border_radius=8)
        pygame.draw.rect(surface, WHITE, bottom_rect, 2, border_radius=8)
        pygame.draw.rect(surface, self.color, (self.x - 6, top_rect.height - 24, PIPE_WIDTH + 12, 24), border_radius=6)
        pygame.draw.rect(surface, self.color, (self.x - 6, bottom_rect.y, PIPE_WIDTH + 12, 24), border_radius=6)
        pygame.draw.rect(surface, WHITE, (self.x - 6, top_rect.height - 24, PIPE_WIDTH + 12, 24), 2, border_radius=6)
        pygame.draw.rect(surface, WHITE, (self.x - 6, bottom_rect.y, PIPE_WIDTH + 12, 24), 2, border_radius=6)


class Game:
    def __init__(self):
        self.state = "character_select"
        self.selected_character = 0
        self.character_buttons = []
        start_y = 220
        for i, char in enumerate(CHARACTERS):
            self.character_buttons.append(Button(WIDTH // 2 - 120, start_y + i * 90, 240, 58, char["name"]))
        self.start_button = Button(WIDTH // 2 - 90, 520, 180, 60, "Start Game")
        self.reset_game()
        self.music_channel = pygame.mixer.Channel(0)
        self.music_notes = []
        self.note_index = 0
        self.note_timer = 0
        self.last_music_level = 1

    def reset_game(self):
        self.bird = Bird(CHARACTERS[self.selected_character])
        self.pipes = []
        self.score = 0
        self.level = 1
        self.pipe_timer = 0
        self.game_over = False
        self.flash_timer = 0
        self.level_text_timer = 120

    def current_theme(self):
        idx = min(self.level - 1, len(LEVELS) - 1)
        return LEVELS[idx]

    def update_music_pack(self):
        theme = self.current_theme()
        self.music_notes = [make_tone(freq) for freq in theme["music"]]
        self.note_index = 0
        self.note_timer = 0
        self.last_music_level = self.level

    def play_music_step(self):
        if self.state != "playing":
            return
        if self.level != self.last_music_level or not self.music_notes:
            self.update_music_pack()
        if self.note_timer > 0:
            self.note_timer -= 1
            return
        if not self.music_channel.get_busy() and self.music_notes:
            self.music_channel.play(self.music_notes[self.note_index])
            self.note_index = (self.note_index + 1) % len(self.music_notes)
            self.note_timer = 8

    def pipe_speed(self):
        return 3 + min(self.level, 6)

    def current_gap(self):
        return max(140, PIPE_GAP - (self.level - 1) * 8)

    def spawn_delay(self):
        return max(72, 102 - (self.level - 1) * 5)

    def update_level(self):
        new_level = min(self.score // 10 + 1, len(LEVELS))
        if new_level != self.level:
            self.level = new_level
            self.level_text_timer = 120

    def spawn_pipe(self):
        gap_margin = 90
        gap_y = random.randint(gap_margin, HEIGHT - GROUND_HEIGHT - gap_margin - self.current_gap())
        pipe = PipePair(WIDTH + 20, gap_y, self.current_gap(), self.pipe_speed(), self.current_theme()["pipe"])
        self.pipes.append(pipe)

    def start_playing(self):
        self.reset_game()
        self.state = "playing"
        self.update_music_pack()

    def handle_flap(self):
        if self.state == "playing":
            self.bird.flap()

    def update(self):
        self.play_music_step()

        if self.state != "playing":
            if self.flash_timer > 0:
                self.flash_timer -= 1
            return

        self.bird.update()
        self.pipe_timer += 1
        if self.pipe_timer >= self.spawn_delay():
            self.spawn_pipe()
            self.pipe_timer = 0

        for pipe in self.pipes:
            pipe.update()
            if not pipe.passed and pipe.x + PIPE_WIDTH < self.bird.x:
                pipe.passed = True
                self.score += 1
                self.update_level()

        self.pipes = [p for p in self.pipes if not p.offscreen()]

        if self.bird.y - self.bird.radius <= 0 or self.bird.y + self.bird.radius >= HEIGHT - GROUND_HEIGHT:
            self.state = "game_over"
            self.game_over = True
            self.flash_timer = 18

        for pipe in self.pipes:
            if pipe.collides(self.bird.rect):
                self.state = "game_over"
                self.game_over = True
                self.flash_timer = 18
                break

        if self.level_text_timer > 0:
            self.level_text_timer -= 1

    def draw_gradient(self, top, bottom):
        for y in range(HEIGHT):
            ratio = y / HEIGHT
            r = int(top[0] * (1 - ratio) + bottom[0] * ratio)
            g = int(top[1] * (1 - ratio) + bottom[1] * ratio)
            b = int(top[2] * (1 - ratio) + bottom[2] * ratio)
            pygame.draw.line(screen, (r, g, b), (0, y), (WIDTH, y))

    def draw_background_details(self):
        theme = self.current_theme()
        name = theme["name"]

        if name == "Sunny Meadow":
            pygame.draw.circle(screen, (255, 240, 140), (440, 90), 42)
            for i in range(0, WIDTH, 120):
                pygame.draw.ellipse(screen, WHITE, (i, 90 + (i % 60), 90, 34))
        elif name == "Jungle Falls":
            for i in range(0, WIDTH, 85):
                pygame.draw.rect(screen, (50, 110, 60), (i, HEIGHT - GROUND_HEIGHT - 130, 18, 130))
                pygame.draw.circle(screen, (40, 150, 70), (i + 9, HEIGHT - GROUND_HEIGHT - 135), 34)
        elif name == "Desert Wind":
            pygame.draw.circle(screen, (255, 220, 120), (430, 95), 48)
            pygame.draw.ellipse(screen, (235, 195, 120), (20, HEIGHT - GROUND_HEIGHT - 70, 240, 55))
            pygame.draw.ellipse(screen, (225, 185, 110), (210, HEIGHT - GROUND_HEIGHT - 60, 260, 48))
        elif name == "Snow Peaks":
            for i in range(0, WIDTH, 100):
                pygame.draw.polygon(screen, (230, 240, 250), [(i, HEIGHT - GROUND_HEIGHT), (i + 40, HEIGHT - GROUND_HEIGHT - 120), (i + 80, HEIGHT - GROUND_HEIGHT)])
        elif name == "Sunset Volcano":
            pygame.draw.circle(screen, (255, 170, 90), (420, 120), 46)
            pygame.draw.polygon(screen, (95, 40, 35), [(20, HEIGHT - GROUND_HEIGHT), (140, HEIGHT - GROUND_HEIGHT - 120), (250, HEIGHT - GROUND_HEIGHT)])
            pygame.draw.polygon(screen, (75, 35, 30), [(250, HEIGHT - GROUND_HEIGHT), (360, HEIGHT - GROUND_HEIGHT - 160), (500, HEIGHT - GROUND_HEIGHT)])
        else:
            pygame.draw.circle(screen, (250, 250, 255), (435, 90), 42)
            for _ in range(30):
                random.seed(_)
                x = 20 + _ * 16
                y = 50 + (_ * 37) % 220
                pygame.draw.circle(screen, WHITE, (x, y), 2)

    def draw_ground(self):
        ground_color = self.current_theme()["ground"]
        pygame.draw.rect(screen, ground_color, (0, HEIGHT - GROUND_HEIGHT, WIDTH, GROUND_HEIGHT))
        pygame.draw.line(screen, WHITE, (0, HEIGHT - GROUND_HEIGHT), (WIDTH, HEIGHT - GROUND_HEIGHT), 3)
        for i in range(0, WIDTH, 28):
            pygame.draw.line(screen, (255, 255, 255, 40), (i, HEIGHT - GROUND_HEIGHT + 24), (i + 14, HEIGHT - 18), 2)

    def draw_hud(self):
        score_text = font.render(f"Score: {self.score}", True, WHITE)
        level_text = font.render(f"Level: {self.level}", True, WHITE)
        tip_text = small_font.render("Press SPACE to flap upward", True, WHITE)
        theme_text = small_font.render(self.current_theme()["name"], True, WHITE)
        screen.blit(score_text, (18, 16))
        screen.blit(level_text, (WIDTH - 140, 16))
        screen.blit(tip_text, (18, 50))
        screen.blit(theme_text, (WIDTH - theme_text.get_width() - 18, 50))
        if self.level_text_timer > 0:
            txt = menu_font.render(self.current_theme()["name"], True, WHITE)
            screen.blit(txt, (WIDTH // 2 - txt.get_width() // 2, 100))

    def draw_character_preview(self, idx, x, y):
        char = CHARACTERS[idx]
        preview = Bird(char)
        preview.x = x
        preview.y = y
        preview.angle = -8
        preview.draw(screen)

    def draw_character_select(self):
        self.draw_gradient((70, 130, 220), (200, 230, 255))
        title = large_font.render("SKY FLAP ADVENTURE", True, WHITE)
        subtitle = font.render("Choose your flyer", True, WHITE)
        info = small_font.render("Space moves upward. Levels change background and music.", True, WHITE)
        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 80))
        screen.blit(subtitle, (WIDTH // 2 - subtitle.get_width() // 2, 145))
        screen.blit(info, (WIDTH // 2 - info.get_width() // 2, 182))

        for i, button in enumerate(self.character_buttons):
            button.draw(screen, active=(i == self.selected_character))
            self.draw_character_preview(i, button.rect.x - 48, button.rect.centery)

        self.start_button.draw(screen, active=True)
        tip = small_font.render("Click a character, then click Start Game", True, WHITE)
        screen.blit(tip, (WIDTH // 2 - tip.get_width() // 2, 600))

    def draw_game_over(self):
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))
        screen.blit(overlay, (0, 0))
        title = large_font.render("GAME OVER", True, WHITE)
        info1 = font.render(f"Final Score: {self.score}", True, WHITE)
        info2 = font.render(f"Reached Level: {self.level}", True, WHITE)
        info3 = small_font.render("Press R to restart or Q to quit", True, WHITE)
        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, HEIGHT // 2 - 100))
        screen.blit(info1, (WIDTH // 2 - info1.get_width() // 2, HEIGHT // 2 - 28))
        screen.blit(info2, (WIDTH // 2 - info2.get_width() // 2, HEIGHT // 2 + 12))
        screen.blit(info3, (WIDTH // 2 - info3.get_width() // 2, HEIGHT // 2 + 62))

    def draw(self):
        if self.state == "character_select":
            self.draw_character_select()
            return

        theme = self.current_theme()
        self.draw_gradient(theme["sky_top"], theme["sky_bottom"])
        self.draw_background_details()
        for pipe in self.pipes:
            pipe.draw(screen)
        self.draw_ground()
        if not (self.state == "game_over" and self.flash_timer % 4 < 2):
            self.bird.draw(screen)
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

            if game.state == "character_select":
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    for i, button in enumerate(game.character_buttons):
                        if button.clicked(event.pos):
                            game.selected_character = i
                            game.bird = Bird(CHARACTERS[game.selected_character])
                    if game.start_button.clicked(event.pos):
                        game.start_playing()

            elif game.state == "playing":
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    game.handle_flap()
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    game.handle_flap()

            elif game.state == "game_over":
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        game.state = "character_select"
                        game.selected_character = 0
                        game.reset_game()
                    elif event.key == pygame.K_q:
                        pygame.quit()
                        sys.exit()

        game.update()
        game.draw()
        pygame.display.flip()


if __name__ == "__main__":
    main()
