# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
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
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem: SearchProblem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print("Start:", problem.getStartState())
    print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    print("Start's successors:", problem.getSuccessors(problem.getStartState()))
    """
    "*** YOUR CODE HERE ***"
    visited = set()
    stack = util.Stack()
    start = problem.getStartState()   #we get the starting point
    stack.push((start, []))      #push the start state into the empty stack

    while stack.isEmpty() == False:
        cur_node, path = stack.pop()   
        if problem.isGoalState(cur_node):    #checks if we reached our goal state
            return path
        else:
            if cur_node in visited:               #if current state has already been visited, we continue 
                continue
            else:
                visited.add(cur_node)          #else, we put the current state in the visited set
            successors = problem.getSuccessors(cur_node)
            for (succ, action, cost) in successors:                   
                new_path = path + [action]     #we add the action to the path
                stack.push((succ, new_path))   
  
    util.raiseNotDefined()

def breadthFirstSearch(problem: SearchProblem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    visited = set()
    queue = util.Queue()
    start = problem.getStartState()   #we get the start point
    queue.push((start, []))      #push the start state into the empty queue

    while queue.isEmpty() == False:
        cur_node, path = queue.pop()
        if (problem.isGoalState(cur_node) == True):    #checks if we reached our goal state
            return path
        else:
            if cur_node in visited:               #if current state has already been visited, we continue 
                continue
            else:
                visited.add(cur_node)          #else, we put the current state in the visited set
            successors = problem.getSuccessors(cur_node)
            for (succ, action, cost) in successors:                   
                new_path = path + [action]     #add action to the current path
                queue.push((succ, new_path))   
                
    util.raiseNotDefined()

def uniformCostSearch(problem: SearchProblem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    pqueue = util.PriorityQueue()
    visited = set()
    start = problem.getStartState()
    cost = {start : 0}   #dictionary which stores for each state the total cost to get there, it uses the state coordinates as a key
    pqueue.push([start, None, 0], 0) 
    path = []
    par = {}          #dictionary that stores the parent of each state, we use the state as the key

    while(1):
        cur_cost = 0  

        if pqueue.isEmpty():
            return -1
        cur_node = pqueue.pop()

        if problem.isGoalState(cur_node[0]):
            break
        else:
            if cur_node[0] in visited:
                continue

            visited.add(cur_node[0])

            for state in problem.getSuccessors(cur_node[0]):
                cur_cost = cost[cur_node[0]] + state[2]  
                if state[0] not in visited and state not in pqueue.heap:
                    par[state] = cur_node          #update successor parent
                    cost[state[0]] = cur_cost      #update total cost to get to the successor
                    pqueue.push(state, cur_cost)   

                elif state in pqueue.heap:
                    if cur_cost < cost[state[0]]: #check if we found a path with a smaller cost, if yes we update the cost of the node on the dictionary
                        cost[state[0]] = cur_cost
                        par[state] = cur_node

    end = cur_node

    #we find the path by moving backwards to the parent of each node till we reach the start state
    while end != None:    
        if end[0] == start:
            end = None
        else:
            path.append(end[1])    #put the action into the path list
            end = par[end]      #we move to the previous (parent) state

    path.reverse()                     
    return path 
    
    util.raiseNotDefined()

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem: SearchProblem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    pqueue = util.PriorityQueue()
    visited = set()
    start = problem.getStartState()
    cost = {start : heuristic(start, problem)}
    pqueue.push([start, None, 0], 0)
    path = []
    par = {}

    while(1):

        cur_cost = 0
        Ascore = 0

        if pqueue.isEmpty() == True:
            return -1

        cur_node = pqueue.pop()
        
        if (problem.isGoalState(cur_node[0]) == True):
            break
        else:
            if cur_node[0] in visited:
                continue

            visited.add(cur_node[0])

            for state in problem.getSuccessors(cur_node[0]):
                cur_cost = cost[cur_node[0]] + state[2]  
                Ascore = cur_cost + heuristic(state[0], problem)  #Ascor is the current cost plus the heuristic value

                if state[0] not in visited and state not in pqueue.heap:
                    par[state] = cur_node
                    cost[state[0]] = cur_cost
                    pqueue.push(state, Ascore)

                elif state in pqueue.heap:
                    if cur_cost < cost[state[0]]:
                        cost[state[0]] = cur_cost
                        par[state] = cur_node

    end = cur_node    
    #we find the path by moving backwards to the parent of each node until we reach the start state
    while end != None:   
        if end[0] == start:
            end = None
        else:
            path.append(end[1])    #we put the action into the path list
            end = par[end]      #we move to the previous (parent) state
            
    path.reverse()                    
    return path 

    util.raiseNotDefined()


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
