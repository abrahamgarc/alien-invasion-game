import pygame.font
from firebase_config import get_db_reference
import firebase_admin
from firebase_admin import firestore



class Leaderboard:
    """A class to represent the leaderboard."""

    def __init__(self, ai_game):
        """Initialize button attributes."""
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()

        # Font settings for the leaderboard.
        #self.screen.fill((0, 0, 0))
        self.background = (0,0,0)
        self.text_color = (255, 255, 255)

        self.scores_ref = get_db_reference().collection("leaderboard")

        # Sort scores by score in descending order
        self.scores = []
        query = self.scores_ref.order_by("score", direction=firestore.Query.DESCENDING).limit(10)
        results = query.stream()
        for doc in results:
            self.scores.append(doc.to_dict())


        self._prep_text()


    def _prep_text(self):
        """Turn msg into a rendered image."""
        self.font = pygame.font.Font('joystix.otf', 55)
        self.msg = 'HIGH SCORES'
        self.msg_image = self.font.render(self.msg, True, self.text_color, self.background)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect = (350, 120)

        self.font = pygame.font.Font('joystix.otf', 30)
        self.row1 = 'RANK'
        self.row1_image = self.font.render(self.row1, True, self.text_color, self.background)
        self.row1_image_rect = self.row1_image.get_rect()
        self.row1_image_rect = (300,250)

        self.row2 = 'NAME'
        self.row2_image = self.font.render(self.row2, True, self.text_color, self.background)
        self.row2_image_rect = self.row1_image.get_rect()
        self.row2_image_rect = (550, 250)

        self.row3 = 'SCORE'
        self.row3_image = self.font.render(self.row3, True, self.text_color, self.background)
        self.row3_image_rect = self.row3_image.get_rect()
        self.row3_image_rect = (800, 250)

        self.font = pygame.font.Font('joystix.otf', 25)
        self.rank_images = []
        self.name_images = []
        self.score_images = []

        for rank, entry in enumerate(self.scores[:10], start=1):
            rank_image = self.font.render(str(rank), True, self.text_color, self.background)
            name_image = self.font.render(entry['name'], True, self.text_color, self.background)
            score_image = self.font.render(f"{entry['score']:,}", True, self.text_color, self.background)

            self.rank_images.append(rank_image)
            self.name_images.append(name_image)
            self.score_images.append(score_image)


    def draw_text(self):
        # Draw blank button and then draw message.
        self.screen.blit(self.msg_image, self.msg_image_rect)
        self.screen.blit(self.row1_image, self.row1_image_rect)
        self.screen.blit(self.row2_image, self.row2_image_rect)
        self.screen.blit(self.row3_image, self.row3_image_rect)

        # Draw scores
        for i in range(len(self.rank_images)):
            rank_rect = self.rank_images[i].get_rect()
            rank_rect.topleft = (300, 300 + i * 40)
            self.screen.blit(self.rank_images[i], rank_rect)

            name_rect = self.name_images[i].get_rect()
            name_rect.topleft = (550, 300 + i * 40)
            self.screen.blit(self.name_images[i], name_rect)

            score_rect = self.score_images[i].get_rect()
            score_rect.topleft = (800, 300 + i * 40)
            self.screen.blit(self.score_images[i], score_rect)






