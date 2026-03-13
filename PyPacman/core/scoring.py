"""Scoring system for ASCII Pac-Man."""
from __future__ import annotations

import json
from pathlib import Path

from .config import (
    SCORE_DOT,
    SCORE_GHOST_BASE,
    SCORE_GHOST_MAX,
    SCORE_GHOST_MULTIPLIER,
    SCORE_POWER_PELLET,
)


class ScoringSystem:
    """Manages game scoring and points."""

    def __init__(self) -> None:
        """Initialize scoring system."""
        self.score: int = 0
        self.ghosts_eaten_combo: int = 0

        self.high_score_file: Path = Path.home() / ".ascii_pacman_scores.json"
        self.high_scores: list[tuple[str, int]] = self._load_high_scores()

    def _load_high_scores(self) -> list[tuple[str, int]]:
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
            pass

    def reset(self) -> None:
        """Reset score for new game."""
        self.score = 0
        self.ghosts_eaten_combo = 0

    def add_dot(self) -> int:
        """Award points for eating a dot."""
        self.score += SCORE_DOT
        return SCORE_DOT

    def add_power_pellet(self) -> int:
        """Award points for eating a power pellet."""
        self.score += SCORE_POWER_PELLET
        return SCORE_POWER_PELLET

    def _calculate_ghost_points(self, combo_count: int) -> int:
        """
        Calculate ghost points based on combo count.

        Args:
            combo_count: Number of ghosts already eaten in this combo (0-based)

        Returns:
            Points for the next ghost, capped at SCORE_GHOST_MAX
        """
        points = SCORE_GHOST_BASE * (SCORE_GHOST_MULTIPLIER ** combo_count)
        return min(points, SCORE_GHOST_MAX)

    def get_next_ghost_points(self) -> int:
        """
        Get the points that would be awarded for eating the next ghost.

        This does not modify state - use add_ghost() to actually award points.

        Returns:
            Points for the next ghost
        """
        return self._calculate_ghost_points(self.ghosts_eaten_combo)

    def add_ghost(self) -> int:
        """
        Award points for eating a ghost (progressive scoring).

        Points double with each ghost eaten: 200, 400, 800, 1600 (capped).

        Returns:
            Points awarded
        """
        points = self._calculate_ghost_points(self.ghosts_eaten_combo)
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
        self.high_scores.append((name, self.score))
        self.high_scores.sort(key=lambda x: x[1], reverse=True)

        rank = 0
        for i, (n, s) in enumerate(self.high_scores[:10]):
            if n == name and s == self.score:
                rank = i + 1
                break

        self.high_scores = self.high_scores[:10]
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

    def get_high_scores(self) -> list[tuple[str, int]]:
        """Get all high scores."""
        return self.high_scores.copy()
