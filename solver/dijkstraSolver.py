# -------------------------------------------------------------------
# PLEASE UPDATE THIS FILE.
# Dijkstra's maze solver.
#
# __author__ =  Nguyen Ba Duc Manh
# __copyright__ = 'Copyright 2024, RMIT University'
# -------------------------------------------------------------------

from maze.util import Coordinates
from maze.maze import Maze
from typing import List, Dict
import heapq
from collections import defaultdict
import itertools

class DijkstraSolver:
    
    def __init__(self):
        # self.m_solverPath: Path from entrance to exit
        self.m_solverPath: List[Coordinates] = []
        # self.m_cellsExplored: Number of cells explored during solving
        self.m_cellsExplored = 0
        # self.m_entranceUsed: Entrance used to enter maze
        self.m_entranceUsed = None
        # self.m_exitUsed: Exit found and used by solver
        self.m_exitUsed = None
        self.counter = itertools.count()  # A counter to ensure uniqueness
    
    def solveMaze(self, maze: Maze, entrance: Coordinates):
        # Priority queue for Dijkstra (min-heap)
        pq = []
        # Distances dictionary, initialized to infinity for all cells except the entrance
        distances: Dict[Coordinates, float] = defaultdict(lambda: float('inf'))
        predecessors: Dict[Coordinates, Coordinates] = {}
        
        # Initialize the entrance
        distances[entrance] = 0
        # Push the entrance with a tie-breaking counter
        heapq.heappush(pq, (0, next(self.counter), entrance))  # (distance, counter, cell)
        self.m_cellsExplored = 0

        while pq:
            # Get the cell with the smallest distance
            curr_distance, _, curr_cell = heapq.heappop(pq)

            # Check if we've reached an exit
            if curr_cell in maze.getExits():
                self.m_exitUsed = curr_cell
                self.m_entranceUsed = entrance
                break
            
            # Explore all unvisited neighbors
            for neighbor in maze.neighbours(curr_cell):
                if not maze.hasWall(curr_cell, neighbor):
                    new_distance = curr_distance + abs(curr_cell.getWeight() - neighbor.getWeight())
                    
                    if new_distance < distances[neighbor]:
                        distances[neighbor] = new_distance
                        predecessors[neighbor] = curr_cell
                        # Push neighbor with its distance and a tie-breaking counter
                        heapq.heappush(pq, (new_distance, next(self.counter), neighbor))

            self.m_cellsExplored += 1

        self._reconstructPath(predecessors, entrance, self.m_exitUsed)

    def _reconstructPath(self, predecessors: Dict[Coordinates, Coordinates], start: Coordinates, end: Coordinates):
        """
        Reconstruct the path from start to end using the predecessors dictionary.
        """
        path = []
        curr_cell = end
        while curr_cell is not None:
            path.append(curr_cell)
            curr_cell = predecessors.get(curr_cell)

        # Reverse the path to get it from entrance to exit
        self.m_solverPath = path[::-1]
        self.m_entranceUsed = start
        self.m_exitUsed = end
                    

	
