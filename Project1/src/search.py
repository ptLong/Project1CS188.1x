# search.py
# ---------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html

"""
In search.py, you will implement generic search algorithms which are called
by Pacman agents (in searchAgents.py).
"""

import util

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples,
        (successor, action, stepCost), where 'successor' is a
        successor to the current state, 'action' is the action
        required to get there, and 'stepCost' is the incremental
        cost of expanding to that successor
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.  The sequence must
        be composed of legal moves
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other
    maze, the sequence of moves will be incorrect, so only use this for tinyMaze
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s,s,w,s,w,w,s,w]

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first

    Your search algorithm needs to return a list of actions that reaches
    the goal.  Make sure to implement a graph search algorithm

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print "Start:", problem.getStartState()
    print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    print "Start's successors:", problem.getSuccessors(problem.getStartState())
    """
    "*** YOUR CODE HERE ***"
    print ""
    print "----Begin DFS-----"
    
    startNode = problem.getStartState()
    fringe = util.Stack()
    fringe.push((startNode, []))
    visited = set()
    
    while not fringe.isEmpty():
        currentNode,path = fringe.pop()
        
        if problem.isGoalState(currentNode):
            #print path
            return path
        else:
            visited.add(currentNode)
            for n,d,c in problem.getSuccessors(currentNode):
                if n not in visited:
                    fringe.push( (n, path + [d]) )
    print "----End DFS-------"
    print ""

def breadthFirstSearch(problem):
    """
    Search the shallowest nodes in the search tree first.
    """
    "*** YOUR CODE HERE ***"
    #print ""
    #print "----Begin BFS-----"
    
    startNode = problem.getStartState()
    fringe = util.Queue()
    firstItem = (startNode, [])  #node, dir
    fringe.push(firstItem)
    #visited= {startNode: 0}
    visited = set()
    visited.add(startNode)
    expandedNodes = {}
    #visited = {startNode : 0+heuristic(startNode,problem)}
    #print visited
    #print "startNode: ",startNode
    while not fringe.isEmpty():
        currentItem = fringe.pop()
        currentNode, currentPath = currentItem     
 
        if currentNode not in expandedNodes.keys(): #make sure expand only onces              
            expandedNodes[currentNode] = 0

            if problem.isGoalState(currentNode):
                #print currentPath
                return currentPath
            else:
                for successors in problem.getSuccessors(currentNode):                    
                    n,d,c = successors
                    #print n,d,c
                    item = (n , currentPath + [d])
                    if n not in visited:                        
                        fringe.push(item)
                        visited.add(n)   

 

    #print "----End BFS-------"
    #print ""

def uniformCostSearch(problem):
    "Search the node of least total cost first. "
    "*** YOUR CODE HERE ***"
    print ""
    print "----Begin BFS-----"
    
    startNode = problem.getStartState()
    fringe = util.PriorityQueue()
    firstItem = (startNode, [], 0) #node, direction, ACCcost
    fringe.push(firstItem, 0)
    
    visited = {startNode:0} 
    
    while not fringe.isEmpty():
        currentNode, currentPath, currentCost = fringe.pop()
        #print currentPath
        if problem.isGoalState(currentNode):
            return currentPath
        else:
            for n,d,c in problem.getSuccessors(currentNode):
                item = (n, currentPath + [d], currentCost + c)
                if n in visited.keys():
                    if visited[n] > currentCost+c:                  
                        fringe.push(item, currentCost +c)
                        visited[n] = currentCost + c
                    else:
                        continue
                else:
                    fringe.push(item, currentCost +c)
                    visited[n] = currentCost + c

                    
                    


    print "----End DFS-------"
    print ""

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def myPriorityFunc(item):
    return item[2] + item[3]
def aStarSearch(problem, heuristic=nullHeuristic):
    "Search the node that has the lowest combined cost and heuristic first."
    "*** YOUR CODE HERE ***"
    #print ""
    #print "====Begin AStar====="
    startNode = problem.getStartState()
    fringe = util.PriorityQueueWithFunction(myPriorityFunc)
    firstItem = (startNode, [], 0, heuristic(startNode, problem))  #node, dir, AccCost, heuristic
    #print myPriorityFunc(firstItem)
    fringe.push(firstItem)
    visited= {startNode: myPriorityFunc(firstItem)}
    #print "visited", visited
    expandedNodes = {}
    #visited = {startNode : 0+heuristic(startNode,problem)}
    #print visited
    while not fringe.isEmpty():
        currentItem = fringe.pop()
        currentNode, currentPath, currentCost, currentHeuristic = currentItem 
        
        if currentNode not in expandedNodes.keys(): #make sure expand only onces              
            expandedNodes[currentNode] = myPriorityFunc(currentItem)
            if problem.isGoalState(currentNode):
                return currentPath
            else:
                for n,d,c in problem.getSuccessors(currentNode):
                    item = (n, currentPath + [d], currentCost + c, heuristic(n, problem))
                    if n in visited.keys():
                        if visited[n] > myPriorityFunc(item) :
                            fringe.push(item)
                            visited[n] = myPriorityFunc(item)
                        else:
                            continue
                    else:
                        fringe.push(item)
                        visited[n] = myPriorityFunc(item)
    
    
    #print "=====End Astar======"
    #print ""

# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
