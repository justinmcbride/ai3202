from collections import defaultdict
import sys
import getopt

DEFAULT_FILE = "World1MDP.txt"
DEFAULT_EPSILON = 0.5

#Constants as defined by the assignment specfication

TILE_NORMAL = 0
TILE_MOUNTAIN = 1
TILE_WALL = 2
TILE_SNAKE = 3
TILE_BARN = 4
TILE_GOAL = 50

REWARD_NORMAL = 0
REWARD_BARN = 1
REWARD_APPLE = 50
REWARD_SNAKE = -2
REWARD_MOUNTAINS = -1

MOVE_SUCCESS = 0.8
MOVE_FAIL_LEFT = 0.1
MOVE_FAIL_RIGHT = 0.1

GAMMA = 0.9

class DIR_UP:
  pass
class DIR_DOWN:
  pass
class DIR_LEFT:
  pass
class DIR_RIGHT:
  pass
class DIR_GOAL:
  pass

class World:
  def __init__(self, in_map, rows, cols):
    self.map = in_map
    self.rows = rows
    self.cols = cols

  def NodeAt(self, row, col):
    return self.map[row][col]

class Node:
  def __init__(self, loc, tiletype):
    self.position = loc
    self.type = tiletype

    if tiletype == TILE_GOAL:
      self.utility = 50
      self.bestDirection = DIR_GOAL
    else:
      self.utility = 0
      self.bestDirection = None

    if (tiletype == TILE_NORMAL or tiletype == TILE_WALL):
      self.reward = REWARD_NORMAL
    elif (tiletype == TILE_MOUNTAIN): 
      self.reward = REWARD_MOUNTAINS
    elif (tiletype == TILE_SNAKE): 
      self.reward = REWARD_SNAKE
    elif (tiletype == TILE_BARN):
      self.reward = REWARD_BARN

  def __str__(self):
    return "Node: Location={},utility={},direction={}".format(self.position, self.utility, self.bestDirection)

# Use recursion and induction to print out the path
def NodeToPath(node):
  if node.parent == None:
    return "{}".format(node.pos)
  else:
    return "{} => {}".format(NodeToPath(node.parent), node.pos)

def Utility(world, node):
  # These two cases should not be inspected
  if node.type == TILE_WALL:
    return None
  if node.type == TILE_GOAL:
    return None

  (row, col) = node.position
  # Retrieve the utility of all possible moves
  util_up = (world.NodeAt(row-1,col).utility) if ((row-1) >= 0) else 0
  util_down = (world.NodeAt(row-1,col).utility) if ((row+1) < world.rows) else 0
  util_left = (world.NodeAt(row,col-1).utility) if ((col-1) >= 0) else 0
  util_right = (world.NodeAt(row,col+1).utility) if ((col+1) < world.cols) else 0

  # Calculate the expected utilities for each move
  eu_up = (MOVE_SUCCESS * util_up) + (MOVE_FAIL_RIGHT * util_right) + (MOVE_FAIL_LEFT * util_left)
  eu_down = (MOVE_SUCCESS * util_down) + (MOVE_FAIL_RIGHT * util_left) + (MOVE_FAIL_LEFT * util_right)
  eu_left = (MOVE_SUCCESS * util_left) + (MOVE_FAIL_RIGHT * util_down) + (MOVE_FAIL_LEFT * util_up)
  eu_right = (MOVE_SUCCESS * util_right) + (MOVE_FAIL_RIGHT * util_up) + (MOVE_FAIL_LEFT * util_down)

  maxEU = float("-inf")
  if eu_up > maxEU:
    maxEU = eu_up
    node.bestDirection = DIR_UP
  if eu_down > maxEU:
    maxEU = eu_down
    node.bestDirection = DIR_DOWN
  if eu_left > maxEU:
    maxEU = eu_left
    node.bestDirection = DIR_LEFT
  if eu_right > maxEU:
    maxEU = eu_right
    node.bestDirection = DIR_RIGHT

  newUtility = node.reward + (GAMMA * maxEU)
  delta = abs(node.utility - newUtility)

  node.utility = newUtility

  return delta

def MDP(world, epsilon):
  delta = float("inf")
  while (delta > (epsilon*( (1-GAMMA)/GAMMA) ) ):
    delta = 0
    for row in reversed(world.map):
      for node in reversed(row):
        newDelta = Utility(world, node)
        if newDelta > delta:
          delta = newDelta

def ShortestPath(world, startX, startY):
  row = startY
  col = startX

  node = world.NodeAt(row,col)
  while node.bestDirection != DIR_GOAL:
    print node
    if node.bestDirection == DIR_UP:
      row += 1
    elif node.bestDirection == DIR_DOWN:
      row -= 1
    elif node.bestDirection == DIR_LEFT:
      col -= 1
    elif node.bestDirection == DIR_RIGHT:
      col += 1
    node = world.NodeAt(row, col)

def readWorld(filename):
  world = []
  nRow = 0
  nElems = 0
  with open(filename, 'r') as f:
    for row, line in enumerate(f):
      currentRow = []
      col = 0
      line = line.strip("\n")
      elems = line.split(' ')
      if ((row != 0) and len(elems) != nElems):
        break
      nElems = len(elems)
      for e in elems:
        currentRow.append( Node( (nRow,col), int(e) ) )
        col += 1
      world.append(currentRow)
      nRow += 1
  return World(world, nRow, nElems)

def main(argv):
  worldFile = DEFAULT_FILE
  epsilon = DEFAULT_EPSILON
  
  try:
    opts, args = getopt.getopt(argv, "e:w:", ["world="])
  except getopt.GetoptError:
    sys.exit(2)
  for opt, arg in opts:
    if opt in ("-w", "--world"):
      worldFile = arg
    if opt in ("-e", "--epsilon"):
      epsilon = arg

  print("Using world file: " + worldFile)
  print("Using epsilon: " + str(epsilon))

  world = readWorld(worldFile)
  
  print("Calculating MDP...")
  MDP(world, epsilon)
  print("...Done")

  print("Best path:")
  ShortestPath(world, 0, 7)

if __name__ == '__main__':
  main(sys.argv[1:])
