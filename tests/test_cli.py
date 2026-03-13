"""Tests for command-line argument parsing."""

import unittest
from unittest.mock import patch
import sys

# We'll import these once they exist
# from PyPacman.main import parse_args
# from PyPacman.data.levels import get_available_levels


class TestGetAvailableLevels(unittest.TestCase):
    """Tests for get_available_levels function."""

    def test_returns_list(self):
        """Test that get_available_levels returns a list."""
        from PyPacman.data.levels import get_available_levels
        result = get_available_levels()
        self.assertIsInstance(result, list)

    def test_contains_numeric_levels(self):
        """Test that numeric levels are included."""
        from PyPacman.data.levels import get_available_levels
        result = get_available_levels()
        self.assertIn(1, result)
        self.assertIn(2, result)
        self.assertIn(3, result)
        self.assertIn(4, result)

    def test_contains_named_levels(self):
        """Test that named levels are included."""
        from PyPacman.data.levels import get_available_levels
        result = get_available_levels()
        self.assertIn('test', result)
        self.assertIn('mini', result)

    def test_returns_all_levels_from_dict(self):
        """Test that all levels from LEVELS dict are returned."""
        from PyPacman.data.levels import get_available_levels, LEVELS
        result = get_available_levels()
        self.assertEqual(set(result), set(LEVELS.keys()))


class TestParseArgs(unittest.TestCase):
    """Tests for argument parsing."""

    def test_no_args_returns_defaults(self):
        """Test that no arguments returns default values."""
        from PyPacman.main import parse_args
        args = parse_args([])
        self.assertIsNone(args.level)
        self.assertIsNone(args.ghost_speed)
        self.assertFalse(args.list_levels)

    def test_level_long_form_with_string(self):
        """Test --level with string value."""
        from PyPacman.main import parse_args
        args = parse_args(['--level', 'test'])
        self.assertEqual(args.level, 'test')

    def test_level_short_form_with_string(self):
        """Test -l with string value."""
        from PyPacman.main import parse_args
        args = parse_args(['-l', 'mini'])
        self.assertEqual(args.level, 'mini')

    def test_level_with_numeric_string(self):
        """Test --level with numeric string converts to int."""
        from PyPacman.main import parse_args
        args = parse_args(['--level', '1'])
        self.assertEqual(args.level, 1)

    def test_level_with_larger_numeric(self):
        """Test --level with larger number."""
        from PyPacman.main import parse_args
        args = parse_args(['--level', '3'])
        self.assertEqual(args.level, 3)

    def test_level_invalid_name_exits(self):
        """Test --level with invalid name causes exit."""
        from PyPacman.main import parse_args
        with self.assertRaises(SystemExit):
            parse_args(['--level', 'nonexistent'])

    def test_level_invalid_number_exits(self):
        """Test --level with invalid number causes exit."""
        from PyPacman.main import parse_args
        with self.assertRaises(SystemExit):
            parse_args(['--level', '99'])

    def test_ghost_speed_long_form(self):
        """Test --ghost-speed with float value."""
        from PyPacman.main import parse_args
        args = parse_args(['--ghost-speed', '0.5'])
        self.assertEqual(args.ghost_speed, 0.5)

    def test_ghost_speed_short_form(self):
        """Test -g with float value."""
        from PyPacman.main import parse_args
        args = parse_args(['-g', '0.25'])
        self.assertEqual(args.ghost_speed, 0.25)

    def test_ghost_speed_one_point_zero(self):
        """Test ghost speed of 1.0 (normal speed)."""
        from PyPacman.main import parse_args
        args = parse_args(['--ghost-speed', '1.0'])
        self.assertEqual(args.ghost_speed, 1.0)

    def test_ghost_speed_max_value(self):
        """Test ghost speed at maximum allowed value."""
        from PyPacman.main import parse_args
        args = parse_args(['--ghost-speed', '2.0'])
        self.assertEqual(args.ghost_speed, 2.0)

    def test_ghost_speed_min_value(self):
        """Test ghost speed at minimum allowed value."""
        from PyPacman.main import parse_args
        args = parse_args(['--ghost-speed', '0.1'])
        self.assertEqual(args.ghost_speed, 0.1)

    def test_ghost_speed_zero_exits(self):
        """Test --ghost-speed with zero causes exit."""
        from PyPacman.main import parse_args
        with self.assertRaises(SystemExit):
            parse_args(['--ghost-speed', '0'])

    def test_ghost_speed_negative_exits(self):
        """Test --ghost-speed with negative value causes exit."""
        from PyPacman.main import parse_args
        with self.assertRaises(SystemExit):
            parse_args(['--ghost-speed', '-0.5'])

    def test_ghost_speed_too_high_exits(self):
        """Test --ghost-speed above maximum causes exit."""
        from PyPacman.main import parse_args
        with self.assertRaises(SystemExit):
            parse_args(['--ghost-speed', '3.0'])

    def test_ghost_speed_invalid_format_exits(self):
        """Test --ghost-speed with non-numeric value causes exit."""
        from PyPacman.main import parse_args
        with self.assertRaises(SystemExit):
            parse_args(['--ghost-speed', 'slow'])

    def test_list_levels_long_form(self):
        """Test --list-levels flag."""
        from PyPacman.main import parse_args
        args = parse_args(['--list-levels'])
        self.assertTrue(args.list_levels)

    def test_list_levels_short_form(self):
        """Test -L flag for list levels."""
        from PyPacman.main import parse_args
        args = parse_args(['-L'])
        self.assertTrue(args.list_levels)

    def test_combined_level_and_ghost_speed(self):
        """Test combining --level and --ghost-speed."""
        from PyPacman.main import parse_args
        args = parse_args(['--level', 'test', '--ghost-speed', '0.3'])
        self.assertEqual(args.level, 'test')
        self.assertEqual(args.ghost_speed, 0.3)

    def test_combined_short_forms(self):
        """Test combining -l and -g."""
        from PyPacman.main import parse_args
        args = parse_args(['-l', '2', '-g', '0.5'])
        self.assertEqual(args.level, 2)
        self.assertEqual(args.ghost_speed, 0.5)


