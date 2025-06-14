"""Sound manager for the pythonpaddle game."""
import os
import pygame
from pythonpaddle.utils.config import CONFIG


class SoundManager:
    """Manages sound effects for the game."""
    
    def __init__(self):
        """Initialize the sound manager."""
        self.sounds = {}
        self.enabled = CONFIG.SOUND_ENABLED
        self.volume = CONFIG.SOUND_VOLUME
        
        # Try to initialize the mixer
        try:
            pygame.mixer.init()
            pygame.mixer.set_num_channels(8)
        except pygame.error:
            print("Warning: Sound system could not be initialized")
            self.enabled = False
        
        # Create base directories and placeholder sounds
        self._ensure_sound_files()
    
    def _ensure_sound_files(self):
        """Create sound directories and placeholder files if they don't exist."""
        # Create assets/sounds directory
        sound_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 
                                "assets", "sounds")
        os.makedirs(sound_dir, exist_ok=True)
        
        # Create placeholder sound files if they don't exist
        sound_files = {
            "paddle_hit": "paddle_hit.wav",
            "wall_hit": "wall_hit.wav",
            "score": "score.wav"
        }
        
        for sound_name, filename in sound_files.items():
            sound_path = os.path.join(sound_dir, filename)
            if not os.path.exists(sound_path):
                print(f"Creating placeholder sound: {sound_path}")
                with open(sound_path, "wb") as f:
                    # Write minimal WAV file header
                    f.write(b"RIFF\x24\x00\x00\x00WAVEfmt \x10\x00\x00\x00\x01\x00\x01\x00\x44\xAC\x00\x00\x88\x58\x01\x00\x02\x00\x10\x00data\x00\x00\x00\x00")
    
    def load_sounds(self):
        """Load all sound effects."""
        if not self.enabled:
            return
        
        sound_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 
                                "assets", "sounds")
        
        sound_files = {
            "paddle_hit": "paddle_hit.wav",
            "wall_hit": "wall_hit.wav",
            "score": "score.wav"
        }
        
        for sound_name, filename in sound_files.items():
            sound_path = os.path.join(sound_dir, filename)
            try:
                self.sounds[sound_name] = pygame.mixer.Sound(sound_path)
                self.sounds[sound_name].set_volume(self.volume)
            except pygame.error:
                print(f"Warning: Could not load sound {sound_path}")
    
    def play(self, sound_name):
        """
        Play a sound effect by name.
        
        Args:
            sound_name: The name of the sound to play
        """
        if self.enabled and sound_name in self.sounds:
            self.sounds[sound_name].play()
    
    def set_volume(self, volume):
        """
        Set the volume for all sounds.
        
        Args:
            volume: Volume level (0.0 to 1.0)
        """
        self.volume = max(0.0, min(1.0, volume))
        for sound in self.sounds.values():
            sound.set_volume(self.volume)
    
    def toggle(self):
        """Toggle sound on/off."""
        self.enabled = not self.enabled
        return self.enabled