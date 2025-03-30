import pygame

from color import Color

class Button():
    
    any_hovered = False
    all_buttons = []

    def __init__(self,x: int, y: int,  width: int, height: int, color: tuple, text: str):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.text = text
        self.is_hovered = False
        self.visible = True
        self.font = pygame.font.SysFont('arial', 24)
        Button.all_buttons.append(self)

    def draw_button(self, screen: pygame.Surface):
        if not self.visible:
            return
        # Kiểm tra sự kiện hover
        mouse_pos = pygame.mouse.get_pos()
        self.is_hovered = self.rect.collidepoint(mouse_pos) # Phương thức collidepoint(mouse_pos) tra về True nêu vị trí trỏ chuột trùng với vị trí nút.
      
        Button.any_hovered = any(button.is_hovered for button in Button.all_buttons)
        # Vẽ nút
        if Button.any_hovered :
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
        else:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

        if self.is_hovered:
            pygame.draw.rect(screen, self.color, self.rect, 2, border_radius=5)
        else:
            pygame.draw.rect(screen, self.color, self.rect, border_radius=5)



        # Vẽ text
        text_surface = self.font.render(self.text, True, self.color if self.is_hovered else  Color.WHITE)  # Tạo bề mặt chứa văn bản từ chuỗi self.text, với màu trắng và chống răng cưa
        text_rect = text_surface.get_rect(center=self.rect.center)  # Tạo hình chữ nhật bao quanh văn bản và căn giữa nó theo tâm của self.rect
        screen.blit(text_surface, text_rect)  # Vẽ bề mặt văn bản lên màn hình tại vị trí được xác định bởi text_rect

    def is_clicked(self, event: pygame.event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(pygame.mouse.get_pos()): # Kiểm tra sự kiện click chuột
                return True
        return False

    def hide(self):
        Button.any_hovered = False
        self.visible = False
    
    def show(self):
        self.visible = True

    @classmethod
    def reset(cls):
        cls.any_hovered = False

    
if __name__ == "__main__":
    pygame.init()

    running = True
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Button Test")

    while running:
        # Kiểm tra
        
        button = Button(350, 275, 100, 50, Color.GREEN, "Start")
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if button.is_clicked(event):
                print("Button clicked!")

        screen.fill(Color.BLACK)
        button.draw_button(screen)
        pygame.display.flip()

    pygame.quit()