class TestFormatLevelList(unittest.TestCase):
    """Tests for format_level_list function."""

    def test_returns_string(self):
        """Test that format_level_list returns a string."""
        from PyPacman.main import format_level_list
        result = format_level_list()
        self.assertIsInstance(result, str)

    def test_contains_level_numbers(self):
        """Test that output contains level numbers."""
        from PyPacman.main import format_level_list
        result = format_level_list()
        self.assertIn('1', result)
        self.assertIn('2', result)
        self.assertIn('3', result)
        self.assertIn('4', result)

    def test_contains_named_levels(self):
        """Test that output contains named levels."""
        from PyPacman.main import format_level_list
        result = format_level_list()
        self.assertIn('test', result)
        self.assertIn('mini', result)

    def test_has_header(self):
        """Test that output has a header."""
        from PyPacman.main import format_level_list
        result = format_level_list()
        # Check for 'available' in lowercase since we're lowercasing the result
        self.assertIn('available', result.lower())


class TestGameEngineStartingLevel(unittest.TestCase):
    """Tests for GameEngine starting level parameter."""

    def setUp(self):
        """Set up test fixtures."""
        from PyPacman.ui.display import MockDisplay
        from PyPacman.ui.input_handler import MockInputHandler
        self.display = MockDisplay()
        self.input_handler = MockInputHandler()

    def test_default_starts_at_level_1(self):
        """Test that default GameEngine starts at level 1."""
        from PyPacman.core.game_engine import GameEngine
        game = GameEngine(self.display, self.input_handler)
        self.assertEqual(game.game_state.get_level(), 1)

    def test_starting_level_numeric(self):
        """Test starting at a specific numeric level."""
        from PyPacman.core.game_engine import GameEngine
        game = GameEngine(self.display, self.input_handler, starting_level=3)
        self.assertEqual(game.game_state.get_level(), 3)

    def test_starting_level_test(self):
        """Test starting at test level."""
        from PyPacman.core.game_engine import GameEngine
        from PyPacman.data.levels import LEVEL_TEST
        game = GameEngine(self.display, self.input_handler, starting_level='test')
        # Verify the maze dimensions match LEVEL_TEST
        self.assertEqual(game.maze.height, len(LEVEL_TEST))
        self.assertEqual(game.maze.width, len(LEVEL_TEST[0]))

    def test_starting_level_mini(self):
        """Test starting at mini level."""
        from PyPacman.core.game_engine import GameEngine
        from PyPacman.data.levels import LEVEL_MINI
        game = GameEngine(self.display, self.input_handler, starting_level='mini')
        # Verify the maze dimensions match LEVEL_MINI
        self.assertEqual(game.maze.height, len(LEVEL_MINI))
        self.assertEqual(game.maze.width, len(LEVEL_MINI[0]))

    def test_starting_level_2(self):
        """Test starting at level 2."""
        from PyPacman.core.game_engine import GameEngine
        from PyPacman.data.levels import LEVEL_2
        game = GameEngine(self.display, self.input_handler, starting_level=2)
        self.assertEqual(game.game_state.get_level(), 2)
        self.assertEqual(game.maze.height, len(LEVEL_2))

    def test_starting_level_preserved_after_reset(self):
        """Test that starting level is used after game reset."""
        from PyPacman.core.game_engine import GameEngine
        game = GameEngine(self.display, self.input_handler, starting_level=3)

        # Simulate playing and resetting
        game.game_state.level = 5  # Pretend we advanced
        game.reset_game()

        # Should reset to starting level, not level 1
        self.assertEqual(game.game_state.get_level(), 3)

    def test_game_state_starting_level_parameter(self):
        """Test GameState accepts starting_level parameter."""
        from PyPacman.core.game_state import GameState
        state = GameState(starting_lives=3, starting_level=4)
        self.assertEqual(state.get_level(), 4)

    def test_game_state_reset_uses_starting_level(self):
        """Test GameState reset returns to starting level."""
        from PyPacman.core.game_state import GameState
        state = GameState(starting_lives=3, starting_level=2)
        state.level = 5  # Advance the level
        state.reset()
        self.assertEqual(state.get_level(), 2)

    def test_game_state_default_starting_level(self):
        """Test GameState defaults to level 1."""
        from PyPacman.core.game_state import GameState
        state = GameState(starting_lives=3)
        self.assertEqual(state.get_level(), 1)


