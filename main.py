ROW = 3
COL = 4
WEIGHT = 1.0
class Node: 
    def __init__(self,data,level = 0 ,f_value = 0 ):
        """ 
        Initialize the node with the data, level of the node and the calculated fvalue 
        """
        self.data = data #might be array or 2d array
        self.level = level
        self.f_value = f_value

    def generate_child(self):
        """
        Generate all child nodes with possible moves.
        """
        x,y = self.find(self.data,'0') #might have to change from char to int
        pos_values = [[x,y-1],[x,y+1],[x-1,y],[x+1,y]]
        children = []
        for i in pos_values:
            child_data = self.move_tile(self.data,x,y,i[0],i[1])
            if child_data is not None: #if the move is possible
                child_node = Node(child_data,self.level+1,0)
                children.append(child_node)
        return children

        def move_tile(self,puzzle_data,x1,y1,x2,y2):
        """ Move the blank space in the given direction and if the position value are out
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

        def find(self,puzzle_data,x):
        """ 
        Returns the position int,int of where 0 is located 
        """
        for i in range(0,len(self.data)):
            for j in range(0,len(self.data)):
                if puzzle_data[i][j] == x:
                    return i,j

        def copy(self,root):
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


def readFile(fname):            #to read the input and set up initial and goal state objects
  with open(fname, "r") as f:
    initialArray = [] 
    goalArray = []  
    
    for i in range(ROW):        #reading input matrix
        for num in f.readline().split():    #reading line by line and creating list of numbers in that line 
            initialArray.append(int(num))   

    f.readline()    #skipping the empty line between 2 matrices

    for i in range(ROW):        #reading output matrix
        for num in f.readline().split():    #reading line by line and creating list of numbers in that line 
            goalArray.append(int(num))

    #initialState = Node(initialArray)
    #goalState = Node(goalArray)

    #return initialState, goalState
    return initialArray, goalArray
                    

def main():
    global WEIGHT
    f = input("Enter input file name: ")
    initialState, goalState = readFile(f)
    WEIGHT = input("Please enter a valid weight")

    print(initialState)
    print(goalState)
    #gState, nodesGenerated = aStar(initialState, goalState)
    #printOutput(gState, nodesGenerated)


main()