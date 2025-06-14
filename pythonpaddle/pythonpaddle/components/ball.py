"""Ball component for the pythonpaddle game."""
import os
import pygame
from pythonpaddle.utils.config import CONFIG
from pythonpaddle.core.physics import BallPhysics, CollisionDetector


class Ball:
    """Ball class representing the game ball."""
    
    def __init__(self):
        """Initialize the ball with default values."""
        self.size = CONFIG.BALL_SIZE
        self.reset()
        
        # For special effects - reduce trail complexity
        self.trail = []
        self.max_trail_length = 3  # Reduced from 5 to reduce complexity
        self.trail_opacity = 120
        
        # Sound setup with safer loading
        self.has_sounds = False
        
        if CONFIG.SOUND_ENABLED:
            try:
                # Get the correct sound directory path
                base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
                sound_dir = os.path.join(base_dir, "assets", "sounds")
                
                paddle_hit_path = os.path.join(sound_dir, "paddle_hit.wav")
                wall_hit_path = os.path.join(sound_dir, "wall_hit.wav")
                score_path = os.path.join(sound_dir, "score.wav")
                
                # Only try to load if the files exist
                if os.path.exists(paddle_hit_path):
                    self.paddle_sound = pygame.mixer.Sound(paddle_hit_path)
                    self.paddle_sound.set_volume(0.5)
                    
                if os.path.exists(wall_hit_path):
                    self.wall_sound = pygame.mixer.Sound(wall_hit_path)
                    self.wall_sound.set_volume(0.4)
                    
                if os.path.exists(score_path):
                    self.score_sound = pygame.mixer.Sound(score_path)
                    self.score_sound.set_volume(0.6)
                    
                self.has_sounds = True
                
            except Exception as e:
                print(f"Sound loading error (continuing without sound): {e}")
                self.has_sounds = False
    
    def reset(self):
        """Reset ball to initial position and give it a random direction."""
        self.position_x = CONFIG.WINDOW_WIDTH // 2
        self.position_y = CONFIG.WINDOW_HEIGHT // 2
        
        # Set random initial velocity
        self.velocity_x, self.velocity_y = BallPhysics.generate_initial_velocity()
        
        # Create the collision rect
        self.rect = pygame.Rect(
            self.position_x - self.size // 2,
            self.position_y - self.size // 2,
            self.size,
            self.size
        )
        
        # Reset trail
        self.trail = []
    
    def update(self, dt, paddles):
        """
        Update the ball's position and handle collisions.
        
        Args:
            dt: Delta time for frame-rate independent physics
            paddles: List of paddle objects to check collisions against
        
        Returns:
            int: 0 if no score, 1 if right player scored, -1 if left player scored
        """
        # Safety check for extreme dt values that could cause physics issues
        if dt > 0.1:  # Cap dt to avoid physics bugs on slow machines
            dt = 0.1
        
        # Store previous position for trail
        prev_pos = (self.position_x, self.position_y)
        
        # Calculate new position
        self.position_x += self.velocity_x * dt * 60
        self.position_y += self.velocity_y * dt * 60
        
        # Update the rect for collision detection
        self.rect.x = self.position_x - self.size // 2
        self.rect.y = self.position_y - self.size // 2
        
        # Handle wall collisions (top and bottom)
        if CollisionDetector.check_ball_wall_collision(self, CONFIG.WINDOW_HEIGHT):
            self.velocity_y = BallPhysics.calculate_wall_collision(self.velocity_y)
            # Ensure ball stays in bounds
            if self.rect.top < 0:
                self.rect.top = 0
                self.position_y = self.rect.centery
            elif self.rect.bottom > CONFIG.WINDOW_HEIGHT:
                self.rect.bottom = CONFIG.WINDOW_HEIGHT
                self.position_y = self.rect.centery
                
            if self.has_sounds and hasattr(self, 'wall_sound'):
                try:
                    self.wall_sound.play()
                except:
                    pass  # Ignore sound errors
        
        # Handle paddle collisions
        for paddle in paddles:
            if CollisionDetector.check_ball_paddle_collision(self, paddle):
                # Determine which side the paddle is on
                is_left_paddle = paddle.position_x < CONFIG.WINDOW_WIDTH // 2
                
                # Calculate new velocity based on physics
                self.velocity_x, self.velocity_y = BallPhysics.calculate_collision_velocity(
                    self, paddle, is_left_paddle)
                
                # Apply spin effect based on paddle's movement
                self.velocity_x, self.velocity_y = BallPhysics.apply_spin(
                    self.velocity_x, self.velocity_y, paddle.velocity)
                
                # Prevent the ball from getting stuck in the paddle
                if is_left_paddle:  # Left paddle
                    self.rect.left = paddle.rect.right
                    self.position_x = self.rect.centerx
                else:  # Right paddle
                    self.rect.right = paddle.rect.left
                    self.position_x = self.rect.centerx
                
                if self.has_sounds and hasattr(self, 'paddle_sound'):
                    try:
                        self.paddle_sound.play()
                    except:
                        pass  # Ignore sound errors
                
                # Create a trail on paddle hit (simplified)
                self.trail.append(prev_pos)
        
        # Check if the ball is out of bounds (scoring)
        goal_result = CollisionDetector.check_ball_goal_collision(self, CONFIG.WINDOW_WIDTH)
        if goal_result != 0:
            if self.has_sounds and hasattr(self, 'score_sound'):
                try:
                    self.score_sound.play()
                except:
                    pass  # Ignore sound errors
            self.reset()
            return goal_result
        
        # Update trail (simplified)
        self.trail.append((self.position_x, self.position_y))
        while len(self.trail) > self.max_trail_length:
            self.trail.pop(0)
        
        return 0  # No scoring
    
    def render(self, screen):
        """
        Render the ball on the screen.
        
        Args:
            screen: Pygame surface to render on
        """
        # Simplified trail rendering
        if len(self.trail) > 1:
            for i, (x, y) in enumerate(self.trail[:-1]):  # Don't render the last position (current ball position)
                # Simpler trail effect
                size = max(4, self.size - (len(self.trail) - i) * 2)
                opacity = int(100 * (i / len(self.trail)))
                
                # Draw simplified trail
                pygame.draw.circle(
                    screen,
                    (255, 255, 255, opacity),  # White with fading opacity
                    (int(x), int(y)),
                    size // 2
                )
        
        # Draw the ball (as a circle for simplicity and better performance)
        pygame.draw.circle(
            screen, 
            CONFIG.WHITE, 
            (int(self.position_x), int(self.position_y)),
            self.size // 2
        )