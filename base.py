import pygame as pg
import os


BASE_IMG = pg.transform.scale2x(pg.image.load(os.path.join("imgs", "base.png")))

class Base:
    VEL = 5
    WIDTH = BASE_IMG.get_width()
    IMG = BASE_IMG

    def __init__(self,y) -> None:
        self.y = y 
        self.x1 = 0
        self.x2 = self.WIDTH

    def move(self):
        """
            Moves the ground
        """
        self.x1 -= self.VEL
        self.x2 -= self.VEL
        """
            There are 2 BASE IMGS we are using
            x1 and x2 are their respective x's 
            both imgs are "rotating" around the screen 
            giving the illusion that the ground is also moving
        """
        if self.x1 + self.WIDTH < 0:
            self.x1 = self.WIDTH + self.x2
        
        if self.x2 + self.WIDTH < 0:
            self.x2 = self.WIDTH + self.x1

    def draw(self, window):
        """
            Draws the base to the screen
        """
        window.blit(self.IMG, (self.x1, self.y))
        window.blit(self.IMG, (self.x2, self.y))