class TestMainLevelIntegration(unittest.TestCase):
    """Tests for main() passing level to GameEngine."""

    def test_parse_args_level_available_for_engine(self):
        """Test that parsed level arg can be passed to GameEngine."""
        from PyPacman.main import parse_args
        from PyPacman.core.game_engine import GameEngine
        from PyPacman.ui.display import MockDisplay
        from PyPacman.ui.input_handler import MockInputHandler

        args = parse_args(['-l', 'test'])

        display = MockDisplay()
        input_handler = MockInputHandler()
        game = GameEngine(display, input_handler, starting_level=args.level)

        # Should have loaded the test level
        from PyPacman.data.levels import LEVEL_TEST
        self.assertEqual(game.maze.height, len(LEVEL_TEST))

    def test_main_function_passes_level_to_engine(self):
        """Test that main() actually passes level argument to GameEngine."""
        import PyPacman.main as main_module
        from unittest.mock import patch, MagicMock

        # Mock GameEngine to capture what arguments it receives
        with patch.object(main_module, 'GameEngine') as mock_engine:
            mock_instance = MagicMock()
            mock_engine.return_value = mock_instance

            # Simulate calling main with -l test
            with patch.object(main_module, 'parse_args') as mock_parse:
                mock_args = MagicMock()
                mock_args.list_levels = False
                mock_args.level = 'test'
                mock_args.ghost_speed = None
                mock_parse.return_value = mock_args

                # Call main, but mock start() to prevent actual game loop
                mock_instance.start = MagicMock()

                try:
                    main_module.main()
                except SystemExit:
                    pass  # Ignore any sys.exit calls

                # Verify GameEngine was called with starting_level='test'
                mock_engine.assert_called_once()
                call_kwargs = mock_engine.call_args[1]
                self.assertEqual(call_kwargs.get('starting_level'), 'test')

