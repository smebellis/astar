# CIS 579 First Assignment
## General Approach to the problem

My approach to this problem was to use small, but manageable functions to keep the code understandable and easy to debug.  I choose python as my language for this problem because it is what I am most familiar with and although the problem was easy to understand, the implementation took more time than expected.  In the beginning stages of development, I was using nested lists to represent each knight’s path to its end state; however, this was not working effectively.  Therefore, I adjusted my approach to the problem and developed a Node class which stored the board state in each instance.  This allowed me to approach the problem by focusing on the board state instead of each individual knight’s movement.  In addition, the board start required the positions casted to a list of tuples.  Having a board state immutable allowed for hashing of the board and comparison of start board and end board.  

## Reasons for the expand function

Starting out with an initial board state, how do I get to the final state and how is it possible to determine what a next state looks like, so it is possible to achieve the final state.  I chose to write a function called `GetNeighbors`. This function takes in a list of all the possible moves a knight can make on a 3x3 board.  Then it loops through the list and checks if it is a valid move.  A valid move is one that fits within the board space and does not occupy a space with a knight already on it.  After this function generates all the possible moves for the current node, the algorithms can cycle through each neighbor and generate newer moves.  Eventually, one of the neighbors will be in the final positions

## Heuristic for the remaining distance to goal in A*

The first step to develop an effective heuristic function for A* was to determine what are the criteria for an admissible heuristic.  An admissible heuristic must not overestimate the distance to the final state.  Overestimates in A* heuristics can cause A* to perform sub optimally.   In the case where each move can only be up, down, left, or right.  The Manhattan distance is the ideal heuristic.  The Manhattan distance abs(x1-x2)+abs(y1-y2); however, in the give problem this would result in an overestimate and therefore the Manhattan distance is not considered an admissible heuristic.  Since a knight can move three squares at a time, I adjusted the Manhattan Distance by dividing the overall result by three to account for the three moves.  This ensured the heuristic function would not overestimate the distance to the final state, and therefore be an admissible heuristic.  

