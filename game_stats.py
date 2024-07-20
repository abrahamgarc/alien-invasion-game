from pathlib import Path
from firebase_config import get_db_reference
import firebase_admin
from firebase_admin import firestore

class GameStats:
    """Track statistics for Alien Invasion."""


    def __init__(self, ai_game):
        """Initialize statistics."""
        self.settings = ai_game.settings
        self.screen = ai_game.screen
        self.reset_stats()

        # High score should never be reset.
        self.high_score = 0

            #Leaderboard Rankings
        # Initialize scores from Firebase
        self.scores_ref = get_db_reference().collection("leaderboard")


    def reset_stats(self):
        """Initialize statistics that can change during the game."""
        self.ships_left = self.settings.ship_limit
        self.score = 0
        self.level = 1

     
    def upload_packet(self, username):
        """Upload the highscore and username to json file for leaderboard rankings."""
        doc_ref = self.scores_ref.document(username)
        doc = doc_ref.get()
        if doc.exists:
            data = doc.to_dict()
            if data['score'] == self.score:
                # If the existing score is greater than or equal to the current score, do not update
                return
            else:
                # Update with the new score if it's higher
                doc_ref.update({
                    "score": self.score
                })
        else:
            # Add the new score if the document does not exist
            doc_ref.set({
                "name": username,
                "score": self.score
            })







 



    