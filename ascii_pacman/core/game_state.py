"""Game state management for lives, levels, and progression."""

from typing import Tuple


class GameState:
    """Manages game state including lives, level, and game over."""
    
    def __init__(self, starting_lives: int = 3):
        """
        Initialize game state.
        
        Args:
            starting_lives: Number of lives to start with
        """
        self.starting_lives = starting_lives
        self.lives = starting_lives
        self.level = 1
        self.game_over = False
        
    def reset(self) -> None:
        """Reset game state for new game."""
        self.lives = self.starting_lives
        self.level = 1
        self.game_over = False
        
    def lose_life(self) -> bool:
        """
        Lose a life.
        
        Returns:
            True if game over (no lives left), False otherwise
        """
        self.lives -= 1
        if self.lives <= 0:
            self.game_over = True
            return True
        return False
        
    def add_life(self) -> None:
        """Add an extra life."""
        self.lives += 1
        
    def next_level(self) -> int:
        """
        Advance to next level.
        
        Returns:
            The new level number
        """
        self.level += 1
        return self.level
        
    def is_game_over(self) -> bool:
        """Check if game is over."""
        return self.game_over
        
    def get_lives(self) -> int:
        """Get current number of lives."""
        return self.lives
        
    def get_level(self) -> int:
        """Get current level."""
        return self.level
        
    def get_ghost_speed_multiplier(self) -> float:
        """
        Get ghost speed multiplier based on level.
        Ghosts get faster as levels progress.
        
        Returns:
            Speed multiplier (1.0 = normal, >1.0 = faster)
        """
        # Increase speed by 5% per level, cap at 2x speed
        return min(1.0 + (self.level - 1) * 0.05, 2.0)
        
    def get_pacman_speed_multiplier(self) -> float:
        """
        Get Pac-Man speed multiplier based on level.
        Pac-Man gets slightly faster too, but not as much as ghosts.
        
        Returns:
            Speed multiplier (1.0 = normal, >1.0 = faster)
        """
        # Increase speed by 3% per level, cap at 1.5x speed
        return min(1.0 + (self.level - 1) * 0.03, 1.5)
