from random import choice
class Color:
    # Khai báo các hằng số màu sắc như class variables
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)
    ORANGE = (255, 165, 0)  # Màu cam
    DARK_ORANGE = (255, 140, 0)  # Màu cam đậm (cho hover)
    LIGHT_ORANGE = (255, 190, 0)  # Màu cam nhạt (cho nút khác)
    VIOLET = (148, 0, 211)  # Màu tím (violet)
    DARK_VIOLET = (128, 0, 191)  # Màu tím đậm (cho hover)
    LIGHT_VIOLET = (186, 85, 211)  # Màu tím nhạt (cho nút khác)
    YELLOW = (255,255,0)
    @classmethod
    def get_random_color(cls) -> tuple:
        all_values = vars(cls).values()
        color_list = [
            value for value in all_values
            if isinstance(value, tuple) and len(value) in (3, 4) and all(isinstance(x, int) for x in value) and value not in [(0,0,0), (255,255,255)]
        ]
        return choice(color_list)

    
