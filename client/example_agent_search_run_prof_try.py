import client
import ast
import random
import copy


# AUXILIAR
class Stack:
    def __init__(self):
        self.items = []

    def is_empty(self):
        return self.items == []

    def push(self, item):
        self.items.insert(0,item)

    def pop(self):
        return self.items.pop(0)

    def size(self):
        return len(self.items)

    def peek(self):
        return self.items[0]

    def str(self):
        return self.items

class Queue:
    def __init__(self):
         self.queue_data = []

    def isEmpty(self):
        if len(self.queue_data) == 0:
            return True
        else:
            return False

    def pop(self):
        return self.queue_data.pop(0)

    def poppop(self):
        return self.queue_data.pop(-1)

    def insert(self,element):
        return self.queue_data.append(element)

    def getQueue(self):
        return self.queue_data

# SEARCH AGENT

class Node:
    def __init__(self,state,parent,action,path_cost,level):
        self.state = state
        self.parent = parent
        self.action =action
        self.path_cost = path_cost
        self.level = level

    def getState(self):
        return self.state

    def getParent(self):
        return self.parent

    def getAction(self):
        return self.action

    def getPathCost(self):
        return self.path_cost

    def getParent(self):
        return self.parent

    def getLevel(self):
        return self.level


class Agent:
    def __init__(self):
        self.c = client.Client('127.0.0.1', 50001)
        self.res = self.c.connect()
        random.seed()  # To become true random, a different seed is used! (clock time)
        self.visited_nodes = Queue()
        self.frontier_nodes = Stack()
        self.weightMap =[]
        self.goalNodePos =(0,0)
        self.state = (0,0)
        self.maxCoord = (0,0)


    def getConnection(self):
        return self.res
    # NEW NEW
    def getDirection(self):
        msg = self.c.execute("info", "direction")
        dir = msg#ast.literal_eval(msg)
        # test
        print('Dir is:', dir)
        return dir

    def getGoalPosition(self):
        msg = self.c.execute("info", "goal")
        goal = ast.literal_eval(msg)
        # test
        print('Goal is located at:', goal)
        return goal

    def getSelfPosition(self):
        msg = self.c.execute("info", "position")
        pos = ast.literal_eval(msg)
        # test
        print('Received agent\'s position:', pos)
        return pos

    def getWeightMap(self):
        msg = self.c.execute("info", "map")
        w_map = ast.literal_eval(msg)
        # test
        print('Received map of weights:', w_map)
        return w_map

    def getPatchCost(self,pos):
        return self.weightMap[pos[0]][pos[1]]

    def getMaxCoord(self):
        msg = self.c.execute("info","maxcoord")
        max_coord =ast.literal_eval(msg)
        # test
        print('Received maxcoord', max_coord)
        return max_coord

    def getObstacles(self):
        msg = self.c.execute("info","obstacles")
        obst =ast.literal_eval(msg)
        # test
        print('Received map of obstacles:', obst)
        return obst



    def step(self,pos,action):
        if action == "east":
            if pos[0] + 1 < self.maxCoord[0]:
                new_pos = (pos[0] + 1, pos[1])
            else:
                new_pos =(0,pos[1])

        if action == "west":
            if pos[0] - 1 >= 0:
                new_pos = (pos[0] - 1, pos[1])
            else:
                new_pos = (self.maxCoord[0] - 1, pos[1])


        if action == "south":
            if pos[1] + 1 < self.maxCoord[1]:
                new_pos = (pos[0], pos[1] + 1 )
            else:
                new_pos = (pos[0], 0)

        if action == "north":
            if pos[1] - 1 >= 0:
                new_pos = (pos[0], pos[1] - 1)
            else:
                new_pos = (pos[0], self.maxCoord[1] - 1 )
        return new_pos


    def getNode(self,parent_node,action):
        state = self.step(parent_node.getState(),action)
        level = parent_node.getLevel() + 1
        pathCost = parent_node.getPathCost() + self.getPatchCost(state)
        return Node(state, parent_node, action, pathCost, level)

    def printNodes(self, type, nodes, i):
        print(type, " (round ", i, " )")
        print("state | path cost")
        for node in nodes.getQueue():
            print(node.getState(), "|", node.getPathCost())

    def printNodes2(self, type, nodes, i):
        print(type, " (round ", i, " )")
        print("state | path cost")
        for node in nodes.str():
            print(node.getState(), "|", node.getPathCost())

    def printPath(self, node):
        n = node
        n_list = []
        while n.getPathCost() != 0:
            n_list.insert(0, [n.getState(), n.getPathCost()])
            n = n.getParent()
        n_list.insert(0, [self.getSelfPosition(), 0])
        print("Final Path", n_list)

    def run(self):
        # Get the position of the Goal
        self.goalNodePos = self.getGoalPosition()
        # Get information of the weights for each step in the world ...
        self.weightMap = self.getWeightMap()
        # Get max coordinates
        self.maxCoord = self.getMaxCoord()
        # Get the initial position of the agent
        self.state = self.getSelfPosition()
        # Start thinking
        obst = self.getObstacles()
        i = 0
        found = None

        #Add first node (root)
        root = Node(self.state,None,"",0,0)
        self.visited_nodes.insert(root)

        # Get the first four nodes. They are not in the same position of the root node.
        """"
        dir = ["north","east","south","west"]
        for i in range(len(dir)):
            x = random.sample(dir, 1)[0]
            print(x)
            if obst[self.getNode(root, x).getState()[0]][self.getNode(root, x).getState()[1]] == 0:
                self.frontier_nodes.insert(self.getNode(root, x)) 
        dire = ["north", "east", "west", "south"]
        random.shuffle(dire)
        for dir in dire:
            if obst[self.getNode(root, dir).getState()[0]][self.getNode(root, dir).getState()[1]] == 0:
                self.frontier_nodes.push(self.getNode(root, dir))
        """


        for dir in ["north", "east", "south", "west"]:
            if obst[self.getNode(root, dir).getState()[0]][self.getNode(root, dir).getState()[1]] == 0:
                self.frontier_nodes.push(self.getNode(root, dir))


        # test
        #self.printNodes2("Frontier", self.frontier_nodes, i)
        #self.printNodes("Visitied", self.visited_nodes, i)
        printed=[]
        for i in self.frontier_nodes.str():
            printed.append(i.getState())

        print("frontier:", printed)
        end = False
        limit = 999
        # Cycle expanding nodes following the sequence in frontier nodes.
        while (end == False and self.frontier_nodes.is_empty()==False):
            if self.frontier_nodes.peek().getLevel() < limit:
                """max=self.frontier_nodes.peek().getCost()
                for i in self.frontier_nodes.str():
                    if i.getCost() > max:
                        max = i
                """
                node_to_expand = self.frontier_nodes.pop()
                self.state = node_to_expand.getState()
                if obst[self.state[0]][self.state[1]] == 0:
                    print("Node's position (expand):", self.state)
                    self.visited_nodes.insert(node_to_expand)

                    """
                    for i in range(len(dir)):
                        x = random.sample(dir, 1)[0]
                        new_node = self.getNode(node_to_expand, x)
                        
                    dire = ["north", "east", "west", "south"]
                    random.shuffle(dire)
                    for dir in dire:
                        new_node = self.getNode(node_to_expand, dir)
                        list_visited = []
                    """
                    for dir in ["north", "east", "west", "south"]:
                        new_node = self.getNode(node_to_expand, dir)
                        list_visited = []
                        for n in self.visited_nodes.getQueue():
                            list_visited.append(n.getState())
                        if new_node.getState() not in list_visited:
                            if obst[new_node.getState()[0]][new_node.getState()[1]] == 0:
                                self.frontier_nodes.push(new_node)

                    # test
                    #self.printNodes2("Frontier", self.frontier_nodes, i)
                    #self.printNodes("Visitied", self.visited_nodes, i)
                    printed = []
                    for i in self.frontier_nodes.str():
                        printed.append(i.getState())

                    print("frontier:", printed)
                    for node in self.frontier_nodes.str():
                        if node.getState() == self.goalNodePos:
                            print("Node state:", node.getState())
                            print("GoalNodePos", self.goalNodePos)
                            found = node
                            # self.printPath(found)
                            end = True

                    for node in self.frontier_nodes.str():
                        print(node.getLevel())
                        if node.getLevel() > limit:
                            self.frontier_nodes.pop()

            else:
                self.frontier_nodes.pop()

        if end == True:
            self.exe(found)
        else:
            print("Not Found the GOAL!!!")
        input("Waiting for return!")

    # Return the direction to which the robot must turn based on the differences between coordinates from
    # actual position and next position
    def getNextDirection(self, pos, next_pos):
        dir = None
        # North or South
        if (pos[0] == next_pos[0]):
            if (next_pos[1] == pos[1] - 1) or (pos[1] - next_pos[1] == -1 * (self.maxCoord[1] - 1)):
                dir = "north"
            elif (next_pos[1] == pos[1] + 1) or (pos[1] - next_pos[1] == (self.maxCoord[1] - 1)):
                dir = "south"
        # East or West
        elif (pos[1] == next_pos[1]):
            if (next_pos[0] == pos[0] + 1) or (pos[0] - next_pos[0] == (self.maxCoord[0] - 1)):
                dir = "east"
            elif (next_pos[0] == pos[0] - 1) or (pos[0] - next_pos[0] == -1 * (self.maxCoord[0] - 1)):
                dir = "west"
        return dir

    # Return the number of turns and the direction of the turns based on actual direction and desired direction
    def getTurns(self, direction, desired_direction):
        # Return directions
        if direction == "north" and desired_direction == "east":
            return ["right"]
        if direction == "north" and desired_direction == "west":
            return ["left"]
        if direction == "north" and desired_direction == "south":
            return ["right", "right"]

        if direction == "south" and desired_direction == "east":
            return ["left"]
        if direction == "south" and desired_direction == "west":
            return ["right"]
        if direction == "south" and desired_direction == "north":
            return ["right", "right"]

        if direction == "east" and desired_direction == "north":
            return ["left"]
        if direction == "east" and desired_direction == "south":
            return ["right"]
        if direction == "east" and desired_direction == "west":
            return ["right", "right"]

        if direction == "west" and desired_direction == "north":
            return ["right"]
        if direction == "west" and desired_direction == "south":
            return ["left"]
        if direction == "west" and desired_direction == "east":
            return ["left", "left"]
        return []

    def exe(self, final_node=None):
        actual_dir = self.getDirection()
        actual_pos = self.getSelfPosition()
        steps = []
        actual_node = final_node
        # Follow from the goal leaf to root...
        while actual_node.getPathCost() != 0:
            steps.insert(0, [actual_node.getState(), actual_node.getPathCost()])
            actual_node = actual_node.getParent()
        steps.insert(0, [actual_pos, 0])

        print("Final Path", steps)

        actions = []
        fim = False
        i = 0
        print("Length of steps:", len(steps))
        while fim == False:
            actual_step = steps[i]
            next_step = steps[i + 1]
            print("Actual step:", actual_step)
            print("Next step:", next_step)
            next_dir = self.getNextDirection(actual_step[0], next_step[0])
            turns = self.getTurns(actual_dir, next_dir)
            for turn_action in turns:
                actions.append(turn_action)
            actions.append("forward")
            i = i + 1
            if i >= len(steps) - 1:
                fim = True
            else:
                actual_dir = next_dir
        print("Actions:", actions)
        for action in actions:
            self.c.execute("command", action)

# STARTING THE PROGRAM:
def main():
    print("Starting client!")
    ag = Agent()
    if ag.getConnection()!= -1:
        ag.run()

main()
