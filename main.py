ROW = 3
COL = 4
WEIGHT = 1.0


class Node:
    def __init__(self, data, level=0, f_value=0, lastMove=''):
        """ 
        Initialize the node with the data, level of the node and the calculated fvalue 
        """
        self.data = data  # might be array or 2d array
        self.level = level
        self.f_value = f_value
        self.lastMove = lastMove

    def generate_child(self):
        """
        Generate all child nodes with possible moves.
        """
        x, y = self.find(self.data, '0')  # might have to change from char to int
        pos_values = [[x, y - 1,"D"], [x, y + 1, "U"], [x - 1, y, "L"], [x + 1, y, "R"]] # DULR
        children = []
        for i in pos_values:
            child_data = self.move_tile(self.data, x, y, i[0], i[1])
            if child_data is not None:  # if the move is possible
                child_node = Node(child_data, self.level + 1, 0)
                child_node.lastMove = (i[2]) 
                children.append(child_node)
        return children



    def move_tile(self, puzzle_data, x1, y1, x2, y2):
        """
        Move the blank space in the given direction and if the position value are out
            of limits the return None """
        if x2 >= 0 and x2 < len(self.data) and y2 >= 0 and y2 < len(self.data):
            holder = []
            holder = self.copy(puzzle_data)
            temp = holder[x2][y2]
            holder[x2][y2] = holder[x1][y1]
            holder[x1][y1] = temp
            return holder
        else:
            return None

    def find(self, puzzle_data, x):
        """
        Returns the position int,int of where 0 is located
        """
        for i in range(0, len(self.data)):
            for j in range(0, len(self.data)):
                if puzzle_data[i][j] == x:
                    return i, j

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
        input: =12
        Initialize the puzzle size by the specified size,open and closed lists to empty
        """
        self.n = size
        self.frontier = []
        self.reached = []
        self.nodes_generated = 1
        self.moves = []

    def evalFunc(self, current, goal):
        """
        input: Node, Node
        Calculate f(n) = W*h(n) + g(n)
        """
        return WEIGHT * self.manhattanDis(current.data, goal.data) + current.level

    def manhattanDis(self, current, goal):
        """
        input: array, array ?
        Calculates the different between the given puzzles
        """
        res = 0
        for i in range(0, ROW):
            for j in range(0, COL):
                if current[i][j] != goal[i][j] and current[i][j] != 0:
                    res += 1
        return res

    def process(self, initialArray, goalArray):
        """
        input: Node, Node
        Accept Start and Goal Puzzle state
        """
        # print("Enter the start state matrix: \n")
        # start = self.readFile()
        # print("Enter the goal state matrix: \n")
        # goal = self.readFile()

        start = Node(initialArray)
        goal = Node(goalArray)
        start.f_value = self.evalFunc(start, goal)

        # initialState.f_value = self.evalFunc(initialState, goalState)

        """ Put the start node in the open list"""
        self.frontier.append(start)

        print("\n\n")
        while True:
            currState = self.frontier[0]
            print("")
            print("  | ")
            print("  | ")
            print(" \\\'/ \n")
            for ii in currState.data:
                for jj in ii:
                    print(jj, end=" ")
                print("")
            """ If the difference between current and goal node is 0 we have reached the goal node"""
            if self.manhattanDis(currState.data, goal.data) == 0:
                self.writeOutput(start.data, currState)
                break
            for ii in currState.generate_child():
                ii.f_value = self.evalFunc(ii, goal)
                self.frontier.append(ii)
                self.nodes_generated += 1
            self.reached.append(currState)
            self.moves.append(currState.lastMove)
            del self.frontier[0]

            """ sort the open list based on f value """
            self.frontier.sort(key=lambda x: x.f_value, reverse=False)

        
    def writeOutput(self, start_data, currState):
        filename = input("Enter output file name: ")
        with open(filename, "w") as f:
            for ii in start_data:
                temp = " ".join(ii)
                temp = temp + "\n"
                f.write(temp)

            f.write("\n")

            for ii in currState.data:
                temp = " ".join(ii)
                temp = temp + "\n"
                f.write(temp)

            f.write("\n")

            f.write(str(WEIGHT) + "\n")
            f.write((str(currState.level)) + "\n")
            f.write((str(self.nodes_generated)) + "\n")
            f.write(" ".join(self.moves) + "\n")
            #f.write(self.moves())


def readFile(fname):  # to read the input and set up initial and goal state objects
    with open(fname, "r") as f:
        initialArray = []
        goalArray = []

        for i in range(ROW):  # reading input matrix
            initialArray.append(f.readline().strip('\n').split(" "))

        f.readline()  # skipping the empty line between 2 matrices

        for i in range(ROW):  # reading output matrix
            goalArray.append(f.readline().strip('\n').split(" "))

        return initialArray, goalArray



        

def main():
    # global WEIGHT
    # f = input("Enter input file name: ")
    #f = "test_dude.txt"
    f = 'Sample_Input.txt'
    #f = "correct_test.txt"
    initialArray, goalArray = readFile(f)
    # WEIGHT = input("Please enter a valid weight: ")
    puzzle = Puzzle()
    # puzzle.process()
    puzzle.process(initialArray, goalArray)
    # print(initialState)
    # print(goalState)
    # gState, nodesGenerated = aStar(initialState, goalState)
    # printOutput(gState, nodesGenerated)


main()
