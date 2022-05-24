import time
from matplotlib import pyplot as plt
import numpy as np


def timeme(method):
    def wrapper(*args, **kw):
        startTime = int(round(time.time() * 1000))
        result = method(*args, **kw)
        endTime = int(round(time.time() * 1000))

        print(f"The {method} ran in", endTime - startTime, "ms\n")
        return result

    return wrapper


class Node(object):
    def __init__(self):
        self.boundries = []
        # Establish the chessboard boundries
        self.boundries.append([(0, 0), (0, 1), (0, 2), (2, 2)])

    def heuristic(self, start, goal):
        """Since a knight moves three spots, the Manhattan distance can not be used
        as an admissible heuristic becuase it may overestimate.  Therefore
        in order to guarantee an underestimate I took the manhattan distance and a
        divided by three.

        Args:
            start (_type_): starting position to calculate distance
            goal (_type_): ending position

        Returns:
            _type_: Interger distance between start and goal
        """
        return (abs(start[0] - goal[0]) + abs(start[1] - goal[1])) / 3

    def get_neighbors(self, pos):

        n = []
        # All the possible moves a knight can make
        for dx, dy in [
            (-2, -1),
            (-2, 1),
            (-1, -2),
            (-1, 2),
            (1, -2),
            (1, 2),
            (2, -1),
            (2, 1),
        ]:
            x2 = pos[0] + dx
            y2 = pos[1] + dy
            # Check if the move is within the board
            if x2 < 0 or x2 > 2 or y2 < 0 or y2 > 2:
                continue
            n.append((x2, y2))
        return n


def aStar(start, end, graph):
    G = {}
    F = {}

    G[start] = 0
    F[start] = graph.heuristic(start, end)

    closedVerticies = set()
    openVerticies = set([start])
    cameFrom = {}

    while len(openVerticies) > 0:

        current = None
        currentFScore = None

        for pos in openVerticies:
            if current is None or F[pos] < currentFScore:
                currentFScore = F[pos]
                current = pos

        if current == end:
            path = [current]
            while current in cameFrom:
                current = cameFrom[current]
                path.append(current)
            path.reverse()
            return path, len(closedVerticies)

        openVerticies.remove(current)
        closedVerticies.add(current)

        for neighbor in graph.get_neighbors(current):
            if neighbor in closedVerticies:
                continue
            candidateG = G[current] + 1

            if neighbor not in openVerticies:
                openVerticies.add(neighbor)
            elif candidateG >= G[neighbor]:
                continue

            cameFrom[neighbor] = current
            G[neighbor] = candidateG
            H = graph.heuristic(neighbor, end)
            F[neighbor] = G[neighbor] + H

    return None


def branchAndBound(start, end, graph):

    F = {}
    F[start] = 0

    closedVerticies = set()
    openVerticies = set([start])
    cameFrom = {}

    while len(openVerticies) > 0:

        current = None

        for pos in openVerticies:
            current = pos

        if current == end:
            path = [current]
            while current in cameFrom:
                current = cameFrom[current]
                path.append(current)
            path.reverse()
            return path, len(closedVerticies)

        openVerticies.remove(current)
        closedVerticies.add(current)

        for neighbor in graph.get_neighbors(current):
            if neighbor in closedVerticies:
                continue

            if neighbor not in openVerticies:
                openVerticies.add(neighbor)

            cameFrom[neighbor] = current

    return None


def plotPaths(path, graph):
    plt.plot([v[0] for v in path], [v[1] for v in path])
    for barrier in graph.boundries:
        plt.plot([v[0] for v in barrier], [v[1] for v in barrier])
    plt.xlim(0, 2)
    plt.ylim(0, 2)
    plt.show()


def main():
    print(f"********A STAR********\n")
    tic = time.perf_counter()
    graph = Node()
    path, cost1 = aStar((0, 0), (2, 2), graph)
    path2, cost2 = aStar((0, 2), (2, 0), graph)
    path3, cost3 = aStar((2, 0), (0, 0), graph)
    path4, cost4 = aStar((2, 2), (0, 0), graph)
    toc = time.perf_counter()

    print(f"Path 1: {path}")
    print(f"Path 2: {path2}")
    print(f"Path 3: {path3}")
    print(f"Path 4: {path4}")

    print(f"Total number of extensions: {cost1 + cost2 + cost3 + cost4}\n")
    print(f"A* took {toc - tic:0.4f} seconds to run\n")

    print(f"********Branch and Bound********\n")
    tic1 = time.perf_counter()
    path5, cost5 = branchAndBound((0, 0), (2, 2), graph)
    path6, cost6 = branchAndBound((0, 2), (2, 0), graph)
    path7, cost7 = branchAndBound((2, 0), (0, 0), graph)
    path8, cost8 = branchAndBound((2, 2), (0, 0), graph)
    toc1 = time.perf_counter()

    print(f"Path 5: {path5}")
    print(f"Path 6: {path6}")
    print(f"Path 7: {path7}")
    print(f"Path 8: {path8}")

    print(f"Total number of extensions: {cost5 + cost6 + cost7 + cost8}\n")
    print(f"Branch and Bound took {toc1 - tic1:0.4f} seconds to run\n")

    plotPaths(path, graph)
    plotPaths(path2, graph)
    plotPaths(path3, graph)
    plotPaths(path4, graph)


if __name__ == "__main__":

    main()

    # plt.plot([v[0] for v in result], [v[1] for v in result])
    # for barrier in graph.boundries:
    #     plt.plot([v[0] for v in barrier], [v[1] for v in barrier])
    # plt.xlim(0,2)
    # plt.ylim(0,2)
    # plt.show()
