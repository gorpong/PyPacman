"""Ghost AI system implementation."""
from __future__ import annotations

import random
from collections import deque
from enum import Enum

from ..core.colors import Colors
from ..core.sprites import Sprites
from ..core.types import Direction, DirectionType, MazeProtocol, PacManProtocol, Position
from .base import MovableEntity


class GhostMode(Enum):
    """Ghost behavior modes."""
    SCATTER = "scatter"
    CHASE = "chase"
    VULNERABLE = "vulnerable"
    EATEN = "eaten"


class GhostState(Enum):
    """Ghost current state."""
    IN_HOUSE = "in_house"
    LEAVING_HOUSE = "leaving_house"
    ACTIVE = "active"
    RETURNING = "returning"


class GhostSpeed:
    """Speed multipliers for ghost movement."""
    NORMAL: float = 1.0
    VULNERABLE: float = 0.5
    EATEN: float = 2.0
    IN_HOUSE: float = 0.6
    LEAVING_HOUSE: float = 0.8


class Ghost(MovableEntity):
    """Base ghost class with common behaviors."""

    BASE_SPEED: float = 7.0

    def __init__(self, start_x: int, start_y: int, color: str, name: str) -> None:
        """Initialize a ghost."""
        super().__init__(start_x, start_y, speed=self.BASE_SPEED)

        self.color: str = color
        self.name: str = name

        self.mode: GhostMode = GhostMode.SCATTER
        self.state: GhostState = GhostState.IN_HOUSE
        self.target: Position = Position(start_x, start_y)

        self.mode_timer: float = 0.0
        self.vulnerable_timer: float = 0.0
        self.release_timer: float = 0.0

        self.scatter_target: Position = Position(1, 1)
        self.release_delay: float = 0.0

        self.house_exit_target: Position | None = None

        self.return_path: list[Position] = []
        self.path_target: Position | None = None

    def reset(self) -> None:
        """Reset ghost to starting position and state."""
        super().reset()
        self.direction = Direction.UP
        self.state = GhostState.IN_HOUSE
        self.mode = GhostMode.SCATTER
        self.mode_timer = 0.0
        self.vulnerable_timer = 0.0
        self.release_timer = 0.0
        self.house_exit_target = None
        self.return_path = []
        self.path_target = None

    def get_current_speed(self) -> float:
        """
        Calculate the current movement speed based on mode and state.

        Returns:
            The effective speed for this update
        """
        base: float = self.BASE_SPEED

        if self.state == GhostState.IN_HOUSE:
            return base * GhostSpeed.IN_HOUSE
        elif self.state == GhostState.LEAVING_HOUSE:
            return base * GhostSpeed.LEAVING_HOUSE
        elif self.state == GhostState.RETURNING:
            return base * GhostSpeed.EATEN

        if self.mode == GhostMode.VULNERABLE:
            return base * GhostSpeed.VULNERABLE
        elif self.mode == GhostMode.EATEN:
            return base * GhostSpeed.EATEN

        return base * GhostSpeed.NORMAL

    def update_movement(self, delta_time: float, maze: MazeProtocol) -> bool:
        """
        Update movement based on current speed and time.

        Args:
            delta_time: Time since last update
            maze: The maze object

        Returns:
            True if ghost should move this frame
        """
        self.move_timer += delta_time

        current_speed: float = self.get_current_speed()
        move_delay: float = 1.0 / current_speed

        if self.move_timer >= move_delay:
            self.move_timer = 0.0
            return True

        return False

    def set_scatter_target_for_maze(self, maze: MazeProtocol) -> None:
        """Set appropriate scatter target based on maze dimensions."""
        self.scatter_target = Position(1, 1)

    def find_house_exit(self, maze: MazeProtocol) -> Position | None:
        """
        Find the ghost house exit (position just outside the door).

        Args:
            maze: The maze object

        Returns:
            Position just outside the door, or None if not found
        """
        door_pos: Position | None = maze.get_ghost_door_position()
        if door_pos:
            door_x, door_y = door_pos.x, door_pos.y
            for check_y in range(door_y - 1, max(0, door_y - 3), -1):
                if maze.is_walkable(door_x, check_y, is_ghost=False):
                    return Position(door_x, check_y)
            return Position(door_x, door_y)

        if maze.ghost_house_cells:
            ghost_cells: list[tuple[int, int]] = list(maze.ghost_house_cells)
            min_y: int = min(c[1] for c in ghost_cells)
            center_x: int = sum(c[0] for c in ghost_cells) // len(ghost_cells)

            for y in range(min_y - 1, -1, -1):
                if maze.is_walkable(center_x, y, is_ghost=False):
                    return Position(center_x, y)

        return Position(maze.width // 2, maze.height // 2 - 3)

    def find_house_entrance(self, maze: MazeProtocol) -> Position | None:
        """
        Find the ghost house entrance (door position) for returning ghosts.

        Args:
            maze: The maze object

        Returns:
            Position of the ghost house door
        """
        door_pos = maze.get_ghost_door_position()
        if door_pos:
            return door_pos

        return Position(self.start_position.x, self.start_position.y)

    def _find_path_to_target(self, maze: MazeProtocol, target: Position) -> list[Position]:
        """
        Find a path from current position to target using BFS.

        Args:
            maze: The maze object
            target: The target position to reach

        Returns:
            List of positions forming the path (excluding current position)
        """
        start: tuple[int, int] = (self.position.x, self.position.y)
        goal: tuple[int, int] = (target.x, target.y)

        if start == goal:
            return []

        queue: deque[tuple[int, int]] = deque([start])
        came_from: dict[tuple[int, int], tuple[int, int] | None] = {start: None}

        directions: list[DirectionType] = Direction.all_directions()

        while queue:
            current: tuple[int, int] = queue.popleft()

            if current == goal:
                path: list[Position] = []
                while current != start:
                    path.append(Position(current[0], current[1]))
                    prev = came_from.get(current)
                    if prev is None:
                        break
                    current = prev
                path.reverse()
                return path

            for dx, dy in directions:
                next_x: int = current[0] + dx
                next_y: int = current[1] + dy
                next_pos = (next_x, next_y)

                if next_pos in came_from:
                    continue

                if maze.is_walkable_for_ghost(next_x, next_y):
                    came_from[next_pos] = current
                    queue.append(next_pos)

        return []

    def _get_next_path_direction(self, maze: MazeProtocol) -> DirectionType | None:
        """
        Get the next direction from the pre-calculated path.

        Args:
            maze: The maze object

        Returns:
            Direction to move, or None if no path
        """
        if not self.return_path:
            return None

        next_pos: Position = self.return_path[0]

        dx: int = next_pos.x - self.position.x
        dy: int = next_pos.y - self.position.y

        if dx != 0:
            dx = dx // abs(dx)
        if dy != 0:
            dy = dy // abs(dy)

        if self.position.x == next_pos.x and self.position.y == next_pos.y:
            self.return_path.pop(0)
            if self.return_path:
                return self._get_next_path_direction(maze)
            return None

        return (dx, dy)

    def update(self, delta_time: float, maze: MazeProtocol, pacman: PacManProtocol) -> None:
        """Update ghost AI and movement."""
        self.mode_timer += delta_time

        if self.vulnerable_timer > 0:
            self.vulnerable_timer -= delta_time
            if self.vulnerable_timer <= 0:
                self.vulnerable_timer = 0
                if self.mode == GhostMode.VULNERABLE:
                    self.mode = GhostMode.SCATTER

        if self.state == GhostState.IN_HOUSE:
            self.release_timer += delta_time
            if self.release_timer >= self.release_delay:
                self.state = GhostState.LEAVING_HOUSE
                if self.house_exit_target is None:
                    self.house_exit_target = self.find_house_exit(maze)

        self._update_ai(maze, pacman)

        if self.update_movement(delta_time, maze):
            self._perform_movement(maze)

    def _update_ai(self, maze: MazeProtocol, pacman: PacManProtocol) -> None:
        """Update AI target based on current mode and state."""
        if self.state == GhostState.IN_HOUSE:
            self._bob_in_house(maze)
            return

        elif self.state == GhostState.LEAVING_HOUSE:
            if self.house_exit_target is None:
                self.house_exit_target = self.find_house_exit(maze)

            if self.house_exit_target:
                self.target = self.house_exit_target

                current_x, current_y = self.position.x, self.position.y
                exit_x, exit_y = self.house_exit_target.x, self.house_exit_target.y

                at_target: bool = (abs(current_x - exit_x) <= 1 and
                                   abs(current_y - exit_y) <= 1)
                not_in_house: bool = (not maze.is_ghost_house(current_x, current_y) and
                                      not maze.is_ghost_door(current_x, current_y))

                if at_target or not_in_house:
                    self.state = GhostState.ACTIVE
                    self.house_exit_target = None
                    self.set_scatter_target_for_maze(maze)

        elif self.state == GhostState.ACTIVE:
            if self.mode == GhostMode.SCATTER:
                self.target = self.scatter_target
            elif self.mode == GhostMode.CHASE:
                chase_target = self._get_chase_target(pacman)
                self.target = chase_target
            elif self.mode == GhostMode.VULNERABLE:
                self._flee_from_pacman(maze, pacman)
            elif self.mode == GhostMode.EATEN:
                self.state = GhostState.RETURNING
                self._init_return_path(maze)

        elif self.state == GhostState.RETURNING:
            self._update_returning(maze)

    def _init_return_path(self, maze: MazeProtocol) -> None:
        """Initialize the path for returning to ghost house."""
        entrance: Position | None = self.find_house_entrance(maze)
        if entrance:
            self.path_target = entrance
            self.return_path = self._find_path_to_target(maze, entrance)
            self.target = entrance
        else:
            self.target = Position(self.start_position.x, self.start_position.y)
            self.return_path = []

    def _update_returning(self, maze: MazeProtocol) -> None:
        """Update AI when returning to ghost house."""
        current_x, current_y = self.position.x, self.position.y

        if maze.is_ghost_house(current_x, current_y):
            self.state = GhostState.IN_HOUSE
            self.mode = GhostMode.SCATTER
            self.release_timer = self.release_delay * 0.3
            self.return_path = []
            self.path_target = None
            return

        if maze.is_ghost_door(current_x, current_y):
            inside_target: Position = Position(self.start_position.x, self.start_position.y)
            self.return_path = self._find_path_to_target(maze, inside_target)
            self.target = inside_target
            return

        if not self.return_path:
            self._init_return_path(maze)

    def _bob_in_house(self, maze: MazeProtocol) -> None:
        """Simple up/down movement while in ghost house."""
        if self.direction == Direction.UP or self.direction == Direction.NONE:
            new_y: int = self.position.y - 1
            if not maze.is_walkable_for_ghost(self.position.x, new_y):
                self.direction = Direction.DOWN
            else:
                self.direction = Direction.UP
        else:
            new_y = self.position.y + 1
            if not maze.is_walkable_for_ghost(self.position.x, new_y):
                self.direction = Direction.UP
            else:
                self.direction = Direction.DOWN

        dx, dy = self.direction
        self.target = Position(self.position.x + dx, self.position.y + dy)

    def _flee_from_pacman(self, maze: MazeProtocol, pacman: PacManProtocol) -> None:
        """Choose a direction away from Pac-Man when vulnerable."""
        pac_pos = pacman.get_position()
        px, py = pac_pos.x, pac_pos.y

        best_distance: float = -1
        best_target: Position | None = None

        for direction in Direction.all_directions():
            dx, dy = direction
            new_x: int = self.position.x + dx * 3
            new_y: int = self.position.y + dy * 3

            distance: float = ((new_x - px) ** 2 + (new_y - py) ** 2) ** 0.5

            if distance > best_distance:
                check_x: int = self.position.x + dx
                check_y: int = self.position.y + dy
                if maze.is_walkable_for_ghost(check_x, check_y):
                    if not maze.is_ghost_house(check_x, check_y):
                        best_distance = distance
                        best_target = Position(new_x, new_y)

        if best_target:
            self.target = best_target
        else:
            self._choose_random_target(maze)

    def _get_chase_target(self, pacman: PacManProtocol) -> Position:
        """Get the target position for chase mode. Override in subclasses."""
        return pacman.get_position()

    def _choose_random_target(self, maze: MazeProtocol) -> None:
        """Choose a random direction when needed."""
        directions = Direction.all_directions()
        random.shuffle(directions)

        for direction in directions:
            dx, dy = direction
            new_x: int = self.position.x + dx
            new_y: int = self.position.y + dy
            if maze.is_walkable_for_ghost(new_x, new_y):
                if not maze.is_ghost_house(new_x, new_y):
                    self.target = Position(new_x, new_y)
                    break

    def _perform_movement(self, maze: MazeProtocol) -> None:
        """Execute movement towards target."""
        if self.state == GhostState.RETURNING and self.return_path:
            path_direction = self._get_next_path_direction(maze)
            if path_direction:
                dx, dy = path_direction
                new_x: int = self.position.x + dx
                new_y: int = self.position.y + dy

                if maze.is_walkable_for_ghost(new_x, new_y):
                    self.direction = path_direction
                    self.position = Position(new_x, new_y)
                    return

        best_direction: DirectionType = self._get_best_direction(maze)

        if best_direction != Direction.NONE:
            self.direction = best_direction
            dx, dy = best_direction
            new_x = self.position.x + dx
            new_y = self.position.y + dy

            can_move: bool = self._can_move_to_cell(maze, new_x, new_y)

            if can_move:
                self.position = Position(new_x, new_y)

    def _can_move_to_cell(self, maze: MazeProtocol, x: int, y: int) -> bool:
        """
        Check if ghost can move to the specified cell.

        Args:
            maze: The maze object
            x: Target x coordinate
            y: Target y coordinate

        Returns:
            True if the ghost can move to this cell
        """
        if not maze.is_walkable_for_ghost(x, y):
            return False

        if self.state == GhostState.RETURNING:
            return True

        if self.state == GhostState.ACTIVE:
            if maze.is_ghost_house(x, y) or maze.is_ghost_door(x, y):
                return False

        return True

    def _get_best_direction(self, maze: MazeProtocol) -> DirectionType:
        """
        Calculate the best direction to move towards target.

        Args:
            maze: The maze object

        Returns:
            The best direction tuple to move
        """
        if self.state == GhostState.IN_HOUSE:
            return self.direction

        reverse_direction: DirectionType = Direction.opposite(self.direction)

        can_reverse: bool = self._should_allow_reverse()

        possible_directions: list[tuple[DirectionType, float]] = []

        for direction in Direction.all_directions():
            if direction == reverse_direction and not can_reverse:
                continue

            dx, dy = direction
            new_x: int = self.position.x + dx
            new_y: int = self.position.y + dy

            if self._can_move_to_cell(maze, new_x, new_y):
                new_pos: Position = Position(new_x, new_y)
                distance: float = new_pos.distance_to(self.target)
                possible_directions.append((direction, distance))

        if not possible_directions:
            return reverse_direction

        possible_directions.sort(key=lambda x: x[1])

        return possible_directions[0][0]

    def _should_allow_reverse(self) -> bool:
        """
        Determine if the ghost should be allowed to reverse direction.

        Returns:
            True if reversing is allowed in current state
        """
        if self.state == GhostState.RETURNING:
            return True

        if self.state == GhostState.LEAVING_HOUSE:
            return True

        if self.mode == GhostMode.VULNERABLE:
            return True

        return False

    def set_mode(self, mode: GhostMode, duration: float = 0.0) -> None:
        """Set ghost mode and optional timer."""
        self.mode = mode
        self.mode_timer = 0.0

        if mode == GhostMode.VULNERABLE:
            self.vulnerable_timer = duration

    def make_vulnerable(self, duration: float) -> None:
        """Make ghost vulnerable (after power pellet)."""
        if self.mode != GhostMode.EATEN and self.state != GhostState.RETURNING:
            previous_mode = self.mode
            self.set_mode(GhostMode.VULNERABLE, duration)
            if self.state == GhostState.ACTIVE and previous_mode != GhostMode.VULNERABLE:
                self.direction = Direction.opposite(self.direction)

    def get_eaten(self) -> None:
        """Handle ghost being eaten by Pac-Man."""
        self.mode = GhostMode.EATEN
        self.state = GhostState.RETURNING
        self.vulnerable_timer = 0.0
        self.return_path = []
        self.path_target = None

    def is_vulnerable(self) -> bool:
        """Check if ghost is vulnerable to Pac-Man."""
        return self.mode == GhostMode.VULNERABLE and self.vulnerable_timer > 0

    def is_dangerous(self) -> bool:
        """Check if ghost is dangerous to Pac-Man."""
        return (self.state == GhostState.ACTIVE and
                self.mode in (GhostMode.SCATTER, GhostMode.CHASE))

    def can_be_eaten(self) -> bool:
        """Check if this ghost can be eaten by Pac-Man right now."""
        return self.is_vulnerable() and self.state == GhostState.ACTIVE

    def get_sprite(self) -> str:
        """Get the sprite character for this ghost."""
        if self.mode == GhostMode.EATEN or self.state == GhostState.RETURNING:
            return Sprites.EATEN_GHOST
        elif self.mode == GhostMode.VULNERABLE:
            return Sprites.VULNERABLE_GHOST
        else:
            return Sprites.GHOST

    def get_color(self) -> str:
        """Get the color for this ghost."""
        if self.mode == GhostMode.VULNERABLE:
            if self.vulnerable_timer < 2.0 and int(self.vulnerable_timer * 4) % 2 == 0:
                return Colors.WHITE
            return Colors.BLUE
        elif self.mode == GhostMode.EATEN or self.state == GhostState.RETURNING:
            return Colors.WHITE
        else:
            return self.color


class Blinky(Ghost):
    """Red ghost - aggressive chaser, first to leave house."""

    def __init__(self, start_x: int, start_y: int) -> None:
        super().__init__(start_x, start_y, Colors.RED, "Blinky")
        self.release_delay = 0.0

    def set_scatter_target_for_maze(self, maze: MazeProtocol) -> None:
        """Blinky scatters to top-right corner."""
        self.scatter_target = Position(maze.width - 2, 1)

    def _get_chase_target(self, pacman: PacManProtocol) -> Position:
        """Blinky directly targets Pac-Man."""
        return pacman.get_position()


class Pinky(Ghost):
    """Pink ghost - ambusher, targets ahead of Pac-Man."""

    def __init__(self, start_x: int, start_y: int) -> None:
        super().__init__(start_x, start_y, Colors.PINK, "Pinky")
        self.release_delay = 3.0

    def set_scatter_target_for_maze(self, maze: MazeProtocol) -> None:
        """Pinky scatters to top-left corner."""
        self.scatter_target = Position(1, 1)

    def _get_chase_target(self, pacman: PacManProtocol) -> Position:
        """Pinky targets 4 spaces ahead of Pac-Man."""
        pac_pos = pacman.get_position()
        dx, dy = pacman.direction

        target_x: int = pac_pos.x + dx * 4
        target_y: int = pac_pos.y + dy * 4

        return Position(target_x, target_y)


class Inky(Ghost):
    """Cyan ghost - uses Blinky's position for complex targeting."""

    def __init__(self, start_x: int, start_y: int, blinky: Blinky | None = None) -> None:
        super().__init__(start_x, start_y, Colors.CYAN, "Inky")
        self.release_delay = 6.0
        self.blinky: Blinky | None = blinky

    def set_scatter_target_for_maze(self, maze: MazeProtocol) -> None:
        """Inky scatters to bottom-right corner."""
        self.scatter_target = Position(maze.width - 2, maze.height - 2)

    def _get_chase_target(self, pacman: PacManProtocol) -> Position:
        """Inky uses complex targeting based on Pac-Man and Blinky."""
        pac_pos = pacman.get_position()
        dx, dy = pacman.direction

        intermediate_x: int = pac_pos.x + dx * 2
        intermediate_y: int = pac_pos.y + dy * 2

        if self.blinky:
            blinky_pos = self.blinky.get_position()
            target_x: int = intermediate_x + (intermediate_x - blinky_pos.x)
            target_y: int = intermediate_y + (intermediate_y - blinky_pos.y)
            return Position(target_x, target_y)

        return Position(intermediate_x, intermediate_y)


class Clyde(Ghost):
    """Orange ghost - shy, runs away when close to Pac-Man."""

    def __init__(self, start_x: int, start_y: int) -> None:
        super().__init__(start_x, start_y, Colors.ORANGE, "Clyde")
        self.release_delay = 9.0
        self.shy_distance: int = 8

    def set_scatter_target_for_maze(self, maze: MazeProtocol) -> None:
        """Clyde scatters to bottom-left corner."""
        self.scatter_target = Position(1, maze.height - 2)

    def _get_chase_target(self, pacman: PacManProtocol) -> Position:
        """Clyde chases when far, scatters when close."""
        pac_pos = pacman.get_position()
        distance: float = self.position.distance_to(pac_pos)

        if distance > self.shy_distance:
            return pac_pos
        else:
            return self.scatter_target
