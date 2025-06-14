"""Menu state for the pythonpaddle game."""
import pygame
from pythonpaddle.utils.config import CONFIG


class MenuState:
    """Menu state handling the main menu screen."""
    
    def __init__(self, engine):
        """
        Initialize the menu state.
        
        Args:
            engine: Reference to the main game engine
        """
        self.engine = engine
        self.title_font = pygame.font.Font(None, 100)
        self.menu_font = pygame.font.Font(None, 36)
        
        self.title_text = self.title_font.render("PythonPaddle", True, CONFIG.WHITE)
        self.title_rect = self.title_text.get_rect(center=(CONFIG.WINDOW_WIDTH // 2, CONFIG.WINDOW_HEIGHT // 4))
        
        self.options = [
            {"text": "Single Player", "action": "game_ai"},
            {"text": "Two Players", "action": "game_2p"},
            {"text": "Exit", "action": "quit"}
        ]
        
        self.selected_option = 0
    
    def enter(self):
        """Called when entering this state."""
        pass
    
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
            if event.key == pygame.K_UP:
                self.selected_option = (self.selected_option - 1) % len(self.options)
            elif event.key == pygame.K_DOWN:
                self.selected_option = (self.selected_option + 1) % len(self.options)
            elif event.key == pygame.K_RETURN:
                action = self.options[self.selected_option]["action"]
                if action == "quit":
                    self.engine.quit()
                else:
                    self.engine.state_machine.change(action)
    
    def update(self, dt):
        """
        Update menu state.
        
        Args:
            dt: Delta time for frame-rate independent movement
        """
        pass
    
    def render(self, screen):
        """
        Render the menu to the screen.
        
        Args:
            screen: pygame surface to render on
        """
        # Draw title
        screen.blit(self.title_text, self.title_rect)
        
        # Draw menu options
        for i, option in enumerate(self.options):
            text_color = CONFIG.YELLOW if i == self.selected_option else CONFIG.WHITE
            text = self.menu_font.render(option["text"], True, text_color)
            rect = text.get_rect(center=(CONFIG.WINDOW_WIDTH // 2, CONFIG.WINDOW_HEIGHT // 2 + i * 50))
            screen.blit(text, rect)
        
        # Draw instructions
        instructions_text = self.menu_font.render("Use UP/DOWN arrows and ENTER to select", True, CONFIG.WHITE)
        instructions_rect = instructions_text.get_rect(center=(CONFIG.WINDOW_WIDTH // 2, CONFIG.WINDOW_HEIGHT * 0.8))
        screen.blit(instructions_text, instructions_rect)