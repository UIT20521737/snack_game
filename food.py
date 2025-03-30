
from point import *
class Food(Point):
    all_foods:list['Food'] = []
    food_created = False
    def __init__(self):
        x = randint(1, 799)
        y = randint(1, 599)
        color=Color.get_random_color()
        super().__init__(x, y, color)
    def __str__(self):
        return super().__str__()
    
    def draw_food(self, screen):
        super().draw_point(screen)

    def __repr__(self):
        return f"{self.__str__()}"

    @classmethod
    def create_food(cls):
        food_inc = Food()
        Food.all_foods.append(food_inc)
        Food.food_created = True

    @classmethod
    def draw_all_food(cls, screen):
        for food in Food.all_foods:
            food.draw_food(screen)
    @classmethod
    def check_collision(cls, head:Point) -> bool:
        offset = 20
        for food in cls.all_foods:
            if (abs(head.get_x() - food.get_x()) < offset) and (abs(head.get_y() - food.get_y()) < offset):
                cls.all_foods = [item for item in cls.all_foods if item != food]
                return True
        return False
    
if __name__ == "__main__":
    a = Food()
    print(f"{a}")
    print(f"{a = }k")
