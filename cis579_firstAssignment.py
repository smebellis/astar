from cmath import inf


graph = {
    1: [6, 8],
    2: [7, 9],
    3: [4, 8], 
    4: [3, 9],
    5: [],
    6: [1, 7],
    7: [2, 6],
    8: [1, 3],
    9: [2, 4]
}

start = [[1, 0, 1],
        [0, 0, 0], 
        [2, 0, 2]]

potential_x_coords = [2, 1, -1, -2, -2, -1, 1, 2]
potential_y_coords = [1, 2, 2, 1, -1, -2, -2, -1]

class Node:
    def __init_(self, row, col, value):
        self.row = row
        self.column = col
        self.value = value
        self.g_score = inf
        self.f_score = inf
        self.came_from = None
        
def createNodes(graph):
    nodes = []
    
    for i, row in enumerate(graph):
        nodes.append([])
        for j, value in enumerate(row):
            nodes[i].append(Node(i, j, value))
            
    return nodes

def ManhattanDistance(x1, y1, x2, y2):
    return abs(x1 - x2) + abs(y1 - y2)
         
def checkIfValidMove(x, y):
    return not (x < 0 or y < 0)

def aStarSearch(startRow, startCol, endRow, endCol, graph):
    nodes = createNodes(graph)
    
    startNode = nodes[startRow][startCol]
    
    startNode.g_score = 0
    startNode.f_score = ManhattanDistance(startRow, startCol, endRow, endCol)



print("Chessboard before swap")
for row in start:
   
    print(*row, sep=' ')




def getNeighboors(x, y, X, Y, start):
    
    neighboors = []

    for k in range(8):
        newX = x + X[k]
        newY = y + Y[k]
        
        if start[newX][newY] == 0:
            if checkIfValidMove(newX, newY):
                neighboors.append((newX, newY))
                print(f"neighboor {neighboors}")
                # matrix[0][0], matrix[newX][newY] = matrix[newX][newY], matrix[0][0]
                h = ManhattanDistance(newX, newY, 2, 2)

                print(f"Manhattan distance: {h}")


getNeighboors(0, 0, potential_x_coords, potential_y_coords, start)
# h = manhattan_distance(0)

# print(f"Manhattan distance: {h}")


#This is how you swap the values

# matrix[0][0], matrix[1][2] = matrix[1][2], matrix[0][0]

# for i in range(3):
#     for j in range(3):
#         print(f"{matrix[i][j]} ", end=" ")
print("Chessboard after swap")
for row in start:
   
    print(*row, sep=' ')