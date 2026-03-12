"""Ghost Manager for coordinating all four ghosts."""
from __future__ import annotations

from ..core.config import GHOST_VULNERABLE_DURATION
from ..core.types import MazeProtocol, PacManProtocol, Position
from .ghost import Blinky, Clyde, Ghost, GhostMode, GhostState, Inky, Pinky


class GhostManager:
    """Manages all four ghosts and their coordinated behaviors."""

    def __init__(self, maze: MazeProtocol) -> None:
        """Initialize the ghost manager with ghost starting positions."""
        self.maze: MazeProtocol = maze

        ghost_spawns = maze.get_ghost_spawn_positions()

        while len(ghost_spawns) < 4:
            if ghost_spawns:
                ghost_spawns.append(ghost_spawns[0])
            else:
                ghost_spawns.append(Position(maze.width // 2, maze.height // 2))

        blinky = Blinky(ghost_spawns[0].x, ghost_spawns[0].y)
        pinky = Pinky(ghost_spawns[1].x, ghost_spawns[1].y)
        inky = Inky(ghost_spawns[2].x, ghost_spawns[2].y, blinky)
        clyde = Clyde(
            ghost_spawns[3].x if len(ghost_spawns) > 3 else ghost_spawns[0].x,
            ghost_spawns[3].y if len(ghost_spawns) > 3 else ghost_spawns[0].y
        )

        self.ghosts: list[Ghost] = [blinky, pinky, inky, clyde]

        for ghost in self.ghosts:
            ghost.set_scatter_target_for_maze(maze)

        self.previous_ghost_positions: list[Position] = []
        self._update_previous_positions()

        self.mode_timer: float = 0.0
        self.current_mode_duration: float = 7.0
        self.mode_sequence: list[tuple[GhostMode, float]] = [
            (GhostMode.SCATTER, 7.0),
            (GhostMode.CHASE, 20.0),
            (GhostMode.SCATTER, 7.0),
            (GhostMode.CHASE, 20.0),
            (GhostMode.SCATTER, 5.0),
            (GhostMode.CHASE, 20.0),
            (GhostMode.SCATTER, 5.0),
            (GhostMode.CHASE, float('inf'))
        ]
        self.sequence_index: int = 0

        self.ghosts_eaten_in_sequence: int = 0
        self.vulnerability_expired: bool = False

    def _update_previous_positions(self) -> None:
        """Store current ghost positions as previous positions."""
        self.previous_ghost_positions = [ghost.get_position() for ghost in self.ghosts]

    def reset(self) -> None:
        """Reset all ghosts to starting state."""
        for ghost in self.ghosts:
            ghost.reset()
            ghost.set_scatter_target_for_maze(self.maze)

        self._update_previous_positions()

        self.mode_timer = 0.0
        self.sequence_index = 0
        self.current_mode_duration = self.mode_sequence[0][1]
        self.ghosts_eaten_in_sequence = 0
        self.vulnerability_expired = False

    def update(self, delta_time: float, maze: MazeProtocol, pacman: PacManProtocol) -> None:
        """Update all ghosts and mode timing."""
        self._update_previous_positions()

        was_any_vulnerable: bool = any(ghost.is_vulnerable() for ghost in self.ghosts)

        self.mode_timer += delta_time

        if not was_any_vulnerable:
            if (self.sequence_index < len(self.mode_sequence) and
                    self.mode_timer >= self.current_mode_duration):

                self.sequence_index += 1
                if self.sequence_index < len(self.mode_sequence):
                    next_mode, duration = self.mode_sequence[self.sequence_index]
                    self._set_all_ghost_mode(next_mode)
                    self.current_mode_duration = duration
                    self.mode_timer = 0.0

        for ghost in self.ghosts:
            ghost.update(delta_time, maze, pacman)

        any_vulnerable_now: bool = any(ghost.is_vulnerable() for ghost in self.ghosts)

        if was_any_vulnerable and not any_vulnerable_now:
            self.ghosts_eaten_in_sequence = 0
            self.vulnerability_expired = True
        else:
            self.vulnerability_expired = False

    def _set_all_ghost_mode(self, mode: GhostMode) -> None:
        """Set mode for all active ghosts that aren't vulnerable or eaten."""
        for ghost in self.ghosts:
            if ghost.mode not in (GhostMode.VULNERABLE, GhostMode.EATEN):
                if ghost.state != GhostState.RETURNING:
                    ghost.set_mode(mode)

    def make_all_vulnerable(self) -> None:
        """Make all ghosts vulnerable after power pellet consumption."""
        for ghost in self.ghosts:
            ghost.make_vulnerable(GHOST_VULNERABLE_DURATION)
        self.ghosts_eaten_in_sequence = 0

    def check_collision_with_pacman(
            self,
            pacman: PacManProtocol,
            previous_pacman_pos: Position | None = None
    ) -> Ghost | None:
        """
        Check if any ghost collides with Pac-Man.

        This checks for:
        1. Same cell collision (ghost and Pac-Man in same position)
        2. Crossing collision (ghost and Pac-Man swapped positions)

        Args:
            pacman: The Pac-Man instance
            previous_pacman_pos: Pac-Man's position before this frame's movement

        Returns:
            The colliding ghost, or None if no collision
        """
        pac_pos = pacman.get_position()
        px, py = pac_pos.x, pac_pos.y

        for i, ghost in enumerate(self.ghosts):
            if ghost.state != GhostState.ACTIVE:
                continue
            if ghost.mode == GhostMode.EATEN:
                continue

            ghost_pos = ghost.get_position()
            gx, gy = ghost_pos.x, ghost_pos.y

            if gx == px and gy == py:
                if ghost.is_vulnerable():
                    self.eat_ghost(ghost)
                return ghost

            if previous_pacman_pos is not None and i < len(self.previous_ghost_positions):
                prev_px, prev_py = previous_pacman_pos.x, previous_pacman_pos.y
                prev_ghost_pos = self.previous_ghost_positions[i]
                prev_gx, prev_gy = prev_ghost_pos.x, prev_ghost_pos.y

                pacman_moved_to_ghost: bool = (px == prev_gx and py == prev_gy)
                ghost_moved_to_pacman: bool = (gx == prev_px and gy == prev_py)

                if pacman_moved_to_ghost and ghost_moved_to_pacman:
                    if ghost.is_vulnerable():
                        self.eat_ghost(ghost)
                    return ghost

                if pacman_moved_to_ghost and (gx == prev_gx and gy == prev_gy):
                    if ghost.is_vulnerable():
                        self.eat_ghost(ghost)
                    return ghost

                if ghost_moved_to_pacman and (px == prev_px and py == prev_py):
                    if ghost.is_vulnerable():
                        self.eat_ghost(ghost)
                    return ghost

        return None

    def eat_ghost(self, ghost: Ghost) -> int:
        """
        Handle ghost being eaten by Pac-Man.

        Args:
            ghost: The ghost being eaten

        Returns:
            Points scored for eating the ghost
        """
        if ghost.is_vulnerable():
            ghost.get_eaten()

            base_score: int = 200
            score: int = base_score * (2 ** self.ghosts_eaten_in_sequence)
            self.ghosts_eaten_in_sequence += 1

            return min(score, 1600)

        return 0

    def get_ghost_positions(self) -> list[tuple[int, int, str, str]]:
        """Get positions of all ghosts for rendering."""
        positions: list[tuple[int, int, str, str]] = []
        for ghost in self.ghosts:
            pos = ghost.get_position()
            sprite: str = ghost.get_sprite()
            color: str = ghost.get_color()
            positions.append((pos.x, pos.y, sprite, color))

        return positions

    def get_vulnerable_ghosts(self) -> list[Ghost]:
        """Get list of currently vulnerable ghosts."""
        return [ghost for ghost in self.ghosts if ghost.is_vulnerable()]

    def get_dangerous_ghosts(self) -> list[Ghost]:
        """Get list of currently dangerous ghosts."""
        return [ghost for ghost in self.ghosts if ghost.is_dangerous()]

    def are_all_ghosts_home(self) -> bool:
        """Check if all ghosts are in the ghost house."""
        return all(ghost.state == GhostState.IN_HOUSE for ghost in self.ghosts)

    def get_ghost_by_name(self, name: str) -> Ghost | None:
        """Get a specific ghost by name."""
        for ghost in self.ghosts:
            if ghost.name.lower() == name.lower():
                return ghost
        return None
