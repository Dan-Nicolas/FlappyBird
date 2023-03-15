import pygame as pg


class Button:
    def __init__(self, y, text, color):
        self.rect = pg.Rect(200, y, 200, 100)
        self.text = text
        self.font = pg.font.Font(None, 50)
        self.color = color

    
    def checkForInput(self, position):
        """
            Used to see if mouse clicks on Button
        Args:
            position (_type_): mouse coordinates

        Returns:
            boolean: True if mouse clicks on Button False otherwise
        """
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
            return True
        return False

    def draw(self, surface):
        """
            Draws Button on screen
        """
        color = self.color
        pg.draw.rect(surface, color, self.rect)
        text_surface = self.font.render(self.text, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)
