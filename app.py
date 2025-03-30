import pygame
from PIL import Image, ImageFilter
from random import randint
from color import Color
from button import Button
from snake import Snake
from food import Food

class App():
    score = 0
    __FPS = 3
    def __init__(self, width, length):
        pygame.init()
        self.width = width
        self.length = length
        self.screen = pygame.display.set_mode((self.width, self.length))
        self.mode = 1  # Mode 1: Menu, 2: Game, 3: Help
        self.is_play_game = False
        self.is_help = False
        self.font_game_over = pygame.font.SysFont('Arial', 56)
        self.font_score = pygame.font.SysFont('Arial', 24)
        self.font_title = pygame.font.SysFont('Arial', 36)
        self.font_help = pygame.font.SysFont('Arial', 24)
        pygame.display.set_caption("Snake Game")
        # Biến cho hiển thị hướng dẫn từng dòng
        self.help_lines = [
            "Snake Game is a classic game!",
            "Control the snake with arrow keys (↑, ↓, ←, →).",
            "Eat food to make the snake longer and score points.",
            "Avoid colliding with yourself or the screen edges!",
            "Press SPACE to return to the menu."
        ]
        self.current_help_line = 0  # Dòng hiện tại đang hiển thị
        self.help_timer = 0  # Đếm thời gian để chuyển dòng
        self.help_interval = 300  # Khoảng thời gian giữa các dòng (1 giây)

    def draw_title(self):
        text_surface = self.font_title.render("Snake Game", True, Color.DARK_ORANGE)
        text_rect = text_surface.get_rect(center=(self.width // 2, 100))
        self.screen.blit(text_surface, text_rect)

    def draw_menu(self, start_btn: Button, help_btn: Button):
        start_btn.show()
        help_btn.show()
        start_btn.draw_button(self.screen)
        help_btn.draw_button(self.screen)
        self.draw_title()

    def draw_help(self):
        # Cập nhật thời gian để hiển thị dòng tiếp theo
        self.help_timer += 100  # Điều chỉnh theo FPS
        if self.help_timer >= self.help_interval and self.current_help_line < len(self.help_lines) - 1:
            self.current_help_line += 1
            self.help_timer = 0

        # Hiển thị các dòng đã được "mở khóa"
        y_offset = 200
        for i in range(self.current_help_line + 1):
            text_surface = self.font_help.render(self.help_lines[i], True, Color.VIOLET)
            text_rect = text_surface.get_rect(center=(self.width // 2, y_offset))
            self.screen.blit(text_surface, text_rect)
            y_offset += 40

    def draw_game(self, start_btn: Button, help_btn: Button, snk: Snake):
        help_btn.hide()
        start_btn.hide()
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

        text_surface = self.font_score.render(f"Score: {self.score}", True, (255, 255, 255))
        text_rect = text_surface.get_rect()
        padding = 10
        text_rect.topright = (self.width - padding, padding)
        self.screen.blit(text_surface, text_rect)

        if snk.is_end():
            blurred_surface = self.capture()
            self.screen.blit(blurred_surface, (0, 0))
            text_surface = self.font_game_over.render("Game Over", True, Color.RED)
            text_rect = text_surface.get_rect(center=(self.width // 2, self.length // 2))
            self.screen.blit(text_surface, text_rect)
            space_key_text = pygame.font.SysFont('Arial', 36)
            text_surface = space_key_text.render("Press SPACE to restart", True, Color.RED)
            text_rect = text_surface.get_rect(center=(self.width // 2, self.length // 2 + 100))
            self.screen.blit(text_surface, text_rect)
            self.is_play_game = False
        else:
            snk.draw_snack(self.screen)
            if len(Food.all_foods) == 0:
                Food.create_food()
            Food.draw_all_food(self.screen)
            if Food.check_collision(snk.get_head()):
                snk.increase_length()
                self.score += 1
            snk.update_snake(snk.get_direction())

    def capture(self) -> pygame.Surface:
        screen_size = self.screen.get_size()
        screenshot = pygame.Surface(screen_size)
        screenshot.blit(self.screen, (0, 0))
        raw_data = pygame.image.tostring(screenshot, "RGB")
        img = Image.frombytes("RGB", screen_size, raw_data)
        surface = pygame.image.fromstring(img.tobytes(), screen_size, "RGB")
        return surface

    def reset_game(self):
        self.score = 0
        self.is_play_game = True
        self.mode = 2
        Food.all_foods.clear()
        return Snake(5)

    def display(self):
        is_running = True
        button_width = 100
        button_height = 50
        center_x = self.width // 2 - button_width // 2
        center_y = self.length // 2 - button_height // 2

        start_btn = Button(center_x, center_y - 50, button_width, button_height, Color.LIGHT_ORANGE, "Start")
        help_btn = Button(center_x, center_y + 50, button_width, button_height, Color.LIGHT_ORANGE, "Help")
        snk = Snake(5)
        clock = pygame.time.Clock()

        while is_running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    is_running = False
                if event.type == pygame.KEYDOWN and self.is_play_game:
                    match event.key:
                        case pygame.K_UP:
                            snk.update_snake('up')
                        case pygame.K_DOWN:
                            snk.update_snake('down')
                        case pygame.K_LEFT:
                            snk.update_snake('left')
                        case pygame.K_RIGHT:
                            snk.update_snake('right')
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        if not self.is_play_game and self.mode == 2:  # Reset game
                            snk = self.reset_game()
                        elif self.is_help and self.mode == 3:  # Đóng Help
                            self.is_help = False
                            self.mode = 1
                            self.current_help_line = 0  # Reset dòng hiển thị
                            self.help_timer = 0  # Reset bộ đếm thời gian
                if start_btn.is_clicked(event) and not self.is_play_game and not self.is_help:
                    self.mode = 2
                if help_btn.is_clicked(event) and not self.is_play_game and not self.is_help:
                    self.mode = 3
                    self.is_help = True
                    self.current_help_line = 0  # Bắt đầu từ dòng đầu tiên
                    self.help_timer = 0

            self.screen.fill(Color.BLACK)
            match self.mode:
                case 1:
                    self.draw_menu(start_btn, help_btn)
                case 2:
                    self.is_play_game = True
                    Button.reset()
                    self.draw_game(start_btn, help_btn, snk)
                case 3:
                    self.is_help = True
                    Button.reset()
                    start_btn.hide()
                    help_btn.hide()
                    self.draw_help()
                case _:
                    print("Invalid mode!")

            pygame.display.flip()
            clock.tick(self.__FPS)

        pygame.quit()