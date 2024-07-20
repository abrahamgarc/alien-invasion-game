import pygame

class Background:
    """A class for the loading screen background."""

    def __init__(self, ai_game):
        """Initialize the screen loader."""

        # Screen settings
        self.screen = ai_game.screen
        self.screen_width = 1200
        self.screen_height = 800
        self.image = pygame.image.load('images/green_nebula.png').convert()
        self.background = pygame.transform.scale(self.image, (self.screen_width, self.screen_height))

    def loading_screen(self):
        self.screen.blit(self.background, (0, 0))


