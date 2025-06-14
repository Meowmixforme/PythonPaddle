"""Configuration settings for the pythonpaddle game."""
from dataclasses import dataclass


@dataclass
class GameConfiguration:
    """Game configuration parameters."""
    # Window settings
    WINDOW_WIDTH: int = 800
    WINDOW_HEIGHT: int = 600
    WINDOW_TITLE: str = "PythonPaddle"
    FPS: int = 60
    
    # Colors
    BLACK: tuple = (0, 0, 0)
    WHITE: tuple = (255, 255, 255)
    YELLOW: tuple = (255, 255, 0)
    
    # Game elements
    PADDLE_WIDTH: int = 10
    PADDLE_HEIGHT: int = 100
    PADDLE_SPEED: float = 7.0
    PADDLE_MARGIN: int = 20
    
    # Ball settings
    BALL_SIZE: int = 15
    BALL_SPEED_X: float = 5.0
    BALL_SPEED_Y: float = 5.0
    BALL_SPEED_INCREASE: float = 0.2
    MAX_BALL_SPEED: float = 15.0
    
    # Game settings
    WINNING_SCORE: int = 10
    
    # Sound settings
    SOUND_ENABLED: bool = True
    SOUND_VOLUME: float = 0.7


# Global instance
CONFIG = GameConfiguration()