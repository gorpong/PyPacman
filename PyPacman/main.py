"""Main entry point for ASCII Pac-Man game."""

from __future__ import annotations

import argparse
import sys
from typing import Sequence

from .core.game_engine import GameEngine
from .data.levels import get_available_levels, LEVELS


def parse_level(value: str) -> int | str:
    """
    Parse and validate level argument.

    Args:
        value: The level value from command line

    Returns:
        Integer level number or string level name

    Raises:
        argparse.ArgumentTypeError: If level is invalid
    """
    # Try to parse as integer first
    try:
        level_int = int(value)
        if level_int in LEVELS:
            return level_int
        else:
            available = get_available_levels()
            raise argparse.ArgumentTypeError(
                f"Invalid level: {value}. Available levels: {available}"
            )
    except ValueError:
        # Not an integer, treat as string name
        if value in LEVELS:
            return value
        else:
            available = get_available_levels()
            raise argparse.ArgumentTypeError(
                f"Invalid level: '{value}'. Available levels: {available}"
            )


def parse_ghost_speed(value: str) -> float:
    """
    Parse and validate ghost speed argument.

    Args:
        value: The ghost speed value from command line

    Returns:
        Float speed multiplier

    Raises:
        argparse.ArgumentTypeError: If speed is invalid or out of range
    """
    try:
        speed = float(value)
    except ValueError:
        raise argparse.ArgumentTypeError(
            f"Invalid ghost speed: '{value}'. Must be a number."
        )

    if speed < 0.1 or speed > 2.0:
        raise argparse.ArgumentTypeError(
            f"Ghost speed must be between 0.1 and 2.0, got {speed}"
        )

    return speed


def format_level_list() -> str:
    """
    Format the list of available levels for display.

    Returns:
        Formatted string listing all available levels
    """
    levels = get_available_levels()

    lines = ["Available levels:", ""]

    # Separate numeric and named levels
    numeric_levels = sorted([l for l in levels if isinstance(l, int)])
    named_levels = sorted([l for l in levels if isinstance(l, str)])

    if numeric_levels:
        lines.append("  Standard levels:")
        for level in numeric_levels:
            lines.append(f"    {level}")

    if named_levels:
        lines.append("")
        lines.append("  Special/test levels:")
        for level in named_levels:
            lines.append(f"    {level}")

    lines.append("")
    lines.append("Usage: pacman --level <level>")
    lines.append("       pacman -l <level>")

    return "\n".join(lines)


def parse_args(args: Sequence[str] | None = None) -> argparse.Namespace:
    """
    Parse command-line arguments.

    Args:
        args: Command line arguments (defaults to sys.argv[1:])

    Returns:
        Parsed arguments namespace
    """
    parser = argparse.ArgumentParser(
        prog="pacman",
        description="ASCII Pac-Man - A terminal-based Pac-Man game",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  pacman                     Start game normally
  pacman -l test             Start with test level
  pacman -l 3 -g 0.5         Start at level 3 with slow ghosts
  pacman --list-levels       Show all available levels
        """
    )

    parser.add_argument(
        '-l', '--level',
        type=parse_level,
        default=None,
        metavar='LEVEL',
        help='Starting level (number or name, e.g., 1, 2, test, mini)'
    )

    parser.add_argument(
        '-g', '--ghost-speed',
        type=parse_ghost_speed,
        default=None,
        metavar='SPEED',
        help='Ghost speed multiplier (0.1-2.0, default: 1.0). '
             'Values < 1.0 slow ghosts down for testing.'
    )

    parser.add_argument(
        '-L', '--list-levels',
        action='store_true',
        help='List all available levels and exit'
    )

    return parser.parse_args(args)

def main() -> None:
    """Main function to start the game."""
    args = parse_args()

    # Handle --list-levels
    if args.list_levels:
        print(format_level_list())
        sys.exit(0)

    try:
        game = GameEngine(
            starting_level=args.level,
            ghost_speed_multiplier=args.ghost_speed
        )
        game.start()
    except Exception as e:
        print(f"Error starting game: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
