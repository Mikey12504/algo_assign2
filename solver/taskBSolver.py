# -------------------------------------------------------------------
# PLEASE UPDATE THIS FILE.
# Brute force maze solver for all entrance, exit pairs
#
# __author__ = Nguyen Ba Duc Manh
# __copyright__ = 'Copyright 2024, RMIT University'
# -------------------------------------------------------------------


from maze.util import Coordinates
from maze.maze import Maze
from typing import List, Dict

class bruteForceSolver:
   
    def __init__(self):
        self.best_solution = None               # To store the best non-overlapping paths
        self.min_total_distance = float('inf')  # Track the minimum total distance
        self.all_solved = False                 # Flag to check if a solution was found
        self.entrance_exit_paths = {}           # Dictionary to store the entrance-exit paths
        self.cellsExplored = 0                  # Counter for how many cells were explored during solving

    def solveMaze(self, maze: Maze, entrances: List[Coordinates], exits: List[Coordinates]):
        """
        Solves the maze for all entrance-exit pairs ensuring no overlap in paths.
        Tries all combinations of valid paths between entrance and exit pairs.
        """
        # Ensure that the number of entrances equals the number of exits
        if len(entrances) != len(exits):
            print("Error: Number of entrances and exits must be equal.")
            return False

        # Initialize used cells tracking to prevent overlapping paths
        used_cells = set()

        # Reset the number of explored cells at the beginning
        self.cellsExplored = 0

        # Try to find all valid paths for each entrance-exit pair
        all_paths_for_pairs = []
        for entrance, exit in zip(entrances, exits):
            paths = self._solveSinglePair(maze, entrance, exit, used_cells)
            if not paths:
                print(f"No valid non-overlapping path found for entrance ({entrance.getRow()},{entrance.getCol()}) and exit ({exit.getRow()},{exit.getCol()}).")
                return False
            for path in paths:
                distance = path[1]
                print(f"Solution found with total distance: {distance}")
            print(f"For pair ({entrance.getRow()},{entrance.getCol()}) and ({exit.getRow()},{exit.getCol()})")
            all_paths_for_pairs.append(paths)

        # Now we need to explore all combinations of these paths
        # I use itertools.product to generate all combinations of paths for each pair

        from itertools import product
        best_distance = float('inf')
        best_combination = None

        for combination in product(*all_paths_for_pairs):
            temp_used_cells = set()
            total_distance = 0
            valid = True

            for path, distance in combination:
                # Check if this path overlaps with other paths
                if any(cell in temp_used_cells for cell in path):
                    print(f"No valid non-overlapping paths found among entrance-exit pairs.")
                    valid = False
                    break
                temp_used_cells.update(path)
                total_distance += distance

            if valid and total_distance < best_distance:
                best_distance = total_distance
                best_combination = combination

        if best_combination:
            self.best_solution = best_combination
            self.min_total_distance = best_distance
            self.entrance_exit_paths = {(entrances[i], exits[i]): path for i, (path, distance) in enumerate(best_combination)}
            print(f"New best solution found with total distance: {self.min_total_distance}")
            self.all_solved = True
        else:
            self.all_solved = False

        return self.all_solved


    def _solveSinglePair(self, maze: Maze, entrance: Coordinates, exit: Coordinates, used_cells: set):
        """
        Find all possible non-overlapping paths between entrance and exit using DFS.
        Ensures that no cells in 'used_cells' are part of the path.
        Returns a list of all valid paths and their distances.
        """
        def dfs(current_cell, target_cell, path, distance):
            if current_cell == target_cell:
                # Found a valid path
                all_paths.append((path.copy(), distance))
                return
            
            # Explore neighbors of current cell
            for neighbor in maze.neighbours(current_cell):
                if neighbor not in used_cells and not maze.hasWall(current_cell, neighbor) and neighbor not in path:
                    path.append(neighbor)
                    new_distance = distance + abs(current_cell.getWeight() - neighbor.getWeight())
                    dfs(neighbor, target_cell, path, new_distance)
                    path.pop()  # Backtrack

        all_paths = []
        # Start DFS from entrance to exit
        dfs(entrance, exit, [entrance], 0)

        # If no valid path found, return None
        if not all_paths:
            return None, 0

        # Return all valid paths
        return all_paths


    def getSolverPath(self) -> Dict[tuple, List[Coordinates]]:
        """
        Retrieve the entrance-exit paths. 
        Returns a dictionary with keys as (entrance, exit) tuples and values as the paths.
        """
        return self.entrance_exit_paths