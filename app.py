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
        pygame.init() # Khởi tạo pygame
        self.width = width # Chỉnh chiều rộng cửa sổ
        self.length = length # Chỉnh chiều dài cửa sổ
        self.screen = pygame.display.set_mode((self.width,self.length)) # Chỉnh kích thước của sổ
        self.mode = 1 # Chỉnh màn hình 1
        self.is_play_game = False
        self.font_help = ""
        self.font_game_over = ""
        self.font_score = pygame.font.SysFont('Arial', 24)
        self.font_title = pygame.font.SysFont('Arial', 36)
        self.is_help = False
        pygame.display.set_caption("Snake Game") # Khởi tạo caption

    def draw_title(self):
        text_surface = self.font_title.render("Snake Game", True, Color.DARK_ORANGE)
        text_rect = text_surface.get_rect(center=(self.width // 2, 100))
        self.screen.blit(text_surface, text_rect)

    def draw_menu(self, start_btn: Button, help_btn: Button):
        start_btn.draw_button(self.screen)
        help_btn.draw_button(self.screen)
        self.draw_title()
    
    def draw_help(self):
        text = "Snake Game là một trò chơi kinh điển! Điều khiển con rắn của bạn bằng các phím mũi tên (↑, ↓, ←, →) để di chuyển và ăn thức ăn, giúp rắn phát triển dài hơn và đạt điểm cao. Hãy cẩn thận tránh va chạm với chính mình hoặc các cạnh màn hình!"
        text_width = 400
        text_height = 300
        self.font_help = ""
        text_surface = self.font.render('Arial', True, Color.VIOLET)

    def draw_game(self, start_btn: Button, help_btn: Button, snk: Snake):
        help_btn.hide()
        start_btn.hide()

    
        

        # Giả sử self.font đã được khởi tạo với kích thước text_size, ví dụ:
        # self.font = pygame.font.Font(None, text_size)
        text_surface = self.font_score.render(f"Score: {self.score}", True, (255, 255, 255))  # Màu trắng, có thể thay đổi
        text_rect = text_surface.get_rect()

        # Đặt tọa độ góc phải trên với padding
        padding = 10
        text_rect.topright = (800 - padding, padding)  # 800 là chiều rộng cửa sổ, top-right cách biên 10 pixel

        # Vẽ văn bản lên màn hình
        self.screen.blit(text_surface, text_rect)

        # Kiểm tra xem trò chơi có kết thúc không
        if snk.is_end():
            snk.draw_snack(self.screen)
            self.is_play_game = False
        else:
            # Vẽ rắn và thức ăn
            snk.draw_snack(self.screen)

            # Nếu không có thức ăn nào trên màn hình, tạo một thức ăn mới
            if len(Food.all_foods) == 0:
                Food.create_food()
            Food.draw_all_food(self.screen)

            # Kiểm tra va chạm trước khi cập nhật vị trí rắn
            if Food.check_collision(snk.get_head()):
                # Nếu rắn ăn thức ăn, tăng độ dài và điểm số
                snk.increase_length()  # Đã sửa increase_length trước đó để thêm cell mới
                self.score += 1
                # Không cần gọi Food.create_food() ở đây vì sẽ được xử lý ở bước kiểm tra len(Food.all_foods) == 0

            # Cập nhật vị trí rắn sau khi kiểm tra va chạm
            snk.update_snake(snk.get_direction())
                    

                    
    def capture_and_blur(self) -> pygame.Surface:
        """Chụp màn hình, làm mờ và trả về Pygame Surface"""
        screen_size = self.screen.get_size()

        # Chụp màn hình
        screenshot = pygame.Surface(screen_size)
        screenshot.blit(self.screen, (0, 0))

        # Lấy dữ liệu pixel từ Pygame Surface
        raw_data = pygame.image.tostring(screenshot, "RGB")

        # Chuyển sang PIL Image
        img = Image.frombytes("RGB", screen_size, raw_data)

        # Làm mờ ảnh
        img = img.filter(ImageFilter.GaussianBlur(5))

        # Chuyển lại về Pygame Surface
        blurred_surface = pygame.image.fromstring(img.tobytes(), screen_size, "RGB")

        return blurred_surface



    def display(self):
        is_running = True # Khai báo biến trạng thái chạy
        # Tính tọa độ giữa màn hình
        button_width = 100  # Giả sử chiều rộng nút
        button_height = 50  # Giả sử chiều cao nút
        center_x = self.width // 2 - button_width // 2   # Tọa độ x giữa màn hình
        center_y = self.length // 2 - button_height // 2 # Tọa độ y giữa màn hình
        

        start_btn = Button(center_x, center_y - 50, button_width, button_height, Color.LIGHT_ORANGE, "Start")
        help_btn = Button(center_x, center_y + 50, button_width, button_height, Color.LIGHT_ORANGE, "Help")

        snk = Snake(5)
        clock = pygame.time.Clock()
        
        
        while is_running: # Vòng lặp trò chơi
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    is_running = False
                if event.type == pygame.KEYDOWN and self.is_play_game:
                    match(event.key):
                        case pygame.K_UP:
                            snk.update_snake('up')
                        case pygame.K_DOWN:
                            snk.update_snake('down')
                        case pygame.K_LEFT:
                            snk.update_snake('left')   
                        case pygame.K_RIGHT:
                            snk.update_snake('right')   
                    
                if start_btn.is_clicked(event):
                    if not self.is_play_game and not self.is_help:
                        self.mode = 2
                if help_btn.is_clicked(event):
                    if not self.is_play_game and not self.is_play_game:
                        self.mode = 3

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
                case _:
                    print("Invalid mode!")

            pygame.display.flip()
            clock.tick(self.__FPS)

        pygame.quit()

