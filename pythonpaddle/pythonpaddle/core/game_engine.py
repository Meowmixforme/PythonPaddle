"""Core game engine implementing game loop and state management."""
import pygame
import sys
import time
from pythonpaddle.utils.config import CONFIG
from pythonpaddle.states.state_machine import StateMachine
from pythonpaddle.states.menu_state import MenuState
from pythonpaddle.states.game_state import GameState


class GameEngine:
    """Main game engine class handling the game loop and state management."""
    
    def __init__(self):
        """Initialize the game engine."""
        pygame.init()
        pygame.display.set_caption(CONFIG.WINDOW_TITLE)
        
        self.screen = pygame.display.set_mode((CONFIG.WINDOW_WIDTH, CONFIG.WINDOW_HEIGHT))
        self.clock = pygame.time.Clock()
        self.running = False
        
        # For stability monitoring
        self.last_time = time.time()
        self.frame_count = 0
        self.fps_timer = 0
        
        # Initialize the state machine
        self.state_machine = StateMachine()
        
        try:
            # Create and add states
            menu_state = MenuState(self)
            game_state_ai = GameState(self, is_ai_opponent=True)
            game_state_2p = GameState(self, is_ai_opponent=False)
            
            self.state_machine.add("menu", menu_state)
            self.state_machine.add("game_ai", game_state_ai)
            self.state_machine.add("game_2p", game_state_2p)
        except Exception as e:
            print(f"Error during state initialization: {e}")
            raise
    
    def run(self):
        """Run the main game loop."""
        self.running = True
        self.last_time = time.time()
        self.state_machine.change("menu")
        
        try:
            while self.running:
                # Calculate delta time for frame-rate independent movement
                # Cap dt to avoid physics bugs on slow machines or when window is dragged
                dt = min(self.clock.tick(CONFIG.FPS) / 1000.0, 0.1)
                
                # Performance monitoring
                self.frame_count += 1
                self.fps_timer += dt
                if self.fps_timer >= 1.0:  # Every second
                    self.fps_timer = 0
                    self.frame_count = 0
                
                # Process input
                try:
                    events = pygame.event.get()
                    for event in events:
                        if event.type == pygame.QUIT:
                            self.running = False
                        self.state_machine.handle_event(event)
                except Exception as e:
                    print(f"Event handling error: {e}")
                    continue  # Skip this frame but continue game
                
                # Update game state
                try:
                    self.state_machine.update(dt)
                except Exception as e:
                    print(f"Update error: {e}")
                    continue  # Skip this frame but continue game
                
                # Render
                try:
                    self.screen.fill(CONFIG.BLACK)
                    self.state_machine.render(self.screen)
                    pygame.display.flip()
                except Exception as e:
                    print(f"Render error: {e}")
                    continue  # Skip this frame but continue game
                
        except Exception as e:
            print(f"Critical game loop error: {e}")
        
        finally:
            self._cleanup()
    
    def quit(self):
        """Set the running flag to False to exit the game loop."""
        self.running = False
    
    def _cleanup(self):
        """Clean up resources before exiting."""
        try:
            pygame.quit()
        except:
            pass
        sys.exit()