class TestGhostSpeedMultiplier(unittest.TestCase):
    """Tests for ghost speed multiplier functionality."""

    def setUp(self):
        """Set up test fixtures."""
        from PyPacman.ui.display import MockDisplay
        from PyPacman.ui.input_handler import MockInputHandler
        self.display = MockDisplay()
        self.input_handler = MockInputHandler()

    def test_game_engine_accepts_ghost_speed_parameter(self):
        """Test that GameEngine accepts ghost_speed_multiplier parameter."""
        from PyPacman.core.game_engine import GameEngine
        # Should not raise an error
        game = GameEngine(
            self.display,
            self.input_handler,
            ghost_speed_multiplier=0.5
        )
        self.assertIsNotNone(game)

    def test_game_engine_stores_ghost_speed_multiplier(self):
        """Test that GameEngine stores the ghost speed multiplier."""
        from PyPacman.core.game_engine import GameEngine
        game = GameEngine(
            self.display,
            self.input_handler,
            ghost_speed_multiplier=0.5
        )
        self.assertEqual(game.ghost_speed_multiplier, 0.5)

    def test_game_engine_default_ghost_speed_is_none(self):
        """Test that default ghost speed multiplier is None."""
        from PyPacman.core.game_engine import GameEngine
        game = GameEngine(self.display, self.input_handler)
        self.assertIsNone(game.ghost_speed_multiplier)

    def test_ghost_manager_accepts_speed_multiplier(self):
        """Test that GhostManager accepts speed_multiplier parameter."""
        from PyPacman.core.game_engine import GameEngine
        from PyPacman.entities.ghost_manager import GhostManager

        game = GameEngine(self.display, self.input_handler)
        # Should not raise an error
        manager = GhostManager(game.maze, speed_multiplier=0.5)
        self.assertIsNotNone(manager)

    def test_ghost_manager_stores_speed_multiplier(self):
        """Test that GhostManager stores the speed multiplier."""
        from PyPacman.core.game_engine import GameEngine
        from PyPacman.entities.ghost_manager import GhostManager

        game = GameEngine(self.display, self.input_handler)
        manager = GhostManager(game.maze, speed_multiplier=0.5)
        self.assertEqual(manager.speed_multiplier, 0.5)

    def test_ghost_manager_default_speed_multiplier(self):
        """Test that GhostManager defaults to 1.0 speed multiplier."""
        from PyPacman.core.game_engine import GameEngine
        from PyPacman.entities.ghost_manager import GhostManager

        game = GameEngine(self.display, self.input_handler)
        manager = GhostManager(game.maze)
        self.assertEqual(manager.speed_multiplier, 1.0)

    def test_ghost_accepts_speed_multiplier(self):
        """Test that Ghost accepts external speed multiplier."""
        from PyPacman.entities.ghost import Blinky
        ghost = Blinky(5, 5)
        ghost.set_speed_multiplier(0.5)
        self.assertEqual(ghost.external_speed_multiplier, 0.5)

    def test_ghost_default_speed_multiplier(self):
        """Test that Ghost defaults to 1.0 external speed multiplier."""
        from PyPacman.entities.ghost import Blinky
        ghost = Blinky(5, 5)
        self.assertEqual(ghost.external_speed_multiplier, 1.0)

    def test_ghost_speed_affected_by_multiplier(self):
        """Test that ghost movement speed is affected by multiplier."""
        from PyPacman.entities.ghost import Blinky

        ghost_normal = Blinky(5, 5)
        ghost_slow = Blinky(5, 5)
        ghost_slow.set_speed_multiplier(0.5)

        normal_speed = ghost_normal.get_current_speed()
        slow_speed = ghost_slow.get_current_speed()

        self.assertEqual(slow_speed, normal_speed * 0.5)

    def test_ghost_speed_multiplier_stacks_with_mode(self):
        """Test that external multiplier stacks with mode-based speed."""
        from PyPacman.entities.ghost import Blinky, GhostMode, GhostState

        ghost = Blinky(5, 5)
        ghost.state = GhostState.ACTIVE
        ghost.mode = GhostMode.VULNERABLE
        ghost.vulnerable_timer = 5.0

        # Get vulnerable speed without external multiplier
        base_vulnerable_speed = ghost.get_current_speed()

        # Apply external multiplier
        ghost.set_speed_multiplier(0.5)
        modified_speed = ghost.get_current_speed()

        # Should be half of the vulnerable speed
        self.assertEqual(modified_speed, base_vulnerable_speed * 0.5)

    def test_game_engine_passes_multiplier_to_ghost_manager(self):
        """Test that GameEngine passes speed multiplier to GhostManager."""
        from PyPacman.core.game_engine import GameEngine

        game = GameEngine(
            self.display,
            self.input_handler,
            ghost_speed_multiplier=0.25
        )

        self.assertEqual(game.ghost_manager.speed_multiplier, 0.25)

    def test_ghost_manager_applies_multiplier_to_all_ghosts(self):
        """Test that GhostManager applies multiplier to all ghosts."""
        from PyPacman.core.game_engine import GameEngine

        game = GameEngine(
            self.display,
            self.input_handler,
            ghost_speed_multiplier=0.3
        )

        for ghost in game.ghost_manager.ghosts:
            self.assertEqual(ghost.external_speed_multiplier, 0.3)

    def test_ghost_manager_reset_preserves_speed_multiplier(self):
        """Test that GhostManager reset preserves speed multiplier."""
        from PyPacman.core.game_engine import GameEngine

        game = GameEngine(
            self.display,
            self.input_handler,
            ghost_speed_multiplier=0.4
        )

        game.ghost_manager.reset()

        self.assertEqual(game.ghost_manager.speed_multiplier, 0.4)
        for ghost in game.ghost_manager.ghosts:
            self.assertEqual(ghost.external_speed_multiplier, 0.4)


