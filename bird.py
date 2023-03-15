import pygame as pg
import os
#doubles the sizes and loads the images
FLAPPY_IMGS = [pg.transform.scale2x(pg.image.load(os.path.join("imgs", "bird1.png"))), 
               pg.transform.scale2x(pg.image.load(os.path.join("imgs", "bird2.png"))), 
               pg.transform.scale2x(pg.image.load(os.path.join("imgs", "bird3.png"))) 
              ]

class Bird:

    IMGS = FLAPPY_IMGS
    MAX_ROTATION = 25 # tilts the bird by 25 degrees up/down
    ROT_VEL = 20 # how much we will rotate on each frame
    ANIMATION_TIME = 5 # how long each animation will be 

    def __init__(self, x ,y) -> None:
        self.x = x
        self.y = y
        self.tilt = 0
        self.tick_count = 0
        self.vel = 0
        self.height = self.y
        self.img_count = 0
        self.img = self.IMGS[0]

    def jump(self):
        """
            Makes Flappy jump by -10.5 pixels
            Its a negative bc to go up on the y axis you need to subtract y
        """

        self.vel = -10.5
        # reset to 0 to know when we changed vel/directions for physics
        self.tick_count = 0
        self.height = self.y

    def move(self):
        """
            Flappy isn't actually moving only the pipes and base are moving 
            to give off the illusion it is flying in a supposedly never ending environment
        """
        self.tick_count += 1
        # how many pixels we move up/down this current frame, physics for the bird
        displacement = self.vel * self.tick_count + 1.5 * self.tick_count**2 

        # make sure Flappy isn't moving too far up or down
        if displacement >= 16:
            displacement = 16

        if displacement < 0:
            displacement -= 2 

        #self.y = self.y + displacement
        self.y += displacement
        # tilting the bird up/down appropriately 
        if displacement < 0 or self.y < self.height + 50:
            if self.tilt < self.MAX_ROTATION:
                 self.tilt = self.MAX_ROTATION
        else:
            # Rotate the bird 90 degrees
            if self.tilt > -90:
                self.tilt -= self.ROT_VEL

    def draw(self, window):
        """
            Draws Flappy on to the window as well as animates Flappy flying each frame

        """
        self.img_count += 1
        
        #Checking what img should be shown based on img_count
        if self.img_count < self.ANIMATION_TIME: # display first flappy img if img_count < 5
            self.img = self.IMGS[0]
        elif self.img_count < self.ANIMATION_TIME *2: # display second flappy img if img_count < 10
            self.img = self.IMGS[1]
        elif self.img_count < self.ANIMATION_TIME *3: # display third flappy img if img_count < 15
            self.img = self.IMGS[2]
        elif self.img_count < self.ANIMATION_TIME *4: # display second flappy img if img_count < 20
            self.img = self.IMGS[1]
        elif self.img_count == self.ANIMATION_TIME *4 + 1: # display first flappy img if img_count < 21 and then reset
            self.img = self.IMGS[0]
            self.img_count = 0

        # when bird is tilted almost 90 falling down, dont show it flapping its wings, display it nosediving.
        if self.tilt <= -80:
            self.img = self.IMGS[1]
            self.img_count = self.ANIMATION_TIME * 2
        
        # Rotate the images of the bird
        rotate_img = pg.transform.rotate(self.img, self.tilt)
        new_rect = rotate_img.get_rect(center = self.img.get_rect(topleft = (self.x, self.y)).center)
        window.blit(rotate_img,new_rect.topleft)

    # used for collision
    def get_mask(self):
        return pg.mask.from_surface(self.img)