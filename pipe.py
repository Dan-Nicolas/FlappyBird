import pygame as pg
import os
import random

PIPE_IMG = pg.transform.scale2x(pg.image.load(os.path.join("imgs", "pipe.png")))

class Pipe():
    # how fast the the pipes are moving
    VEL = 5
    def __init__(self, x) -> None:
        self.x = x
        self.height = 0
        self.gap = 200
        self.top = 0
        self.bottom = 0
        self.PIPE_TOP = pg.transform.flip(PIPE_IMG, False, True)
        self.PIPE_BOTTOM = PIPE_IMG
        self.passed = False
        self.set_height()

    def set_height(self):
        """
            Randomly sets the length of each set of pipes with an appropriate sized gap
            for Flappy to fly through
        """
        self.height = random.randrange(50,450)
        self.top = self.height - self.PIPE_TOP.get_height()
        self.bottom = self.height + self.gap

    def move(self):
        """
            Moves pipes by 5 pixels each frame
        """
        self.x -= self.VEL

    def draw(self,window):
        """
            Draws the pipes onto the window

        """
        window.blit(self.PIPE_TOP, (self.x, self.top))
        window.blit(self.PIPE_BOTTOM, (self.x, self.bottom))

    
    def collide(self, bird):
        """
            Collision detection for the game

        Returns:
            boolean: True if a collision has been made False otherwise
        """
        bird_mask = bird.get_mask()
        top_mask = pg.mask.from_surface(self.PIPE_TOP)
        bottom_mask = pg.mask.from_surface(self.PIPE_BOTTOM)

        # cant have decimals so round bird.y
        top_offset = (self.x - bird.x, self.top - round(bird.y))
        bottom_offset = (self.x - bird.x , self.bottom - round(bird.y))
        
        # Tells us the point of collision between the bird mask and the bottom pipe
        # Using how far the bird is from the bottom pipe (bottom_offset)
        b_point = bird_mask.overlap(bottom_mask, bottom_offset)
        t_point = bird_mask.overlap(top_mask, top_offset)

        if t_point or b_point: # if either is true then a collision has been made
            return True
        return False