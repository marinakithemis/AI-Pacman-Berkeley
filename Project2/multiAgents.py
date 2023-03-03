# multiAgents.py
# --------------
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


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent
from pacman import GameState

class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """


    def getAction(self, gameState: GameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState: GameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"
        food_dist = 0
        food_distnew = 0
        score = successorGameState.getScore() + max(newScaredTimes)
        ghostpos = successorGameState.getGhostPositions() 

        for food in newFood.asList():     #we find the manhattan distance between our new position and the closest food
            food_distnew = manhattanDistance(newPos, food)

            if food_dist == 0:
                food_dist = food_distnew

            if food_distnew < food_dist:
                food_dist = food_distnew

        if food_dist < 2:              #we give a motive to pacman to move closer to food
            score += 10
        else:
            score += 1/food_dist       #the shorter the fdist, the higher the score

        for ghost in ghostpos:     #if after a specific action the ghost is really close, we don't choose that action 
            gdist = manhattanDistance(newPos, ghost)
            if gdist < 2:
                score = -100000

        return score
            


def scoreEvaluationFunction(currentGameState: GameState):
    """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the Pacman GUI.

    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
    This class provides some common elements to all of your
    multi-agent searchers.  Any methods defined here will be available
    to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

    You *do not* need to make any changes here, but you can if you want to
    add functionality to all your adversarial search agents.  Please do not
    remove anything, however.

    Note: this is an abstract class: one that should not be instantiated.  It's
    only partially specified, and designed to be extended.  Agent (game.py)
    is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
    Your minimax agent (question 2)
    """
    def minimax(self, gamestate : GameState, depth, agentindex):   #it returns a tuple with the best value and action


        agents = gamestate.getNumAgents()
        if gamestate.isWin() == True or gamestate.isLose() == True or depth == self.depth:
            return (self.evaluationFunction(gamestate), None)

        if agentindex == 0:     #max/pacman

            actions = gamestate.getLegalActions(0)
            maxeval = float('-inf')
            agentindex = 1

            for action in actions:
                succ = gamestate.generateSuccessor(0, action)
                eval = self.minimax(succ, depth , agentindex)   #we call minimax function for its successors
                if eval[0] > maxeval:
                    maxeval = eval[0]
                    bestmove = action
            return (maxeval, bestmove)

        else:                     #min/ ghosts

            mineval = float('+inf')
            actions = gamestate.getLegalActions(agentindex)

            for action in actions:
                succ = gamestate.generateSuccessor(agentindex, action)
                if agentindex == agents - 1 :    #if we reached the final ghost we should call minimax function for pacman (agentindex = 0)
                    eval = self.minimax(succ, depth + 1 , 0)
                else:
                    eval = self.minimax(succ, depth , agentindex + 1)   #else we call minimax function for all the other ghosts
                if eval[0] < mineval:
                    mineval = eval[0]
                    bestmove = action

            return(mineval, bestmove)

    def getAction(self, gameState: GameState):
        """
        Returns the minimax action from the current gameState using self.depth
        and self.evaluationFunction.

        Here are some method calls that might be useful when implementing minimax.

        gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

        gameState.generateSuccessor(agentIndex, action):
        Returns the successor game state after an agent takes an action

        gameState.getNumAgents():
        Returns the total number of agents in the game

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"
        best = self.minimax(gameState, 0, 0)     #we call the minimax function for pacman
        return best[1]                           #we return the best action

        util.raiseNotDefined()

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """
    def abminimax(self, gamestate : GameState, depth, agentindex, a, b):    #implementation of minimax with ab pruning, again we return a tuple with the best value and action

        agents = gamestate.getNumAgents()
        if gamestate.isWin() == True or gamestate.isLose() == True or depth == self.depth:
            return (self.evaluationFunction(gamestate), None)

        if agentindex == 0:     #max/pacman

            actions = gamestate.getLegalActions(0)
            maxeval = float('-inf')
            agentindex = 1

            for action in actions:
                succ = gamestate.generateSuccessor(0, action)
                eval = self.abminimax(succ, depth , agentindex, a, b) #we call abminimax function for its successors
                if eval[0] > maxeval:
                    maxeval = eval[0]
                    bestmove = action
                if maxeval > b:
                    return (maxeval, bestmove)
                a = max(a, maxeval)

            return (maxeval, bestmove)

        else:                     #min/ ghosts

            mineval = float('+inf')
            actions = gamestate.getLegalActions(agentindex)

            for action in actions:
                succ = gamestate.generateSuccessor(agentindex, action)

                if agentindex == agents - 1 :           #if we reached the final ghost we should call abminimax function for pacman (agentindex = 0)
                    eval = self.abminimax(succ, depth + 1 , 0, a, b)
                else:
                    eval = self.abminimax(succ, depth , agentindex + 1, a, b)
                if eval[0] < mineval:
                    mineval = eval[0]
                    bestmove = action 
                if mineval < a:
                    return (mineval, bestmove)

                b = min(b, mineval)

            return(mineval, bestmove)

    def getAction(self, gameState: GameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        a = float('-inf')
        b = float('+inf')
        best = self.abminimax(gameState, 0, 0, a, b)     #we call the abminimax function for pacman
        return best[1]                                   #we return the best action
        util.raiseNotDefined()

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """
    def expectimax(self, gamestate : GameState, depth, agentindex):


        agents = gamestate.getNumAgents()
        if gamestate.isWin() == True or gamestate.isLose() == True or depth == self.depth:
            return (self.evaluationFunction(gamestate), None)

        if agentindex == 0:     #max/pacman, same as the minimax one

            actions = gamestate.getLegalActions(0)
            maxeval = float('-inf')
            agentindex = 1

            for action in actions:
                succ = gamestate.generateSuccessor(0, action)
                eval = self.expectimax(succ, depth , agentindex)
                if eval[0] > maxeval:
                    maxeval = eval[0]
                    bestmove = action

            return (maxeval, bestmove)

        else:                     #min/ ghosts

            mineval = 0
            actionnum = 0         #we need this to calculate the number of total actions
            actions = gamestate.getLegalActions(agentindex)

            for action in actions:
                actionnum += 1
                succ = gamestate.generateSuccessor(agentindex, action)

                if agentindex == agents - 1 :
                    eval = self.expectimax(succ, depth + 1 , 0)
                    mineval = mineval + eval[0]   #we calculate the total of all the values
                    bestmove = action
                else:
                    eval =  self.expectimax(succ, depth , agentindex + 1)
                    mineval = mineval + eval[0]
                    bestmove = action

            mineval = mineval / actionnum       #mineval is the average value

            return(mineval, bestmove)

    def getAction(self, gameState: GameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        "*** YOUR CODE HERE ***"
        best = self.expectimax(gameState, 0, 0)     
        return best[1]
        util.raiseNotDefined()

def betterEvaluationFunction(currentGameState: GameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    totalscore, count, countf, fdist, fdistmax = 0, 0, 0, 0, 0
    pos = currentGameState.getPacmanPosition()
    food = currentGameState.getFood()
    ghost = currentGameState.getGhostStates()
    ghostpos = currentGameState.getGhostPositions()
    newscared = [ghostState.scaredTimer for ghostState in ghost]
    score = currentGameState.getScore() + 0.51*max(newscared)   #0.51 occured after many tests in order to optimize the score

    if currentGameState.isWin() ==  True:    #if state is a winning state then the score is maximized
        score = 1000000
        return score

    elif currentGameState.isLose() == True:  #if state is a losing state, then the score is minimized
        score = -1000000
        return score

    for food in food.asList():
        fdist = manhattanDistance(food, pos)   #we find the manhattan distance to the closest food
        if fdistmax == 0:
            fdistmax = fdist
        elif fdist < fdistmax:
            fdistmax = fdist

    if fdist < 3:          #if food is really close, we give a bonus to the state's score
        score += 10
    if fdistmax != 0:      #check if it is !=0 so that we can divide
        score += 1/fdistmax 

    for ghost in ghostpos:
        gdist = manhattanDistance(pos, ghost)
        if gdist < 1:     #if there is a ghost then, score is minimized so that we don't choose that state
            score = -4839434
            return score
        elif gdist < 3:   #if there is a ghost close to our state, then we reduce our score
            score -= 100
            
    return score

    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction
