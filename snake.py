import pygame
from point import Point
from color import Color
class Snake:
    def __init__(self, length):
        self.__length = length
        self.__points:list[Point] = []
        self.__direction = "right"
        self.offset = 20
        for i in range(self.__length):
            if i == 0:
                coord = Point.random_coord()
                self.__points.append(Point(*coord, Color.YELLOW))
            else:
                x_new = self.__points[i-1].get_x() - self.offset
                y_new = self.__points[i-1].get_y() 
                self.__points.append(Point(x_new, y_new, Color.DARK_VIOLET))

            
            

    def update_snake(self, direction):
        # print("head: ",self.get_head())
        match(direction):
            case "up":
                if self.__direction in ['left', 'right', 'up']:
                    self.set_direction('up')
                    
                    for i in range(self.__length-1, 0, -1):
                        old_x = self.__points[i-1].get_x()
                        old_y = self.__points[i-1].get_y()
                        # print(old_x, old_y)
                        self.__points[i].set_x(old_x)
                        self.__points[i].set_y(old_y)
                        # print(i, self.__points[i])
                    first_y = self.__points[0].get_y()
                    self.__points[0].set_y(first_y-self.offset)
                    # print(0, self.__points[0])
                    

            case "down":
                if self.__direction in ['left', 'right', 'down']:
                    self.set_direction('down')
                    
                    for i in range(self.__length-1, 0, -1):
                        old_x = self.__points[i-1].get_x()
                        old_y = self.__points[i-1].get_y()

                        self.__points[i].set_x(old_x)
                        self.__points[i].set_y(old_y)

                    first_y = self.__points[0].get_y()
                    self.__points[0].set_y(first_y+self.offset)

            case "left":
                if self.__direction in ['left', 'up', 'down']:
                    self.set_direction('left')
                    for i in range(self.__length-1, 0, -1):
                        old_x = self.__points[i-1].get_x()
                        old_y = self.__points[i-1].get_y()

                        self.__points[i].set_x(old_x)
                        self.__points[i].set_y(old_y)

                    first_y = self.__points[0].get_x()
                    self.__points[0].set_x(first_y-self.offset)

            case "right":
                if self.__direction in ['right', 'up', 'down']:
                    self.set_direction('right')
                    for i in range(self.__length-1, 0, -1):
                        old_x = self.__points[i-1].get_x()
                        old_y = self.__points[i-1].get_y()

                        self.__points[i].set_x(old_x)
                        self.__points[i].set_y(old_y)

                    first_y = self.__points[0].get_x()
                    self.__points[0].set_x(first_y+self.offset)

    def set_direction(self, direction: str):
        self.__direction = direction

    def get_direction(self) -> str:
        return self.__direction

    def increase_length(self):
        self.__length += 1
        # Lấy vị trí của phần tử cuối cùng hiện tại
        last_point = self.__points[-1]
        x_last, y_last = last_point.get_x(), last_point.get_y()
        
        # Tính vị trí của cell mới dựa trên hướng di chuyển hiện tại
        if self.__direction == "right":
            x_new = x_last - self.offset
            y_new = y_last
        elif self.__direction == "left":
            x_new = x_last + self.offset
            y_new = y_last
        elif self.__direction == "up":
            x_new = x_last
            y_new = y_last + self.offset
        elif self.__direction == "down":
            x_new = x_last
            y_new = y_last - self.offset
        
        # Thêm cell mới vào danh sách __points
        self.__points.append(Point(x_new, y_new, Color.DARK_VIOLET))
    
    def is_end(self) -> bool:
        head = self.get_head()
        if head.get_y() <= 0 or head.get_y() >= 600:
            return True
        if head.get_x() <= 0 or head.get_x() >= 800:
            return True
        for i in range(1, self.__length):
            if abs(head.get_x() - self.__points[i].get_x()) < self.offset and abs(head.get_y() - self.__points[i].get_y()) < self.offset:
                return True
        return False


    def get_head(self) -> Point:
        return self.__points[0]



    def draw_snack(self, screen: pygame.Surface):
        for point in self.__points:
            point.draw_point(screen, self.offset)
    
