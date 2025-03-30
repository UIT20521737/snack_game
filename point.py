import pygame
from color import Color
from random import randint
class Point:
    def __init__(self, x, y, color = Color.WHITE):
        self.__x = x
        self.__y = y
        self.__color = color
    def __str__(self):
        return f'{self.__x} - {self.__y}'
    
    def draw_point(self, screen: pygame.Surface, width: int = 10):
        point_image = pygame.Rect(self.__x, self.__y, width, width)
        pygame.draw.rect(screen, self.__color, point_image)

    
    def get_x(self):
        return self.__x
    
    def get_y(self):
        return self.__y
    
    def set_x(self, x):
        self.__x = x

    def set_y(self, y):
        self.__y = y
    @classmethod
    def random_coord(cls):
        return (randint(100, 200), randint(100, 200))
