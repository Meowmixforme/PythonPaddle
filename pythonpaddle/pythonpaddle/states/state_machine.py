"""State machine for managing game states."""


class StateMachine:
    """
    A finite state machine that manages game states.
    
    This allows for clean transitions between different game screens (menu, gameplay, etc.)
    """
    
    def __init__(self):
        """Initialize the state machine."""
        self.states = {}
        self.current = None
    
    def add(self, state_name, state_instance):
        """
        Add a state to the state machine.
        
        Args:
            state_name: String identifier for the state
            state_instance: Instance of a state class
        """
        self.states[state_name] = state_instance
    
    def change(self, state_name):
        """
        Change to a different state.
        
        Args:
            state_name: String identifier for the state to change to
        """
        if self.current:
            self.current.exit()
        
        self.current = self.states[state_name]
        self.current.enter()
    
    def handle_event(self, event):
        """
        Pass events to the current state.
        
        Args:
            event: pygame event to process
        """
        if self.current:
            self.current.handle_event(event)
    
    def update(self, dt):
        """
        Update the current state.
        
        Args:
            dt: Delta time for frame-rate independent movement
        """
        if self.current:
            self.current.update(dt)
    
    def render(self, screen):
        """
        Render the current state.
        
        Args:
            screen: pygame surface to render on
        """
        if self.current:
            self.current.render(screen)