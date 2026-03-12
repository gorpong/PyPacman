"""ASCII Pac-Man - A terminal-based version of the classic arcade game."""

__version__ = "1.0.0"
__author__ = "ASCII Game Studio"

__all__ = ["main"]


def main() -> None:
    """Launch the game without eagerly importing the full runtime."""
    from .main import main as _main

    _main()
