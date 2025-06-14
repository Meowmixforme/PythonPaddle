"""
Main entry point for the pythonpaddle game.
This standalone script runs the game without requiring package installation.
"""
import os
import sys
import pygame

# Add the project root directory to Python's import path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def main():
    """Initialize and run the game."""
    try:
        # Initialize pygame
        pygame.init()
        
        # Import the game engine (done here to ensure path is set first)
        from pythonpaddle.core.game_engine import GameEngine
        
        # Create and run the game engine
        print("Starting pythonpaddle game...")
        engine = GameEngine()
        engine.run()
        
    except ImportError as e:
        print(f"Import error: {e}")
        print("\nThis may be due to incorrect file structure or missing files.")
        print("Please ensure all files are in the correct directories.")
        
    except Exception as e:
        print(f"Error running game: {e}")
        import traceback
        traceback.print_exc()
        
    finally:
        # Clean up pygame
        pygame.quit()


if __name__ == "__main__":
    main()