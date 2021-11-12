"""
11-Puzzle Solver
By: Alexandra Casas and Jimena Gonzalez-Cotera Castro
"""


ROW = 3
COL = 4
WEIGHT = 1


class Node:
    def __init__(self, data, level=0, f_value=0, prevAction=[]):
        """
        Initialize the node with the data, level of the node and the calculated
        evaluation function.
        """
        self.data = data  # might be array or 2d array
        self.level = level
        self.f_value = f_value
        self.prevAction = prevAction  # stores all moves in path in reverse order
        self.prevValues = []  # stores all the f_values

    def generate_child(self):
        """
        Generate all child nodes with possible moves.
        return a list of all generated children
        """

        x, y = self.find('0')
        # 4 possible actions: Left, Right, Up, Down
        pos_values = [[x, y - 1, "L"], [x, y + 1, "R"], [x - 1, y, "U"], [x + 1, y, "D"]]
        children = []
        for i in pos_values:
            child_data = self.move_tile(self.data, x, y, i[0], i[1])
            if child_data is not None:  # if the move is possible
                child_node = Node(child_data, self.level + 1, 0, [i[2]])
                children.append(child_node)
        for ii in children:
            ii.prevAction += self.prevAction
            ii.prevValues += self.prevValues
        return children

    def move_tile(self, puzzle_data, x1, y1, x2, y2):
        """
        Move the blank space in the given direction and if the position value are out
            of limits then return None
        vertical indices include 0,1,2
        horizontal indices include 0,1,2,3
        """
        if 0 <= x2 < len(self.data) and 0 <= y2 <= len(self.data):
            holder = self.copy(puzzle_data)
            temp = holder[x2][y2]
            holder[x2][y2] = holder[x1][y1]
            holder[x1][y1] = temp
            return holder
        else:
            return None

    def evalFunc(self, goal):
        """
        Calculate f(n) = W*h(n) + g(n)
        Assigns f(n) to self.f_value
        writes f value to list to keep track
        returns f value of the node
        """
        self.f_value = (WEIGHT * self.manhattanDis(goal)) + self.level
        self.prevValues += [self.f_value]
        return self.f_value

    def manhattanDis(self, goal):
        """
        Calculates the difference between the current node and the goal node
        returns manhattan distance
        """
        dist = 0
        for i in range(ROW * COL):
            if i != 0:
                currX, currY = self.find(str(i))
                goalX, goalY = goal.find(str(i))
                dist += abs(goalX - currX)
                dist += abs(goalY - currY)
        return dist

    def find(self, x):
        """
        Returns the indexes int,int of where any tile is located
        """
        for i in range(0, ROW):
            for j in range(0, COL):
                if self.data[i][j] == x:
                    return i, j
        return 10000, 100000

    def copy(self, root):
        """
        Copy function to create a similar matrix of the given node
        """
        temp = []
        for i in root:
            t = []
            for j in i:
                t.append(j)
            temp.append(t)
        return temp


class Puzzle:
    def __init__(self, size=ROW * COL):
        """
        Initialize the 11-puzzle
        frontier keeps track of the nodes that have been generated
        reached holds the nodes that have been expanded
        nodesGenerated counts the nodes that have been generated
        """
        self.size = size
        self.frontier = []
        self.reached = []
        self.nodesGenerated = 1

    def aStar(self, initialArray, goalArray):
        """
        graph-like, weighted A star search
        input:
            initial and goal array
        output:
            initial state
            goal state
            weight given by user
            depth level of the shallowest goal node
            total number of nodes generated
            sequence of actions in the goal path
            evaluation function values
        """
        # import pdb; pdb.set_trace()
        # converts initial and goal array into node objects
        startNode = Node(initialArray)
        goalNode = Node(goalArray)

        # calculate the initial state's evaluation function
        startNode.evalFunc(goalNode)
        # append initial node to the frontier
        self.frontier.append(startNode)

        goal_found = False
        while not goal_found:
            # currNode: the node with lowest f_value in the frontier
            # currNode is located in position 0
            currNode = self.frontier.pop(0)
            # reached should only contain the data of previously expanded nodes
            self.reached.append(currNode.data)

            # goal node has been reached...
            if currNode.data == goalNode.data:
                self.writeOutput(startNode, currNode)
                goal_found = True

            # generate the children of current node
            for child in currNode.generate_child():
                child.evalFunc(goalNode)  # calculates f_value of the child

                # check that child node's data has not been previously reached
                if child.data not in self.reached:
                    # check if it is valid to add to frontier
                    if self.addToFrontier(child):
                        self.frontier.append(child)
                        self.nodesGenerated += 1
            self.frontier.sort(key=lambda x: x.f_value, reverse=False)

    def addToFrontier(self, childNode):
        """
        check if currNode can be added to the frontier
        """
        for nodeGenerated in self.frontier:
            if childNode == nodeGenerated and childNode.f_value >= nodeGenerated.f_value:
                return False
        return True

    def writeOutput(self, startNode, currNode):
        """
        Generates the output of the 11-puzzle solver
        """
        filename = input("Enter output file name: ")
        with open(filename, "w") as f:
            for ii in startNode.data:
                temp = " ".join(ii)
                temp = temp + "\n"
                f.write(temp)

            f.write("\n")

            for ii in currNode.data:
                temp = " ".join(ii)
                temp = temp + "\n"
                f.write(temp)

            f.write("\n")

            f.write(str(WEIGHT) + "\n")
            f.write((str(currNode.level)) + "\n")
            f.write((str(self.nodesGenerated)) + "\n")
            for ii in reversed(currNode.prevAction):
                f.write(str(ii) + " ")
            f.write("\n")
            for jj in currNode.prevValues:
                f.write(str(jj) + " ")


# Reads the input from user
# Returns the user input into two arrays: Initial and Goal
def readFile(filename):
    with open(filename, "r") as f:
        initialArray = []
        goalArray = []

        for i in range(ROW):  # reading input matrix
            initialArray.append(f.readline().strip('\n').split(" "))

        f.readline()  # skipping the empty line between 2 matrices

        for i in range(ROW):  # reading output matrix
            goalArray.append(f.readline().strip('\n').split(" "))

        return initialArray, goalArray


def main():
    global WEIGHT
    f = input("Enter input file name: ")
    initialArray, goalArray = readFile(f)
    WEIGHT = float(input("Please enter a valid weight: "))
    puzzle = Puzzle()
    puzzle.aStar(initialArray, goalArray)


main()
