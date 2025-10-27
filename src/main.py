"""
Main entry point for ASCII Pac-Man game.
"""

import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.game_engine import GameEngine


def main():
    """Main function to start the game."""
    try:
        game = GameEngine()
        game.start()
    except Exception as e:
        print(f"Error starting game: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
