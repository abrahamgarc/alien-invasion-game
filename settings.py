class Settings:
    """A class to store all settings for Alien Invasion."""

    def __init__(self):
        """Initialize the game's static settings."""
        # Screen settings
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (230, 230, 230)
        

        # Bullet settings
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (60, 60, 60)


        # Alien settings
        self.fleet_drop_speed = 10


        # How quicklythe game speeds up
        self.speedup_scale = 1.1
        # How quickly the alien point value increase.
        self.score_scale = 1.2

        self.difficulty_level = 'easy' #default
        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        """Initialize settings that change throughout the game."""
        if self.difficulty_level == 'easy':
            self.ship_limit = 3
            self.bullets_allowed = 10
            self.ship_speed = 1
            self.bullet_speed = 2
            self.alien_speed = 1
            self.alien_points = 10
        elif self.difficulty_level == 'medium':
            self.ship_limit = 2
            self.bullets_allowed = 5
            self.ship_speed = 2
            self.bullet_speed = 3
            self.alien_speed = 2
            self.alien_points = 20 
        elif self.difficulty_level == 'hard':
            self.ship_limit = 1
            self.bullets_allowed = 3
            self.ship_speed = 3
            self.bullet_speed = 4
            self.alien_speed = 3
            self.alien_points = 30

        # fleet_direction of 1 represents right; -1 represents left.
        self.fleet_direction = 1

    def increase_speed(self):
        """Increase speed settings and alien point values."""
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale

        self.alien_points = int(self.alien_points * self.score_scale)
    

    def set_difficulty(self, diff_setting):
        if diff_setting == 'easy':
            self.difficulty_level = 'easy'
        elif diff_setting == 'medium':
            self.difficulty_level = 'medium'
        elif diff_setting == 'hard':
            self.difficulty_level = 'hard'

        self.initialize_dynamic_settings()