class TestMainGhostSpeedIntegration(unittest.TestCase):
    """Tests for main() passing ghost speed to GameEngine."""

    def test_main_function_passes_ghost_speed_to_engine(self):
        """Test that main() actually passes ghost_speed argument to GameEngine."""
        import PyPacman.main as main_module
        from unittest.mock import patch, MagicMock

        with patch.object(main_module, 'GameEngine') as mock_engine:
            mock_instance = MagicMock()
            mock_engine.return_value = mock_instance

            with patch.object(main_module, 'parse_args') as mock_parse:
                mock_args = MagicMock()
                mock_args.list_levels = False
                mock_args.level = None
                mock_args.ghost_speed = 0.5
                mock_parse.return_value = mock_args

                mock_instance.start = MagicMock()

                try:
                    main_module.main()
                except SystemExit:
                    pass

                mock_engine.assert_called_once()
                call_kwargs = mock_engine.call_args[1]
                self.assertEqual(call_kwargs.get('ghost_speed_multiplier'), 0.5)

    def test_main_passes_both_level_and_ghost_speed(self):
        """Test that main() passes both level and ghost_speed to GameEngine."""
        import PyPacman.main as main_module
        from unittest.mock import patch, MagicMock

        with patch.object(main_module, 'GameEngine') as mock_engine:
            mock_instance = MagicMock()
            mock_engine.return_value = mock_instance

            with patch.object(main_module, 'parse_args') as mock_parse:
                mock_args = MagicMock()
                mock_args.list_levels = False
                mock_args.level = 'test'
                mock_args.ghost_speed = 0.25
                mock_parse.return_value = mock_args

                mock_instance.start = MagicMock()

                try:
                    main_module.main()
                except SystemExit:
                    pass

                mock_engine.assert_called_once()
                call_kwargs = mock_engine.call_args[1]
                self.assertEqual(call_kwargs.get('starting_level'), 'test')
                self.assertEqual(call_kwargs.get('ghost_speed_multiplier'), 0.25)

