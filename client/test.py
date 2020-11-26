#save save


def exe2(self, final_node=None):
    self.goalNodePos = self.getGoalPosition()

    node_expand = None
    node_state = None
    if final_node == None:
        actual_node = Node(self.state, None, "", 0,
                           heuristica=dist(self.state[0], self.state[1], self.goalNodePos[0], self.goalNodePos[1]))
    else:
        actual_node = final_node
    self.frontier_nodes.insert(actual_node)
    print(self.frontier_nodes.getQueue())
    while actual_node != self.goalNodePos:
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

        if node_state == self.goalNodePos:
            print("Node state:", node_state)
            print("GoalNodePos", self.goalNodePos)
            # return self.exe2(node_expand)
        else:
            self.visited_nodes.insert(node_expand)
            avail_dir = self.find_neighbours()
            print("available moves", avail_dir)

            for dir in avail_dir:
                node_to_add = self.getNode(node_expand, dir, self.goalNodePos)
                if node_to_add not in self.frontier_nodes.getQueue():
                    self.frontier_nodes.insert(node_to_add)

            for node in self.frontier_nodes.getQueue():
                print(self.frontier_nodes.getQueue())
                if node.getHeuristica() < heur_antiga and node in self.visited_nodes.getQueue():
                    node_state = node.getState()
                    node_expand = node
                    self.c.execute("command", "forward")

                elif node.getHeuristica() < heur_antiga and node in self.frontier_nodes:
                    node_state = node.getState()
                    node_expand = node
                    self.c.execute("command", "forward")
                elif node not in self.frontier_nodes.getQueue() and node not in self.visited_nodes.getQueue():
                    self.frontier_nodes.insert(node)
                    self.visited_nodes.getQueue()

