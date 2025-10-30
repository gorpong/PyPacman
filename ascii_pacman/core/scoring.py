"""Scoring system for ASCII Pac-Man."""

import os
import json
from typing import Optional, List, Tuple
from pathlib import Path


class ScoringSystem:
    """Manages game scoring and points."""
    
    # Score values
    DOT_POINTS = 10
    POWER_PELLET_POINTS = 50
    GHOST_BASE_POINTS = 200  # First ghost: 200, 2nd: 400, 3rd: 800, 4th: 1600
    
    def __init__(self):
        """Initialize scoring system."""
        self.score = 0
        self.ghosts_eaten_combo = 0  # Resets when power pellet wears off
        
        # High score file location (hidden file in home directory)
        self.high_score_file = Path.home() / ".ascii_pacman_scores.json"
        self.high_scores = self._load_high_scores()
        
    def _load_high_scores(self) -> List[Tuple[str, int]]:
        """Load high scores from file."""
        if self.high_score_file.exists():
            try:
                with open(self.high_score_file, 'r') as f:
                    data = json.load(f)
                    return [(entry['name'], entry['score']) for entry in data]
            except (json.JSONDecodeError, KeyError, IOError):
                return []
        return []
    
    def _save_high_scores(self) -> None:
        """Save high scores to file."""
        try:
            data = [{'name': name, 'score': score} for name, score in self.high_scores]
            with open(self.high_score_file, 'w') as f:
                json.dump(data, f, indent=2)
        except IOError:
            pass  # Silently fail if can't save
        
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
        # Don't reset combo here - it should reset when pellet is collected
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
        
    def is_high_score(self) -> bool:
        """Check if current score qualifies as a high score."""
        if not self.high_scores or len(self.high_scores) < 10:
            return self.score > 0
        return self.score > self.high_scores[-1][1]
    
    def add_high_score(self, name: str) -> int:
        """
        Add a high score entry.
        
        Args:
            name: Player name/initials
            
        Returns:
            Rank (1-10) of the new score, or 0 if not in top 10
        """
        # Add new score
        self.high_scores.append((name, self.score))
        
        # Sort by score descending
        self.high_scores.sort(key=lambda x: x[1], reverse=True)
        
        # Keep only top 10
        rank = 0
        for i, (n, s) in enumerate(self.high_scores[:10]):
            if n == name and s == self.score:
                rank = i + 1
                break
        
        self.high_scores = self.high_scores[:10]
        
        # Save to file
        self._save_high_scores()
        
        return rank
        
    def get_score(self) -> int:
        """Get current score."""
        return self.score
        
    def get_high_score(self) -> int:
        """Get the highest score."""
        if self.high_scores:
            return self.high_scores[0][1]
        return 0
    
    def get_high_scores(self) -> List[Tuple[str, int]]:
        """Get all high scores."""
        return self.high_scores.copy()
