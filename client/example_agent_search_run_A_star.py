import math

import client
import ast
import random
import copy


# AUXILIAR

FRONTIER_COLOR = "red3"
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

    def insert(self,element):
        return self.queue_data.append(element)

    def getQueue(self):
        return self.queue_data
    
    # Adicionamos o clear para "limpar" a lista de frontier e de visited para, quando o agente "bater" numa parede
    #  invisível, volte a pensar desde o novo inícios, endo este a posição atual(antes de bater no obstáculo invisível)
    def clear(self):
        self.queue_data = []

# SEARCH AGENT

class Node:
    def __init__(self,state,parent,action,path_cost,heuristica):
        self.state = state
        self.parent = parent
        self.action =action
        self.path_cost = path_cost
        # Heurística é a distância do node até ao goal, calculada na função "dist()" criada
        self.heuristica = heuristica
        # O custo do algoritmo A* será então a soma do custo para ir para a node mais o da heurística selecionada
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
        self.weightMap =[]
        self.goalNodePos =(0,0)
        self.state = (0,0)
        # Criamos obstacles aqui porque teremos que mudar estes ao encontrar obstáculos invisíveis.
        #  Estes, depois de encontrados, são então adicionados aos obstáculos
        self.obst = self.getObstacles()
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

    # Precisamos de obter os obstáculos a partir do self e não do ficheiro, por isso temos esta função
    #  Isto porque os obstáculos irão ser mais do que os iniciais ao serem adicionados os invisíveis encontrados
    def getObstaclesTotal(self):
        return self.obst

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


    def getNode(self,parent_node,action,goal):
        state = self.step(parent_node.getState(),action)
        pathCost = parent_node.getPathCost() + self.getPatchCost(state)
        heur = dist(self.state[0], self.state[1], goal[0], goal[1])
        return Node(state, parent_node, action, pathCost, heur)

    def printNodes(self,type,nodes,i):
        print(type, " (round ", i, " )")
        print("state | path cost")
        for node in nodes.getQueue():
            print(node.getState(),"|", node.getPathCost())

    # Adicionamos este, irá servir para retornar o custo total(PathCost + Heurística), sendo mais relevante mostrar
    #  nos prints que ocorrem durante a procura
    def printNodesPoderoso(self,type,nodes,i):
        print(type, " (round ", i, " )")
        print("state | cost")
        for node in nodes.getQueue():
            print(node.getState(), "|", node.getCost())

    def printPath(self, node):
        n = node
        n_list = []
        while n.getPathCost() != 0:
            n_list.insert(0,[n.getState(), n.getPathCost()])
            n = n.getParent()
        n_list.insert(0,[self.getSelfPosition(),0])
        print("Final Path", n_list)
    # Funcao que pinta o pensamento do agente
    def mark_frontier(self, node):

        self.c.execute("mark", str(node.getState())[1:-1].replace(" ", "") + "_" + FRONTIER_COLOR)

    # Adicionamos 2 parâmetros:

    # "invisible_obstacles" que irá ser uma lista com 1 elemento, sendo o obstáculo invisível que
    #  obstruiu a tentativa atual de chegar ao objetivo(irá ser None durante primeira vez que se corre o run)

    # "position" que será inicializada a None na primeira vez que o run corre, mas caso haja uma colisão
    #  com um obstáculo invisível esta position a posição atual antes de bater nesse obstáculo e a nova posição inicial
    def run(self, invisible_obstacles, position=None):
        #limpa os pensamentos anteriores
        """
        for node in self.frontier_nodes.getQueue():
            self.c.execute("unmark", str(node.getState())[1:-1].replace(" ", ""))
        for node in self.visited_nodes.getQueue():
            self.c.execute("unmark", str(node.getState())[1:-1].replace(" ", ""))
        """
        # Get the position of the Goal
        self.frontier_nodes.clear()
        self.visited_nodes.clear()
        self.goalNodePos = self.getGoalPosition()

        # Get information of the weights for each step in the world ...
        self.weightMap = self.getWeightMap()
        # Get max coordinates
        self.maxCoord = self.getMaxCoord()
        # Get the initial position of the agent
        self.state = self.getSelfPosition()

        # Se não for a posição inicial, o state será a posição nova (acontece depois de bater no obstáculo invisível)
        if position != None:
            self.state = position

        # Se a lista não for vazia, ou seja, na primeira vez que o run corre onde não se bateu contra um obstáculo
        #  invisível, irá correr
        if invisible_obstacles != []:
            # Irá adicionar na lista de obstáculos o obstáculo invisível encontrado na tentativa anterior
            self.obst[invisible_obstacles[0][0]][invisible_obstacles[0][1]] = 1

        # Start thinking
        # Na primeira vez que corre serão os obstáculos visíveis, nas vezes que corre depois de serem encontrados
        #  obstáculos invisíveis estes serão incluídos
        obst = self.getObstaclesTotal()
        i = 0
        end = False
        found = None
        node_expand = None
        node_state = None

        # O valor da heurística vem da função dist, que recebe o X e Y do node atual e do goal
        heuristica = dist(self.state[0], self.state[1], self.goalNodePos[0], self.goalNodePos[1])

        # Add first node (root)
        root = Node(self.state,None,"",0, heuristica)
        self.visited_nodes.insert(root)
        # Get the first four nodes. They are not in the same position of the root node.
        for dir in ["north","east","south","west"]:
            # Verificar que não está na lista de obstacles, ou seja se a posição na lista obst é 0, ou não 1
            if obst[self.getNode(root, dir,self.goalNodePos).getState()[0]][self.getNode(root, dir,self.goalNodePos).getState()[1]] == 0:
                self.frontier_nodes.insert(self.getNode(root,dir,self.goalNodePos))
                #self.mark_frontier(self.getNode(root,dir,self.goalNodePos))# pintar os node
        # test
        self.printNodesPoderoso("Frontier", self.frontier_nodes, i)
        self.printNodesPoderoso("Visitied", self.visited_nodes, i)

        # Aqui irá se verificar todos os nodes fronteira e verificar qual deles tem o custo total (Pathcost+Heurística)
        #   menor
        while not end:
            heurantiga = 0
            minimum = None
            for node in self.frontier_nodes.getQueue():
                # Adicionar o primeiro node sempre, para ter algo a comparar
                if minimum is None:
                    node_state = node.getState()
                    node_expand = node
                    heurantiga = node.getHeuristica()
                    minimum = node.getCost()
                # Se custo toal for menor adiciona
                elif node.getCost() < minimum:
                    node_state = node.getState()
                    node_expand = node
                    heurantiga = node.getHeuristica()
                    minimum = node.getCost()
                # Caso o custo total do novo node seja igual ao minimum é usado então o que tiver menor heuristica
                elif node.getCost() == minimum and node.getHeuristica() < heurantiga:
                    node_state = node.getState()
                    node_expand = node
                    heurantiga = node.getHeuristica()
                    minimum = node.getCost()
            # Print de ajuda visual para perceber qual é o custo menor selecionado
            #print("min", minimum)

            # Verificar se o node selecionado é o goal, assim verifica que é o caminho "melhor" em termos de custo
            #   total e acaba, tornando "end" True e correndo a função exe
            if node_state == self.goalNodePos:
                print("Node state:", node_state)
                print("GoalNodePos", self.goalNodePos)
                found = node_expand
                end = True

            #estado atual será o do node selecionado
            self.state = node_state
            # Remover da fronteira o node que será espandido
            self.frontier_nodes.remove(node_expand)
            #test
            # Verificar que não está na lista de obstacles
            if obst[self.state[0]][self.state[1]] == 0:
                print("Node's position (expand):", self.state)
                # Insere na lista de nodes visitadas só depois de confirmar se não existe obstáculo
                self.visited_nodes.insert(node_expand)
                # Tenta expandir para todas direções a node
                for dir in ["north","east","west","south"]:
                    new_node = self.getNode(node_expand, dir,self.goalNodePos)
                    list_visited = []
                    for n in self.visited_nodes.getQueue():
                        list_visited.append(n.getState())
                    # Verificar que não é repetido (node já visitada)
                    if new_node.getState() not in list_visited:
                        # Verificar que não está na lista de obstacles
                        if obst[new_node.getState()[0]][new_node.getState()[1]] == 0:
                            # Insere na fronteira as nodes que poderão ser exploradas(que não são obstáculos visíveis)
                            self.frontier_nodes.insert(new_node)
                            #self.mark_frontier(new_node) # pintar os node

                # Código para mostrar todas possíveis soluções(não tem em conta obstáculos invisíveis)
                # Torna a procura mais demorada, visto que tem que percorrer mais uma vez a lista e dar print das
                # soluções todas(que em alguns casos são muitas(Exponencial))
                """
                # Verifica se exite o goal entre os frontier nodes, ignorando o custo este apresenta todas a soluções
                #  encontradas
                for node in self.frontier_nodes.getQueue():
                    if node_state == self.goalNodePos:
                        final_node = node
                        actual_dir = self.getDirection()
                        actual_pos = self.getSelfPosition()
                        actual_step = None
                        steps = []
                        actual_node = final_node
                        # Follow from the goal leaf to root...
                        while actual_node.getPathCost() != 0:
                            steps.insert(0, [actual_node.getState(), actual_node.getPathCost()])
                            actual_node = actual_node.getParent()
                        steps.insert(0, [actual_pos, 0])
                        #print("Possível solução", steps)
                """

                # test
                self.printNodesPoderoso("Frontier", self.frontier_nodes, i)
                self.printNodesPoderoso("Visitied", self.visited_nodes, i)
        if end == True:
            self.exe(found)
        else:
            print("Not Found the GOAL!!!")
        input("Waiting for return!")

    # Return the direction to which the robot must turn based on the differences between coordinates from
    #actual position and next position
    def getNextDirection(self,pos,next_pos):
        dir = None
        # North or South
        if (pos[0] == next_pos[0]):
            if (next_pos[1] == pos[1] - 1) or (pos[1] - next_pos[1] == -1 * (self.maxCoord[1] - 1)  ):
                dir = "north"
            elif (next_pos[1] == pos[1] + 1) or (pos[1] - next_pos[1] ==  (self.maxCoord[1]-1) ):
                dir = "south"
        # East or West
        elif (pos[1] == next_pos[1]):
            if (next_pos[0] == pos[0] + 1) or (pos[0] - next_pos[0]  == (self.maxCoord[0] - 1) ):
                dir = "east"
            elif (next_pos[0] == pos[0] - 1) or (pos[0] - next_pos[0] == -1 *  (self.maxCoord[0] - 1) ):
                dir = "west"
        return dir

    # Return the number of turns and the direction of the turns based on actual direction and desired direction
    def getTurns(self,direction,desired_direction):
        #Return directions
        if direction == "north" and desired_direction == "east":
            return ["right"]
        if direction == "north" and desired_direction == "west":
            return ["left"]
        if direction == "north" and desired_direction == "south":
            return ["right","right"]

        if direction == "south" and desired_direction == "east":
            return ["left"]
        if direction == "south" and desired_direction == "west":
            return ["right"]
        if direction == "south" and desired_direction == "north":
            return ["right","right"]

        if direction == "east" and desired_direction == "north":
            return ["left"]
        if direction == "east" and desired_direction == "south":
            return ["right"]
        if direction == "east" and desired_direction == "west":
            return ["right","right"]

        if direction == "west" and desired_direction == "north":
            return ["right"]
        if direction == "west" and desired_direction == "south":
            return ["left"]
        if direction == "west" and desired_direction == "east":
            return ["left","left"]
        return []



    def exe(self, final_node=None):
        actual_dir = self.getDirection()
        actual_pos = self.getSelfPosition()
        actual_step = None
        steps = []
        actual_node = final_node
        #Follow from the goal leaf to root...
        while actual_node.getPathCost() != 0:
            steps.insert(0, [actual_node.getState(), actual_node.getPathCost()])
            actual_node = actual_node.getParent()
        steps.insert(0, [actual_pos, 0])

        print("Final Path", steps)

        actions =[]
        fim = False
        i = 0
        print("Length of steps:",len(steps))
        while fim == False:
            actual_step = steps[i]
            next_step = steps[i + 1]
            print("Actual step:", actual_step)
            print("Next step:", next_step)
            next_dir = self.getNextDirection(actual_step[0],next_step[0])
            turns = self.getTurns(actual_dir, next_dir)
            for turn_action in turns:
                actions.append(turn_action)
            actions.append("forward")
            i = i + 1
            if i >= len(steps) - 1:
                fim = True
            else:
                actual_dir = next_dir
        print("Actions:",actions)
        self.c.execute("command", "set_steps")

        i = -1
        for action in actions:
            # Se a ação for uma de movimento e não de mudar de direção, corresponde a uma ação dos steps
            # Só neste caso, andamos "1" para a frente na lista, porque não queremos percorrer ações de direção
            if action == "forward":
                i += 1
            self.c.execute("command", action)

            # Após ser executada a ação irá percorrer a seguinte função, incluindo a posição atual(actual_pos),
            #  a posição que deveria estar depois de "andar"(steps[i][0], por isso temos aqui o i sendo apenas nas
            #  ações de "andar") e temos a action
            x = self.checkStuff(actual_pos, steps[i][0], action)

            # Se a condição for dirente de False então encontrou-se obstáculo
            if x != False:
                # Assim, irá correr o run denovo, devolvendo o obstáculo encontrado e a posição onde se encontra
                self.run(x, actual_pos)
            actual_pos = self.getSelfPosition()


    def checkStuff(self, actual_pos, step, action):
        # Atualizamos a posição atual
        actual_pos2 = self.getSelfPosition()
        # Se a posição atual antes do step for igual à nova, sendo a ação feita de "andar"("forward") e se a
        # posição atual for diferente do step(posição que deveria ter), insere o step como um obstáculo invisível
        if actual_pos == actual_pos2 and action == "forward" and actual_pos2 != step:
            invisible_obstacles = []
            invisible_obstacles.append(step)
            return invisible_obstacles
        else:
            return False


# STARTING THE PROGRAM:
def main():
    print("Starting client!")
    ag = Agent()
    if ag.getConnection()!= -1:
        ag.run([])


def dist(x1, y1, x2, y2):
    # Irá devolver distância entre 2 pontos, sendo utilizado para verificar distância entre node atual e goal
    result = abs(x2 - x1)+ abs(y2 - y1)
    return result

main()
