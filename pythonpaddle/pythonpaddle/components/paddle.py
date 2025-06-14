"""Paddle component for the pythonpaddle game."""
import pygame
from pythonpaddle.utils.config import CONFIG
from pythonpaddle.core.physics import BallPhysics


class Paddle:
    """Paddle class for player control."""
    
    def __init__(self, x, is_ai=False):
        """
        Initialize a paddle.
        
        Args:
            x: X-position of the paddle
            is_ai: Whether this paddle is AI-controlled
        """
        self.width = CONFIG.PADDLE_WIDTH
        self.height = CONFIG.PADDLE_HEIGHT
        self.position_x = x
        self.position_y = CONFIG.WINDOW_HEIGHT // 2
        self.velocity = 0
        self.speed = CONFIG.PADDLE_SPEED
        self.is_ai = is_ai
        
        self.rect = pygame.Rect(
            self.position_x - self.width // 2,
            self.position_y - self.height // 2,
            self.width,
            self.height
        )
        
        # AI properties for more natural movement
        self.ai_prediction_steps = 30
        self.ai_reaction_time = 0.5
        self.ai_error_margin = 20
        self.ai_think_timer = 0
        self.ai_target_y = self.position_y
    
    def move_up(self):
        """Set velocity to move paddle up."""
        self.velocity = -self.speed
    
    def move_down(self):
        """Set velocity to move paddle down."""
        self.velocity = self.speed
    
    def stop(self):
        """Stop paddle movement."""
        self.velocity = 0
    
    def update_ai(self, dt, ball):
        """
        Update AI-controlled paddle.
        
        Args:
            dt: Delta time for frame-rate independent movement
            ball: Ball object to track
        """
        # Only update AI decision after reaction time has passed
        self.ai_think_timer += dt
        if self.ai_think_timer >= self.ai_reaction_time:
            self.ai_think_timer = 0
            
            # If ball is moving toward AI
            if (self.position_x < CONFIG.WINDOW_WIDTH // 2 and ball.velocity_x < 0) or \
               (self.position_x > CONFIG.WINDOW_WIDTH // 2 and ball.velocity_x > 0):
                
                # Predict where the ball will be
                predicted_y = BallPhysics.predict_ball_position(
                    ball, self.ai_prediction_steps, CONFIG.WINDOW_HEIGHT)
                
                # Add some intentional error to make AI beatable
                error = pygame.math.Vector2(0, self.ai_error_margin).rotate(
                    pygame.time.get_ticks() % 360).y
                
                self.ai_target_y = predicted_y + error
            else:
                # Move toward center when ball is moving away
                self.ai_target_y = CONFIG.WINDOW_HEIGHT // 2
        
        # Move toward the target position
        if self.position_y < self.ai_target_y - 5:
            self.velocity = self.speed * 0.8
        elif self.position_y > self.ai_target_y + 5:
            self.velocity = -self.speed * 0.8
        else:
            self.velocity = 0
    
    def update(self, dt, ball=None):
        """
        Update paddle position based on velocity or AI logic.
        
        Args:
            dt: Delta time for frame-rate independent movement
            ball: Ball object for AI tracking (optional)
        """
        if self.is_ai and ball:
            self.update_ai(dt, ball)
        
        # Update position with velocity
        self.position_y += self.velocity * dt * 60
        
        # Constrain to screen bounds
        if self.position_y - self.height // 2 < 0:
            self.position_y = self.height // 2
            self.velocity = 0
        elif self.position_y + self.height // 2 > CONFIG.WINDOW_HEIGHT:
            self.position_y = CONFIG.WINDOW_HEIGHT - self.height // 2
            self.velocity = 0
        
        # Update the rect for rendering and collision detection
        self.rect.y = self.position_y - self.height // 2
    
    def render(self, screen):
        """
        Render the paddle on the screen.
        
        Args:
            screen: pygame surface to render on
        """
        # Draw the paddle
        pygame.draw.rect(screen, CONFIG.WHITE, self.rect)
        
        # Add a highlight effect for 3D appearance
        highlight_rect = pygame.Rect(
            self.rect.left, 
            self.rect.top,
            self.width // 3,
            self.height
        )
        pygame.draw.rect(screen, (220, 220, 220), highlight_rect)