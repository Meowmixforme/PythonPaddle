"""Game state for the pythonpaddle game."""
import pygame
from pythonpaddle.utils.config import CONFIG
from pythonpaddle.components.ball import Ball
from pythonpaddle.components.paddle import Paddle
from pythonpaddle.components.scoreboard import Scoreboard
from pythonpaddle.utils.sound_manager import SoundManager


class GameState:
    """Game state handling actual gameplay."""
    
    def __init__(self, engine, is_ai_opponent=True):
        """
        Initialize the game state.
        
        Args:
            engine: Reference to the main game engine
            is_ai_opponent: Whether the right paddle is AI-controlled
        """
        self.engine = engine
        self.is_ai_opponent = is_ai_opponent
        self.sound_manager = SoundManager()
        self.sound_manager.load_sounds()
        self.reset()
    
    def reset(self):
        """Reset the game state to initial conditions."""
        # Create game objects
        self.ball = Ball()
        
        # Create paddles
        left_paddle_x = CONFIG.PADDLE_MARGIN
        right_paddle_x = CONFIG.WINDOW_WIDTH - CONFIG.PADDLE_MARGIN
        
        self.left_paddle = Paddle(left_paddle_x)
        self.right_paddle = Paddle(right_paddle_x, is_ai=self.is_ai_opponent)
        
        self.paddles = [self.left_paddle, self.right_paddle]
        
        # Create scoreboard
        self.scoreboard = Scoreboard()
        
        # Game state tracking
        self.paused = False
        self.game_over = False
        self.winner = None
    
    def enter(self):
        """Called when entering this state."""
        self.reset()
    
    def exit(self):
        """Called when exiting this state."""
        pass
    
    def handle_event(self, event):
        """
        Handle input events.
        
        Args:
            event: pygame event to process
        """
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.engine.state_machine.change("menu")
            elif event.key == pygame.K_p:
                self.paused = not self.paused
            elif event.key == pygame.K_r:
                self.reset()
        
        # Player control handling
        keys = pygame.key.get_pressed()
        
        # Left paddle controls
        if keys[pygame.K_w]:
            self.left_paddle.move_up()
        elif keys[pygame.K_s]:
            self.left_paddle.move_down()
        else:
            self.left_paddle.stop()
        
        # Right paddle controls (only if not AI)
        if not self.is_ai_opponent:
            if keys[pygame.K_UP]:
                self.right_paddle.move_up()
            elif keys[pygame.K_DOWN]:
                self.right_paddle.move_down()
            else:
                self.right_paddle.stop()
    
    def update(self, dt):
        """
        Update game state.
        
        Args:
            dt: Delta time for frame-rate independent movement
        """
        if self.paused or self.game_over:
            return
        
        # Update paddles
        self.left_paddle.update(dt)
        self.right_paddle.update(dt, self.ball if self.is_ai_opponent else None)
        
        # Update ball and check for scoring
        score_result = self.ball.update(dt, self.paddles)
        if score_result != 0:
            self.scoreboard.update_score(score_result)
            
            # Check for winner
            winner = self.scoreboard.check_winner()
            if winner:
                self.game_over = True
                self.winner = winner
    
    def render(self, screen):
        """
        Render the game state.
        
        Args:
            screen: pygame surface to render on
        """
        # Draw the center line
        pygame.draw.aaline(
            screen,
            CONFIG.WHITE,
            (CONFIG.WINDOW_WIDTH // 2, 0),
            (CONFIG.WINDOW_WIDTH // 2, CONFIG.WINDOW_HEIGHT)
        )
        
        # Render game objects
        self.ball.render(screen)
        self.left_paddle.render(screen)
        self.right_paddle.render(screen)
        self.scoreboard.render(screen)
        
        # Display pause message if paused
        if self.paused:
            font = pygame.font.Font(None, 74)
            text = font.render("PAUSED", True, CONFIG.YELLOW)
            text_rect = text.get_rect(center=(CONFIG.WINDOW_WIDTH // 2, CONFIG.WINDOW_HEIGHT // 2))
            screen.blit(text, text_rect)
            
            small_font = pygame.font.Font(None, 36)
            hint_text = small_font.render("Press P to resume, ESC for menu", True, CONFIG.WHITE)
            hint_rect = hint_text.get_rect(center=(CONFIG.WINDOW_WIDTH // 2, CONFIG.WINDOW_HEIGHT // 2 + 50))
            screen.blit(hint_text, hint_rect)
        
        # Display game over message
        if self.game_over:
            font = pygame.font.Font(None, 74)
            winner_text = "Player 1 Wins!" if self.winner == "left" else "Player 2 Wins!"
            if self.winner == "right" and self.is_ai_opponent:
                winner_text = "AI Wins!"
            
            text = font.render(winner_text, True, CONFIG.YELLOW)
            text_rect = text.get_rect(center=(CONFIG.WINDOW_WIDTH // 2, CONFIG.WINDOW_HEIGHT // 2))
            screen.blit(text, text_rect)
            
            small_font = pygame.font.Font(None, 36)
            hint_text = small_font.render("Press R to restart, ESC for menu", True, CONFIG.WHITE)
            hint_rect = hint_text.get_rect(center=(CONFIG.WINDOW_WIDTH // 2, CONFIG.WINDOW_HEIGHT // 2 + 50))
            screen.blit(hint_text, hint_rect)