ROW = 3
COL = 4
WEIGHT = 1.0


class Node:
    def __init__(self, data, level=0, f_value=0, prevAction = [] ):
        """ 
        Initialize the node with the data, level of the node and the calculated fvalue 
        """
        self.data = data  # might be array or 2d array
        self.level = level
        self.f_value = f_value
        self.prevAction = prevAction #stores all moves in path in reverse order
        self.prevValues = [] 

    def generate_child(self):
        """
        Generate all child nodes with possible moves.
        return a list of all generated children
        """
        x, y = self.find('0')  # might have to change from char to int
        pos_values = [[x, y - 1, "L"], [x, y + 1, "R"], [x - 1, y, "U"], [x + 1, y, "D"]]  # DULR
        children = []
        for i in pos_values:
            child_data = self.move_tile(self.data, x, y, i[0], i[1])
            if child_data is not None:  # if the move is possible
                # child_node = Node(child_data, self.level + 1, 0, i[2])
                child_node = Node(child_data, self.level + 1 , 0, [i[2]])
                #print("i2 is : " + i[2])
                children.append(child_node)
        for ii in children: 
            ii.prevAction += self.prevAction
            ii.prevValues += self.prevValues
        return children

    def move_tile(self, puzzle_data, x1, y1, x2, y2):
        """
        Move the blank space in the given direction and if the position value are out
            of limits the return None
        """
        if x2 >= 0 and x2 < len(self.data) and y2 >= 0 and y2 < len(self.data):
            holder = []
            holder = self.copy(puzzle_data)
            temp = holder[x2][y2]
            holder[x2][y2] = holder[x1][y1]
            holder[x1][y1] = temp
            return holder
        else:
            return None

    def evalFunc(self, goal):
        """
        input: Goal node
        Calculate f(n) = W*h(n) + g(n)
        Assigns f(n) to self.f_value
        writes f value to list to keep track
        returns dereferenced f_value, -1 if failed
        """
        self.f_value = ( WEIGHT * self.manhattanDis(goal)) + self.level
        self.prevValues += [self.f_value]
        #return *(self.f_value)
        return self.f_value

    def manhattanDis(self, goal):
        """
        input: GOAL NODE
        Calculates the different between the given puzzles
        returns manhattan distance
        """
        dist = 0
        for i in range(12): 
            if i != 0:
                currx, curry = self.find(str(i))
                goalx, goaly = goal.find(str(i))
                dist += abs(goalx - currx)
                dist += abs(goaly - curry)
        return dist

    #def find(self, puzzle_data, x):
    def find(self, x):
        """
        Returns the position int,int of where 0 is located
        """
        for i in range(0, len(self.data)):
            for j in range(0, len(self.data)):
                if self.data[i][j] == x:
                    return i, j
        return 100,100

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
        # self.moves = moves
        #self.moves = []

    def process(self, initialArray, goalArray):
        """
        input: Node, Node
        Accept Start and Goal Puzzle state
        """
        start = Node(initialArray)
        goal = Node(goalArray)
        start.evalFunc(goal)
        """ Put the start node in the open list"""
        self.frontier.append(start)
        #print("\n\n")
        while True:
            currState = self.frontier[0]
            """ print("")
            print("  | ")
            print("  | ")
            print(" \\\'/ \n")
            print(currState.level)
            print(currState.f_value)
            for ii in currState.data:
                for jj in ii:
                    print(jj, end=" ")
                print("") """
            """ If the difference between current and goal node is 0 we have reached the goal node"""
            if currState.manhattanDis(goal) == 0:
                self.writeOutput(start.data, currState)
                break
            for ii in currState.generate_child():
                ii.evalFunc(goal)
                self.frontier.append(ii)
                self.nodes_generated += 1
            self.reached.append(currState)
            del self.frontier[0]
            """ sort the open list based on f value """
            self.frontier.sort(key=lambda x: x.f_value, reverse=False)

    def writeOutput(self, start_data, currState):
        filename = input("Enter output file name: ")
        filename = "file.txt"
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
            for ii in reversed(currState.prevAction):
                f.write(str(ii) + " ")
            f.write("\n")
            for ii in reversed(currState.prevValues):
                f.write(str(ii) + " ")


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
    f = input("Enter input file name: ")
    # f = "test_dude.txt"
    #f = 'Sample_Input.txt'
    # f = "correct_test.txt"
    initialArray, goalArray = readFile(f)
    WEIGHT = input("Please enter a valid weight: ")
    puzzle = Puzzle()
    puzzle.process(initialArray, goalArray)


main()
