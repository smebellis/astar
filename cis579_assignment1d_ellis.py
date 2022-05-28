"""Ryan Ellis
CIS 579 Assignment 1
Student ID: 9023691"""

from cmath import inf
from queue import PriorityQueue
from itertools import permutations
from time import time


def timer_func(func):
    """A wrapper to print the time it took for a function to run in
    seconds.

    Args:
        func (_type_): A function to be timed.

    Returns:
        _type_: The time it took for the function to run.
    """
    # This function shows the execution time of
    # the function object passed
    def wrap_func(*args, **kwargs):
        t1 = time()
        result = func(*args, **kwargs)
        t2 = time()
        print(f"Function {func.__name__!r} executed in {(t2-t1):.4f}s")
        return result

    return wrap_func


class Node:
    def __init__(self):
        self.board = list()
        self.g_score = inf
        self.f_score = inf
        self.came_from = None

    def __eq__(self, other):
        return self.board == other.board

    def __lt__(self, other):
        return self.f_score < other.f_score

    def __hash__(self):
        return hash(self.board)

    def __str__(self):

        string = ""
        for row in self.board:
            for col in row:
                string += str(col) + " "
            string += "\n"

        return string

    def createStartBoard(self, board):
        """Start Board

        Parse a string representation of a board and return a Node

        Args:
            board (list): A list of strings representing the board

        Returns:
            result: Boolean: True if the board was parsed successfully, False otherwise
        """
        result = False
        grid = []
        rows = []

        for row in range(0, len(board)):
            for col in range(0, len(board[row])):
                rows.append(board[row][col])
                if len(rows) == 3:
                    grid.append(tuple(rows))
                    rows = []

        self.board = tuple(grid)
        result = True
        return result

    def currentPosition(self, x, y):
        """Square at a specific position

        Returns a square at a specific position, or None if there is no
        square at that position

        Args:
            x (int): x coordinate of the square
            y (int): y coordinate of the square

        Returns:
            _type_: board.Square: The square at the given position
        """
        if x < 0 or y < 0:
            return None

        return self.board[x][y]

    def distanceToNextNode(self, other):
        """Distance to another node

        Args:
            other (_type_): The other node

        Returns:
            _type_: int: The distance between the two nodes
        """
        return 0 if self == other else 1

    def createEndBoard(self):
        """Goal Node

        A board where all pieces have switched places

        Returns:
            goal: Node: The goal node
        """
        endBoard = Node()
        grid = [list(row) for row in self.board]

        for x in range(0, len(self.board)):
            for y in range(0, len(self.board[x])):
                square = self.board[x][y]
                if square == 1:
                    grid[x][y] = 2
                elif square == 2:
                    grid[x][y] = 1
                else:
                    continue

        endBoard.board = tuple([tuple(row) for row in grid])

        return endBoard

    def square_at(self, x: int, y: int):
        """Square at a specific position

        Returns a square at a specific position, or None if there is no
        square at that position

        Args:
            x (int): x coordinate of the square
            y (int): y coordinate of the square

        Returns:
            _type_: board.Square: The square at the given position

        Raises:
            IndexError: If the given position is out of bounds

        """
        if x < 0 or y < 0:
            return None
        try:
            return self.board[y][x]
        except IndexError:
            return None

    def getNeighbors(self):
        """Neighbours

        Get the neighbours of the current node

        Returns:
            _type_: list: A list of neighbours for this node

        """
        # All the possible moves a knight can make
        possible_moves = [
            p for p in permutations([-2, -1, 1, 2], 2) if abs(p[0] - p[1]) % 2
        ]
        neighbors = []

        for y in range(0, len(self.board)):
            for x in range(0, len(self.board[y])):
                square = self.board[y][x]
                if square != 0:
                    for p in possible_moves:
                        new_position = self.square_at(x + p[0], y + p[1])
                        if new_position == 0:
                            neighbour = Node()
                            grid = [list(row) for row in self.board]
                            grid[y + p[1]][x + p[0]] = square
                            grid[y][x] = new_position
                            neighbour.board = tuple([tuple(row) for row in grid])
                            if neighbour not in neighbors:
                                neighbors.append(neighbour)

        return neighbors

    def heuristics(self):
        """Heuristic Cost

        Calculate the heuristic cost to reach another node

        Args:
            other (_type_): The other node

        Returns:
            _type_: int: The heuristic cost to reach the other node

        """
        for x in range(0, len(self.board)):
            for y in range(0, len(self.board[x])):
                if self.board[x][y] == 1:
                    currentPosition = (x, y)
                    break
                elif self.board[x][y] == 2:
                    otherPosition = (x, y)
                    break
        try:
            cost = (
                abs(currentPosition[0] - otherPosition[0])
                + abs(currentPosition[1] - otherPosition[1])
            ) / 3
        except:
            cost = 1
        return cost


