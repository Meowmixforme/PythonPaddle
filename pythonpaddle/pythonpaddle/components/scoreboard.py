"""Scoreboard component for tracking and displaying the score."""
import pygame
from pythonpaddle.utils.config import CONFIG


class Scoreboard:
    """Scoreboard for tracking and displaying game score."""
    
    def __init__(self):
        """Initialize the scoreboard with default scores."""
        self.left_score = 0
        self.right_score = 0
        self.font = pygame.font.Font(None, 74)
    
    def update_score(self, result):
        """
        Update the score based on the result.
        
        Args:
            result: 1 if right player scored, -1 if left player scored
        """
        if result == 1:
            self.right_score += 1
        elif result == -1:
            self.left_score += 1
    
    def check_winner(self):
        """
        Check if there's a winner.
        
        Returns:
            str: 'left' or 'right' if there's a winner, None otherwise
        """
        if self.left_score >= CONFIG.WINNING_SCORE:
            return 'left'
        elif self.right_score >= CONFIG.WINNING_SCORE:
            return 'right'
        return None
    
    def reset(self):
        """Reset the scores to zero."""
        self.left_score = 0
        self.right_score = 0
    
    def render(self, screen):
        """
        Render the scoreboard on the screen.
        
        Args:
            screen: pygame surface to render on
        """
        # Render left score
        left_text = self.font.render(str(self.left_score), True, CONFIG.WHITE)
        left_pos = (CONFIG.WINDOW_WIDTH // 4, 50)
        screen.blit(left_text, left_text.get_rect(center=left_pos))
        
        # Render right score
        right_text = self.font.render(str(self.right_score), True, CONFIG.WHITE)
        right_pos = (3 * CONFIG.WINDOW_WIDTH // 4, 50)
        screen.blit(right_text, right_text.get_rect(center=right_pos))