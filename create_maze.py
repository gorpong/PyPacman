#!/usr/bin/env python
"""Create a properly sized and connected maze."""

# Create a simple but large connected maze
maze_lines = []

# Top border
maze_lines.append("#" * 78)

# Row 1 - top corridor with power pellets
maze_lines.append("#o" + "." * 74 + "o#")

# Rows 2-3 - upper section with walls
maze_lines.append("#.####.##########.######################.##########.####.#")
maze_lines.append("#.####.##########.######################.##########.####.#")

# Row 4 - horizontal corridor
maze_lines.append("#" + "." * 76 + "#")

# Rows 5-6 - middle upper walls
maze_lines.append("#.########.####.##.################.##.####.########.#")
maze_lines.append("#.########.####.##.################.##.####.########.#")

# Row 7 - corridor
maze_lines.append("#" + "." * 19 + "##" + "." * 16 + "##" + "." * 16 + "##" + "." * 19 + "#")

# Rows 8-9 - middle walls
maze_lines.append("########.########.##.##############.##.##.########.########")
maze_lines.append("########.########.##.##############.##.##.########.########")

# Rows 10-11 - ghost house area
maze_lines.append("#" + "." * 17 + "##" + "." * 16 + "##" + "." * 16 + "##" + "." * 17 + "#")
maze_lines.append("#.#####.#####.##.############## GG ##############.##.#####.#####.#")

# Rows 12-13 - ghost house
maze_lines.append("#.#####.#####.##.##              ##              ##.##.#####.#####.#")
maze_lines.append("#" + "." * 13 + "##" + "." * 2 + "##              ##              ##" + "." * 2 + "##" + "." * 13 + "#")

# Rows 14-15 - lower middle walls
maze_lines.append("#.###########.##.##  ##########  ##  ##########  ##.##.###########.#")
maze_lines.append("#.###########.##.##  ##########  ##  ##########  ##.##.###########.#")

# Row 16 - power pellet row
maze_lines.append("#o" + "." * 18 + "##" + "." * 34 + "##" + "." * 18 + "o#")

# Row 17 - bottom section
maze_lines.append("#.##################.######################.##################.#")

# Row 18 - bottom corridor
maze_lines.append("#" + "." * 76 + "#")

# Bottom border
maze_lines.append("#" * 78)

# Print the maze
for line in maze_lines:
    print(f'    "{line}",')
    
print(f"\nMaze dimensions: {len(maze_lines[0])} x {len(maze_lines)}")