class TestGhostScoringIntegration(unittest.TestCase):
    """Integration tests for ghost scoring during gameplay."""

    def setUp(self):
        """Set up test fixtures."""
        from PyPacman.ui.display import MockDisplay
        from PyPacman.ui.input_handler import MockInputHandler
        self.display = MockDisplay()
        self.input_handler = MockInputHandler()

    def test_eating_vulnerable_ghost_adds_score(self):
        """Test that eating a vulnerable ghost actually adds to score."""
        from PyPacman.core.game_engine import GameEngine
        from PyPacman.entities.ghost import GhostMode, GhostState

        game = GameEngine(self.display, self.input_handler, starting_level='test')
        initial_score = game.scoring.get_score()

        # Make a ghost vulnerable and position it at Pac-Man's location
        ghost = game.ghost_manager.ghosts[0]
        ghost.state = GhostState.ACTIVE
        ghost.make_vulnerable(10.0)

        # Move ghost to Pac-Man's position
        pac_pos = game.pacman.get_position()
        ghost.position = pac_pos

        # Update previous positions so collision detection works
        game.ghost_manager._update_previous_positions()
        game.previous_pacman_pos = pac_pos

        # Check collision - this should trigger scoring
        game._check_ghost_collisions()

        # Score should have increased by 200
        self.assertEqual(game.scoring.get_score(), initial_score + 200)

    def test_eating_multiple_ghosts_progressive_scoring(self):
        """Test that eating multiple ghosts gives progressive scores."""
        from PyPacman.core.game_engine import GameEngine
        from PyPacman.entities.ghost import GhostState
        from PyPacman.core.types import Position

        game = GameEngine(self.display, self.input_handler, starting_level='test')

        # Make all ghosts vulnerable
        game.ghost_manager.make_all_vulnerable()

        pac_pos = game.pacman.get_position()
        game.previous_pacman_pos = pac_pos

        expected_scores = [200, 400, 800, 1600]
        running_total = 0

        for i, expected in enumerate(expected_scores):
            # Position next ghost at Pac-Man
            ghost = game.ghost_manager.ghosts[i]
            ghost.state = GhostState.ACTIVE
            ghost.position = Position(pac_pos.x, pac_pos.y)

            game.ghost_manager._update_previous_positions()

            score_before = game.scoring.get_score()
            game._check_ghost_collisions()
            score_after = game.scoring.get_score()

            points_earned = score_after - score_before
            self.assertEqual(points_earned, expected,
                           f"Ghost {i+1} should give {expected} points, got {points_earned}")

            running_total += expected

        self.assertEqual(game.scoring.get_score(), running_total)

    def test_score_popup_shows_correct_points(self):
        """Test that score popup displays correct points."""
        from PyPacman.core.game_engine import GameEngine
        from PyPacman.entities.ghost import GhostState

        game = GameEngine(self.display, self.input_handler, starting_level='test')

        # Make first ghost vulnerable
        ghost = game.ghost_manager.ghosts[0]
        ghost.state = GhostState.ACTIVE
        ghost.make_vulnerable(10.0)

        # Position at Pac-Man
        pac_pos = game.pacman.get_position()
        ghost.position = pac_pos
        game.ghost_manager._update_previous_positions()
        game.previous_pacman_pos = pac_pos

        # Trigger collision
        game._check_ghost_collisions()

        # Check popup
        self.assertIsNotNone(game.score_popup)
        popup_text, _, _, _ = game.score_popup
        self.assertEqual(popup_text, "+200")


if __name__ == '__main__':
    unittest.main()
