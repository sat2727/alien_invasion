import json

class GameStats():
    """Track stats for Alien Invasion"""
    def __init__(self, ai_settings):
        self.ai_settings = ai_settings
        self.reset_stats()
        self.game_active = False
        
        self.get_high_score()

    def reset_stats(self):
        """Initialize stats that can change during the game"""
        self.ships_left = self.ai_settings.ship_limit
        self.score = 0
        self.level = 1

    def get_high_score(self):
        try:
            with open('high_score.json') as file:
                self.high_score = json.load(file)

        except FileNotFoundError:
            self.high_score = 0