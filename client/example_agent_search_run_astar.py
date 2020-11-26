import math

import client
import ast
import random
import copy


# AUXILIAR

class Queue:
    def __init__(self):
        self.queue_data = []

    def isEmpty(self):
        if len(self.queue_data) == 0:
            return True
        else:
            return False

    def remove(self, elem):
        return self.queue_data.remove(elem)

    def pop(self):
        return self.queue_data.pop(0)

    def insert(self, element):
        return self.queue_data.append(element)

    def getQueue(self):
        return self.queue_data


# SEARCH AGENT

class Node:
    def __init__(self, state, parent, action, path_cost, heuristica):
        self.state = state
        self.parent = parent
        self.action = action
        self.path_cost = path_cost
        self.heuristica = heuristica
        self.cost = self.path_cost + self.heuristica

    def getState(self):
        return self.state

    def getParent(self):
        return self.parent

    def getAction(self):
        return self.action

    def getPathCost(self):
        return self.path_cost

    def getHeuristica(self):
        return self.heuristica

    def getCost(self):
        return self.cost

    def setHeuristica(self, heur):
        self.heuristica = heur


class Agent:
    def __init__(self):

        self.c = client.Client('127.0.0.1', 50001)
        self.res = self.c.connect()
        random.seed()  # To become true random, a different seed is used! (clock time)
        self.visited_nodes = Queue()
        self.frontier_nodes = Queue()
        self.weightMap = []
        self.obst = self.getObstacles()
        self.goalNodePos = (0, 0)
        self.state = (0, 0)
        self.maxCoord = (0, 0)

    def getConnection(self):
        return self.res

    # NEW NEW
    def getDirection(self):
        msg = self.c.execute("info", "direction")
        dir = msg  # ast.literal_eval(msg)
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

    def getPatchCost(self, pos):
        return self.weightMap[pos[0]][pos[1]]

    def getMaxCoord(self):
        msg = self.c.execute("info", "maxcoord")
        max_coord = ast.literal_eval(msg)
        # test
        print('Received maxcoord', max_coord)
        return max_coord

    def getObstacles(self):
        msg = self.c.execute("info", "obstacles")
        obst = ast.literal_eval(msg)
        # test
        print('Received map of obstacles:', obst)
        return obst

    def step(self, pos, action):
        if action == "east":
            if pos[0] + 1 < self.maxCoord[0]:
                new_pos = (pos[0] + 1, pos[1])
            else:
                new_pos = (0, pos[1])

        if action == "west":
            if pos[0] - 1 >= 0:
                new_pos = (pos[0] - 1, pos[1])
            else:
                new_pos = (self.maxCoord[0] - 1, pos[1])

        if action == "south":
            if pos[1] + 1 < self.maxCoord[1]:
                new_pos = (pos[0], pos[1] + 1)
            else:
                new_pos = (pos[0], 0)

        if action == "north":
            if pos[1] - 1 >= 0:
                new_pos = (pos[0], pos[1] - 1)
            else:
                new_pos = (pos[0], self.maxCoord[1] - 1)
        return new_pos

    def getNode(self, parent_node, action, goal):
        state = self.step(parent_node.getState(), action)
        pathCost = parent_node.getPathCost() + self.getPatchCost(state)
        heur = dist(self.state[0], self.state[1], goal[0], goal[1])
        return Node(state, parent_node, action, pathCost, heur)

    def printNodes(self, type, nodes, i):
        print(type, " (round ", i, " )")
        print("state | path cost")
        for node in nodes.getQueue():
            print(node.getState(), "|", node.getPathCost())

    def printNodesPoderoso(self, type, nodes, i):
        print(type, " (round ", i, " )")
        print("state | cost")
        for node in nodes.getQueue():
            print(node.getState(), "|", node.getCost())

    def printPath(self, node):
        n = node
        n_list = []
        while n.getPathCost() != 0:
            n_list.insert(0, [n.getState(), n.getPathCost()])
            n = n.getParent()
        n_list.insert(0, [self.getSelfPosition(), 0])
        print("Final Path", n_list)

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

    def run(self,invisible_obstacles):
        # Get the position of the Goal

        self.goalNodePos = self.getGoalPosition()
        # Get information of the weights for each step in the world ...
        self.weightMap = self.getWeightMap()
        # Get max coordinates
        self.maxCoord = self.getMaxCoord()
        # Get the initial position of the agent
        self.state = self.getSelfPosition()

        # Start thinking

        if invisible_obstacles != []:
            self.obst[invisible_obstacles[0][0]][invisible_obstacles[0][1]] = 1
        print("THESEARE BOSTALASDLASLD!",self.obst)
        i = 0
        end = False
        found = None
        node_expand = None
        node_state = None
        #Add first node (root)
        root = Node(self.state,None,"",0, heuristica = dist(self.state[0], self.state[1], self.goalNodePos[0], self.goalNodePos[1]))
        self.visited_nodes.insert(root)
        # Get the first four nodes. They are not in the same position of the root node.
        for dir in ["north", "east", "south", "west"]:
            if self.obst[self.getNode(root, dir, self.goalNodePos).getState()[0]][
                self.getNode(root, dir, self.goalNodePos).getState()[1]] == 0:
                self.frontier_nodes.insert(self.getNode(root, dir, self.goalNodePos))
        # test
        self.printNodesPoderoso("Frontier", self.frontier_nodes, i)
        self.printNodesPoderoso("Visitied", self.visited_nodes, i)
        end = False

        # Cycle expanding nodes following the sequence in frontier nodes.
        while not end:
            minimum = None
            heur_antiga = 0
            for node in self.frontier_nodes.getQueue():
                if minimum is None:
                    node_state = node.getState()
                    node_expand = node
                    heur_antiga = node.getHeuristica()
                    minimum = node.getCost()
                elif node.getCost() < minimum:
                    node_state = node.getState()
                    node_expand = node
                    minimum = node.getCost()
                elif node.getCost() == minimum:
                    if node.getHeuristica() < heur_antiga:
                        node_state = node.getState()
                        node_expand = node


            print("min", minimum)
            if node_state == self.goalNodePos:
                print("Node state:", node_state)
                print("GoalNodePos", self.goalNodePos)
                found = node_expand
                end = True

            self.state = node_state
            self.frontier_nodes.remove(node_expand)
            #test
            if self.obst[self.state[0]][self.state[1]] == 0:
                #if node_expand not in self.visited_nodes.getQueue():
                print("Node's position (expand):", self.state)
                self.visited_nodes.insert(node_expand)
                for dir in ["north", "east", "west", "south"]:
                    new_node = self.getNode(node_expand, dir, self.goalNodePos)
                    list_visited = []
                    list_visited = []
                    for n in self.visited_nodes.getQueue():
                        #if n.getState() not in list_visited:
                        list_visited.append(n.getState())
                    if new_node.getState() not in list_visited:
                        if self.obst[new_node.getState()[0]][new_node.getState()[1]] == 0:
                            #if new_node not in self.frontier_nodes.getQueue():
                            self.frontier_nodes.insert(new_node)

                # test
                self.printNodesPoderoso("Frontier", self.frontier_nodes, i)
                self.printNodesPoderoso("Visitied", self.visited_nodes, i)
        if end == True:

            self.exe(found)
        else:
            print("Not Found the GOAL!!!")
        input("Waiting for return!")

    def find_neighbours(self):
        list_neighbours=[]
        # we need to reset the actual_dir each time
        actual_dir = self.c.execute("info", "direction")

        north_directions = self.getTurns(actual_dir, "north")
        for action in north_directions:
            self.c.execute("command", action)
        north_neighbour = self.c.execute("info","view")[2]
        list_neighbours.append(north_neighbour)
        actual_dir = self.c.execute("info", "direction")

        south_directions = self.getTurns(actual_dir, "south")
        for action in south_directions:
            self.c.execute("command", action)
        south_neighbour = self.c.execute("info","view")[2]
        list_neighbours.append(south_neighbour)
        actual_dir = self.c.execute("info", "direction")

        east_directions = self.getTurns(actual_dir, "east")
        for action in east_directions:
            self.c.execute("command", action)
        east_neighbour = self.c.execute("info","view")[2]
        list_neighbours.append(east_neighbour)
        actual_dir = self.c.execute("info", "direction")

        west_directions = self.getTurns(actual_dir, "west")
        for action in west_directions:
            self.c.execute("command", action)
        west_neighbour = self.c.execute("info","view")[2]
        list_neighbours.append(west_neighbour)
        print("neighbours(N;S;E;W):",list_neighbours)

        dir = []
        if list_neighbours[0] == "u":
            dir.append("north")
        if list_neighbours[1] == "u":
            dir.append("south")
        if list_neighbours[2] == "u":
            dir.append("east")
        if list_neighbours[3] == "u":
            dir.append("west")

        return dir


    def exe(self, final_node=None):
        actual_step = None
        actual_dir = self.getDirection()
        actual_pos = self.getSelfPosition()
        print("ACTUAL POS",actual_pos)
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
        self.c.execute("command", "set_steps")
        for action in actions:
            self.c.execute("command", action)
            if self.checkStuff(actual_pos,actual_step) != False:
                print("DOES THIS CHECK OUT BRO",print())
                self.c.execute("command","home")
                self.run(self.checkStuff(actual_pos,actual_step))
            actual_pos= self.getSelfPosition()


    def checkStuff(self,actual_pos,actual_step):
        actual_pos2 = self.getSelfPosition()
        if actual_pos == actual_pos2:
            invisible_obstacles = []
            invisible_obstacles.append(actual_step[0])
            #self.run(invisible_obstacles)
            return invisible_obstacles
        else:
            return False


# STARTING THE PROGRAM:
def main():
    print("Starting client!")
    ag = Agent()
    if ag.getConnection() != -1:
        ag.run([])


def dist(x1, y1, x2, y2):
    #result = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
    x= x1 - x2
    y= y1 - y2
    manhattan = abs(x)+ abs(y)
    # print("x1",x1,"x2",x2,"y1",y1,"y2",y2,"result",result)
    return manhattan


main()