def reconstruct_path(node: Node):
    """Reconstruct Path

    Args:
        node (Node): The node to start from

    Returns:
        _type_: list: A list of nodes representing the path the algorithm chose
                to take to get to end goal.

    """

    path = [node]
    while node.came_from:
        node = node.came_from
        path.append(node)
    path.pop()
    path.reverse()
    return path


@timer_func
def a_star(start: Node, goal: Node):
    """A* Search

    A searching algorithm that is used to find the shortest path between
    an initial and a final point.

    Args:
        start (Node): The starting node to begin search
        goal (Node): The goal node node to end search

    Returns:
        _type_: list: A list of nodes representing the path
    """
    closed_set = set()
    open_set = PriorityQueue()
    open_set.put(start)

    start.g_score = 0
    start.f_score = start.heuristics()

    while not open_set.empty():
        current = open_set.get()

        # Check if we have reached the goal
        if current == goal:
            print(f"Number of nodes in closed set: {len(closed_set)}")
            return reconstruct_path(current)

        # Insert current node to closed set
        closed_set.add(current)

        # Get neighbors of current node
        for neighbor in current.getNeighbors():
            if neighbor in closed_set:
                continue

            # Calculate tentative g score
            g_score = current.g_score + current.distanceToNextNode(neighbor)

            # Check if the neighbor is already in the open set
            if neighbor not in open_set.queue:
                open_set.put(neighbor)
            else:
                for n in open_set.queue:
                    if n == neighbor:
                        neighbor = n
                        break

            # Check if the path to the neighbor is better
            if g_score >= neighbor.g_score:
                continue

            # Update neighbor's score
            neighbor.came_from = current
            neighbor.g_score = g_score
            neighbor.f_score = neighbor.g_score + neighbor.heuristics()

    # No path was found
    return None


@timer_func
def branchNBound(start: Node, goal: Node):
    """Branch and Bound Search

    Branch and Bound is a state space search method in which
    all the children of a node are generated before expanding
    any of its children.

    Args:
        start (Node): The starting node to begin search
        goal (Node): The goal node node to end search

    Returns:
        _type_: list: A list of nodes representing the path
    """
    open_set = []
    closed_set = set()

    open_set.append(start)

    while len(open_set) > 0:
        current = open_set[0]
        open_set.pop(0)

        if current == goal:
            print(f"Number of nodes in closed set: {len(closed_set)}")
            return reconstruct_path(current)

        closed_set.add(current)

        # Explore all the neighbors of the current node
        for neighbor in current.getNeighbors():

            # prevent duplicates from being added to the open set
            if neighbor in open_set:
                continue

            open_set.append(neighbor)
            neighbor.came_from = current

    # No path was found
    return None


def main():

    start = [[1, 0, 1], [0, 0, 0], [2, 0, 2]]

    node = Node()
    node.createStartBoard(start)

    print(f"Looking for solution...\nStart:\n{node}")
    path = a_star(node, node.createEndBoard())

    print("****************A STAR SEARCH****************\n\n")
    if path is None:
        print("No solution found")
    else:
        print(f"Solution found with {len(path)} moves:")
        for i in range(0, len(path)):

            print(f"Move {i + 1}:\n{path[i]}")

    print("****************Branch and Bound****************\n\n")
    node1 = Node()
    node1.createStartBoard(start)
    print(f"Looking for solution...\nStart:\n{node1}")

    path1 = branchNBound(node1, node1.createEndBoard())

    if path1 is None:
        print("No solution found")
    else:
        print(f"Solution found with {len(path1)} moves:")
        for i in range(0, len(path1)):
            print(f"Move {i + 1}:\n{path1[i]}")


if __name__ == "__main__":
    main()
