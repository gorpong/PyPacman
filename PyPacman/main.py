"""Main entry point for ASCII Pac-Man game."""

import sys
from .core.game_engine import GameEngine


def main() -> None:
    """Main function to start the game."""
    try:
        game = GameEngine()
        game.start()
    except Exception as e:
        print(f"Error starting game: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
