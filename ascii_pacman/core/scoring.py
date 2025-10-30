"""Scoring system for ASCII Pac-Man."""

from typing import Optional


class ScoringSystem:
    """Manages game scoring and points."""
    
    # Score values
    DOT_POINTS = 10
    POWER_PELLET_POINTS = 50
    GHOST_BASE_POINTS = 200  # First ghost: 200, 2nd: 400, 3rd: 800, 4th: 1600
    
    def __init__(self):
        """Initialize scoring system."""
        self.score = 0
        self.high_score = 0
        self.ghosts_eaten_combo = 0  # Resets when power pellet wears off
        
    def reset(self) -> None:
        """Reset score for new game."""
        self.score = 0
        self.ghosts_eaten_combo = 0
        
    def add_dot(self) -> int:
        """Award points for eating a dot."""
        self.score += self.DOT_POINTS
        return self.DOT_POINTS
        
    def add_power_pellet(self) -> int:
        """Award points for eating a power pellet."""
        self.score += self.POWER_PELLET_POINTS
        self.ghosts_eaten_combo = 0  # Reset combo for new power pellet
        return self.POWER_PELLET_POINTS
        
    def add_ghost(self) -> int:
        """Award points for eating a ghost (progressive scoring)."""
        points = self.GHOST_BASE_POINTS * (2 ** self.ghosts_eaten_combo)
        self.score += points
        self.ghosts_eaten_combo += 1
        return points
        
    def reset_ghost_combo(self) -> None:
        """Reset ghost combo counter (when power pellet wears off)."""
        self.ghosts_eaten_combo = 0
        
    def update_high_score(self) -> bool:
        """Update high score if current score is higher."""
        if self.score > self.high_score:
            self.high_score = self.score
            return True
        return False
        
    def get_score(self) -> int:
        """Get current score."""
        return self.score
        
    def get_high_score(self) -> int:
        """Get high score."""
        return self.high_score
