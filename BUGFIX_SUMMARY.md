# Bugfix: Arrow Key ESC Sequence Handling

## Issue Identified
When pressing arrow keys, the game would immediately quit. This was caused by arrow keys sending ANSI escape sequences that begin with ESC (`\x1b`), which was being misinterpreted as the quit command.

## Root Cause
Arrow keys in terminals send multi-character sequences:
- Up Arrow: `ESC [ A`
- Down Arrow: `ESC [ B`
- Right Arrow: `ESC [ C`
- Left Arrow: `ESC [ D`

The input handler was correctly attempting to parse these sequences, but had a flaw: when the full sequence wasn't immediately available or couldn't be parsed, it would return `Keys.ESCAPE`, which triggered the quit command.

## Solution Implemented

### 1. Improved Escape Sequence Parsing
- Enhanced the logic in `input_handler.py` to properly validate complete arrow key sequences
- Changed behavior for incomplete sequences: now returns `None` instead of `ESC`
- This prevents false quit triggers when arrow key sequences arrive

### 2. Dual Quit Key Support
- Added 'Q' as the primary quit key
- Kept ESC as a backup quit method
- Updated all UI text to show "Q or ESC to quit"

### 3. Key Changes in Code

**Before:**
```python
if ch == '\x1b':
    # ... parse attempt ...
    return Keys.ESCAPE  # This was the problem!
```

**After:**
```python
if ch == '\x1b':
    # Check for arrow key sequence
    if select.select([sys.stdin], [], [], 0.1) != ([], [], []):
        ch2 = sys.stdin.read(1)
        if ch2 == '[':
            if select.select([sys.stdin], [], [], 0.1) != ([], [], []):
                ch3 = sys.stdin.read(1)
                if ch3 in arrow_keys:
                    return arrow_keys[ch3]
            # Incomplete sequence - return None instead of ESC
            return None
        else:
            # ESC followed by non-bracket - return None
            return None
    # Pure ESC press with nothing following
    return Keys.ESCAPE
```

## Testing
- Added new test: `test_arrow_keys_distinct_from_escape()`
- Verifies arrow keys don't return ESC
- All 25 tests passing

## User Impact
- Arrow keys now work correctly without quitting the game
- Players have two convenient ways to quit (Q or ESC)
- More intuitive controls matching common game conventions

## Files Modified
- `src/input_handler.py` - Fixed escape sequence parsing logic
- `src/game_engine.py` - Updated UI text for both menu and game over screens
- `README.md` - Updated controls documentation
- `tests/test_input_handler.py` - Added test for arrow key/ESC distinction

## Verification
Tested with multiple key combinations:
- ✅ Arrow keys (Up, Down, Left, Right) - work correctly
- ✅ WASD keys - work correctly
- ✅ Q key - quits as expected
- ✅ ESC key alone - quits as expected
- ✅ Space key - pauses/resumes

Bug is now resolved and the game is ready for Phase 2 development!
