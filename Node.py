from globals import MCTSConstant, white, black
import random
import copy
import math

class Node:
    def __init__(self, grid, player, parent = None,  move = None, availableMoves = None):
        self.grid = grid
        self.player = player
        self.parent = parent
        self.move = move
        self.children = []
        self.visits = 0
        self.weight = 0

        self.availableMoves = availableMoves
        self.untriedMoves = self.availableMoves.findAvailMoves(self.grid, self.player)

    def UCTSearch(self, initialState, player, availableMoves, iterations = 500):
        root = Node(grid = initialState, player = player, availableMoves = availableMoves)

        for i in range(iterations):
            node = self.TreePolicy(root)
            reward = self.DefaultPolicy(node.grid, node.player, root.player, availableMoves)
            self.Backup = (node, reward)
        
        return self.BestChild(root, 0).move
    
    def TreePolicy(self, node):
        while not self.isTerminal(node.grid, node.player, node.availableMoves):
            if len(node.untriedMoves) > 0:
                return self.Expand(node)
            else:
                node = self.BestChild(node, MCTSConstant)
        return node
    
    def Expand(self, node):
        move = random.choice(node.untriedMoves)
        node.untriedMoves.remove(move)

        newGrid = copy.deepcopy(node.grid)
        y, x = move
        newGrid[y][x] = node.player

        tilesToSwap = node.availableMoves.swappableTiles(y, x, newGrid, node.player)
        for tile in tilesToSwap:
            newGrid[tile[0]][tile[1]] = node.player
        
        if node.player == black:
            nextPlayer = white
        else:
            nextPlayer = black

        if not node.availableMoves.findAvailMoves(newGrid, nextPlayer):
            nextPlayer = node.player
        
        newNode = Node(grid = newGrid, player = nextPlayer, parent = node, move = move, availableMoves = node.availableMoves)
        node.children.append(newNode)
        return newNode
    
    def BestChild(self, node, const):
        bestScore = -float('inf')
        bestChildren = []

        for child in node.children:
            if child.visits == 0:
                score = float('inf')
            else:
                exploit = child.weight / child.visits
                explore = const * math.sqrt(math.log(node.visits) / child.visits) 
                score = exploit + explore
            
            if score > bestScore:
                bestScore = score
                bestChildren = [child]
            elif score == bestScore:
                bestChildren.append(child)
        
        return random.choice(bestChildren)
    
    def DefaultPolicy(self, grid, playerTurn , rootPlayer, availableMoves):
        currentGrid = copy.deepcopy(grid)
        currentPlayer = playerTurn

        while True:
            moves = availableMoves.findAvailMoves(currentGrid, currentPlayer)

            if not moves:
                if currentPlayer == black:
                    nextPlayer = white
                else:
                    nextPlayer = black
                if not availableMoves.findAvailMoves(currentGrid, nextPlayer):
                    break
                else:
                    currentPlayer = nextPlayer
                    continue
            
            move = random.choice(moves)
            y, x = move
            currentGrid[y][x] = currentPlayer
            tilesToSwap = availableMoves.swappableTiles(y, x, currentGrid, currentPlayer)
            for tile in tilesToSwap:
                currentGrid[tile[0]][tile[1]] = currentPlayer
            
            if currentPlayer == black:
                currentPlayer = white
            else:
                currentPlayer = black
        
        whites = sum(row.count(white) for row in currentGrid)
        blacks = sum(row.count(black) for row in currentGrid)

        if whites > blacks:
            winner = white
        elif whites < blacks:
            winner = black
        else:
            return 0

        if (winner == rootPlayer):
            return 1
        else:
            return -1
    
    def Backup(self, node, reward):
        while node is not None:
            node.visits += 1
            node.weight += reward
            node = node.parent
    
    def isTerminal(self, grid, player, availableMoves):
        moves = availableMoves.findAvailMoves(grid, player)
        if player == black:
            nextPlayer = white
        else:
            nextPlayer = black
        nextMoves = availableMoves.findAvailMoves(grid, nextPlayer)
        return len(moves) == 0 and len(nextMoves) == 0
        
