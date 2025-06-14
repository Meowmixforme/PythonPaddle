"""Physics engine for the pythonpaddle game."""
import math
import random
from pythonpaddle.utils.config import CONFIG


class BallPhysics:
    """Handles physics calculations for the ball."""
    
    @staticmethod
    def calculate_collision_velocity(ball, paddle, is_left_paddle):
        """
        Calculate new velocity after a paddle collision.
        
        Args:
            ball: The ball object
            paddle: The paddle object that was hit
            is_left_paddle: True if the ball hit the left paddle, False for right paddle
            
        Returns:
            tuple: (new_velocity_x, new_velocity_y)
        """
        try:
            # Calculate where the ball hit the paddle (normalized from -1 to 1)
            # -1 means hitting the top of the paddle, 1 means hitting the bottom
            relative_intersect_y = (paddle.rect.centery - ball.rect.centery)
            normalized_intersect_y = relative_intersect_y / (paddle.rect.height / 2)
            # Clamp the value between -1 and 1
            normalized_intersect_y = max(-1.0, min(1.0, normalized_intersect_y))
            
            # Calculate bounce angle based on where the ball hit the paddle
            # The angle will be between -45 and 45 degrees (in radians)
            bounce_angle = normalized_intersect_y * (math.pi / 4)
            
            # Calculate current speed of the ball
            current_speed = math.sqrt(ball.velocity_x**2 + ball.velocity_y**2)
            
            # Increase speed slightly with each paddle hit
            new_speed = current_speed + CONFIG.BALL_SPEED_INCREASE
            new_speed = min(new_speed, CONFIG.MAX_BALL_SPEED)  # Cap the maximum speed
            
            # Calculate new velocity components
            direction = 1 if is_left_paddle else -1
            new_velocity_x = direction * new_speed * math.cos(bounce_angle)
            new_velocity_y = -new_speed * math.sin(bounce_angle)
            
            # Safety check for NaN or infinity values
            if math.isnan(new_velocity_x) or math.isinf(new_velocity_x) or \
               math.isnan(new_velocity_y) or math.isinf(new_velocity_y):
                # Fallback to simpler calculation
                new_velocity_x = direction * CONFIG.BALL_SPEED_X
                new_velocity_y = random.uniform(-0.5, 0.5) * CONFIG.BALL_SPEED_Y
                
            return new_velocity_x, new_velocity_y
            
        except Exception as e:
            # In case of any error, return safe default values
            print(f"Physics calculation error: {e}")
            direction = 1 if is_left_paddle else -1
            return direction * CONFIG.BALL_SPEED_X, random.uniform(-0.5, 0.5) * CONFIG.BALL_SPEED_Y
    
    @staticmethod
    def calculate_wall_collision(velocity_y):
        """
        Calculate new velocity after a wall (top/bottom) collision.
        
        Args:
            velocity_y: Current y velocity
            
        Returns:
            float: New y velocity
        """
        # Simply reverse the y velocity with a slight randomization
        try:
            randomization = random.uniform(0.95, 1.05)
            result = -velocity_y * randomization
            
            # Ensure velocity isn't too low
            if abs(result) < CONFIG.BALL_SPEED_Y * 0.5:
                result = math.copysign(CONFIG.BALL_SPEED_Y * 0.5, result)
            
            return result
        except:
            # Safe fallback
            return -velocity_y
    
    @staticmethod
    def generate_initial_velocity():
        """
        Generate a random initial velocity for the ball.
        
        Returns:
            tuple: (velocity_x, velocity_y)
        """
        try:
            # Generate a random angle between -45 and 45 degrees (in radians)
            angle = random.uniform(-math.pi/4, math.pi/4)
            
            # Randomly choose the horizontal direction
            direction = random.choice([-1, 1])
            
            # Calculate velocity components
            velocity_x = direction * CONFIG.BALL_SPEED_X * math.cos(angle)
            velocity_y = CONFIG.BALL_SPEED_Y * math.sin(angle)
            
            return velocity_x, velocity_y
        except:
            # Safe fallback
            direction = random.choice([-1, 1])
            return direction * CONFIG.BALL_SPEED_X, random.uniform(-0.5, 0.5) * CONFIG.BALL_SPEED_Y
    
    @staticmethod
    def apply_spin(velocity_x, velocity_y, paddle_velocity, spin_factor=0.2):
        """
        Apply spin effect to the ball based on paddle movement.
        
        Args:
            velocity_x: Current x velocity
            velocity_y: Current y velocity
            paddle_velocity: Velocity of the paddle that hit the ball
            spin_factor: How much the paddle's movement affects the ball
            
        Returns:
            tuple: (new_velocity_x, new_velocity_y)
        """
        try:
            # Apply paddle's movement to the ball's vertical velocity
            new_velocity_y = velocity_y + (paddle_velocity * spin_factor)
            
            # Cap the maximum vertical velocity to prevent excessive angles
            max_y_velocity = abs(velocity_x * 0.75)
            if abs(new_velocity_y) > max_y_velocity:
                new_velocity_y = math.copysign(max_y_velocity, new_velocity_y)
            
            return velocity_x, new_velocity_y
        except:
            # Safe fallback - just return original velocities
            return velocity_x, velocity_y
    
    @staticmethod
    def predict_ball_position(ball, time_steps, window_height):
        """
        Predict where the ball will be after a certain time (for AI).
        
        Args:
            ball: The ball object
            time_steps: How many steps into the future to predict
            window_height: Height of the game window
            
        Returns:
            float: Predicted y position
        """
        try:
            # Simple prediction that ignores paddle collisions
            # but accounts for wall bounces
            pos_x = ball.position_x
            pos_y = ball.position_y
            vel_x = ball.velocity_x
            vel_y = ball.velocity_y
            
            # Limit time_steps for safer predictions
            actual_steps = min(time_steps, 30)
            
            # Simulate movement
            for _ in range(actual_steps):
                pos_x += vel_x
                pos_y += vel_y
                
                # Check for wall collisions
                if pos_y <= 0 or pos_y >= window_height:
                    vel_y = -vel_y
                    pos_y = max(0, min(window_height, pos_y))
            
            return pos_y
        except:
            # Safe fallback - return center of screen
            return window_height // 2


class CollisionDetector:
    """Handles collision detection between game objects."""
    
    @staticmethod
    def check_ball_paddle_collision(ball, paddle):
        """
        Check if the ball is colliding with a paddle.
        
        Args:
            ball: The ball object
            paddle: The paddle object
            
        Returns:
            bool: True if collision detected, False otherwise
        """
        try:
            return ball.rect.colliderect(paddle.rect)
        except:
            # In case of error, assume no collision
            return False
    
    @staticmethod
    def check_ball_wall_collision(ball, window_height):
        """
        Check if the ball is colliding with the top or bottom wall.
        
        Args:
            ball: The ball object
            window_height: Height of the game window
            
        Returns:
            bool: True if collision detected, False otherwise
        """
        try:
            return ball.rect.top <= 0 or ball.rect.bottom >= window_height
        except:
            # In case of error, assume no collision
            return False
    
    @staticmethod
    def check_ball_goal_collision(ball, window_width):
        """
        Check if the ball has entered a goal area (left or right edge).
        
        Args:
            ball: The ball object
            window_width: Width of the game window
            
        Returns:
            int: 1 if right player scored, -1 if left player scored, 0 otherwise
        """
        try:
            if ball.rect.right >= window_width:
                return -1  # Left player scored
            elif ball.rect.left <= 0:
                return 1  # Right player scored
            else:
                return 0  # No goal
        except:
            # In case of error, assume no scoring
            return 0