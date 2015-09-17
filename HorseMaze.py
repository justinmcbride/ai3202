from collections import defaultdict
import sys
import getopt

TILE_NORMAL = 0
TILE_MOUNTAIN = 1
TILE_WALL = 2

COST_ADJACENT = 10
COST_DIAGONAL = 14
COST_MOUNTAIN = 10

class Node:
  def __init__(self, parent, loc):
    self.parent = parent
    self.pos = loc
    self.f = None
    self.g = None
    self.h = None
  def __str__(self):
    return "Node(loc={},f={},g={},h={}".format(self.pos, self.f, self.g, self.h)

class Heuristic:
  selected = None
  @staticmethod
  def Manhattan( (startX, startY), (goalX, goalY) ):
    return (abs(goalX-startX) + abs(goalY-startY)) * 10
  @staticmethod
  def Custom( (startX, startY), (goalX, goalY) ):
    x = abs(startX-goalX)
    y = abs(startY-goalY)
    if x > y:
      return 14*y + 10*(x-y)
    else:
      return 14*x + 10*(y-x)

def NodeToPath(node):
  if node.parent == None:
    return "{}".format(node.pos)
  else:
    return "{} => {}".format(NodeToPath(node.parent), node.pos)

def minCost(l):
  #todo: handle ties with <=
  minCost = float("inf")
  node = None
  for item in l:
    if item.f < minCost:
      minCost = item.f
      node = item
  return node


def lowerCostExists(l, n):
  for item in l:
    if item.f < n.f and item.pos == n.pos:
      return True
  return False

def aStar(world, start, goal):
  lOpen = []
  lClosed = []

  rootNode = Node(None, start)
  rootNode.h = Heuristic.selected(start, goal)
  rootNode.g = 0
  rootNode.f = rootNode.h
  lOpen.append(rootNode)
  print("Starting search..")
  while len(lOpen) != 0:
    currentNode = minCost(lOpen)
    lOpen.remove(currentNode)
    if currentNode == goal:
      return currentNode
    lClosed.append(currentNode)
    for (nextLocation,cost) in world[currentNode.pos]:      
      nextNode = Node(currentNode, nextLocation)
      nextNode.g = currentNode.g + cost
      nextNode.h = Heuristic.selected(nextNode.pos, goal)
      nextNode.f = nextNode.g + nextNode.h
      if nextNode.pos == goal:
        return nextNode
      if lowerCostExists(lOpen, nextNode) or lowerCostExists(lClosed, nextNode):
        pass
      else:
        lOpen.append(nextNode)
    lClosed.append(currentNode)
  return None

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
        currentRow.append(int(e))
        col += 1
      world.append(currentRow)
      nRow += 1
  return (world, nRow, nElems)

def adjacentTiles(row, col, maxRow, maxCol):
  neighbors = []
  if col >= 0:
    if (col-1) >= 0:
      neighbors.append((row,col-1)) #left
    if (col+1) < maxCol:
      neighbors.append((row,col+1)) #right
  if row >= 0:
    if (row-1) >= 0:
      neighbors.append((row-1,col)) #up
    if (row+1) < maxRow:
      neighbors.append((row+1,col)) #down
  return neighbors

def diagonalTiles(row, col, maxRow, maxCol):
  neighbors = []
  if col-1 >= 0:
    if (row-1) >= 0:
      neighbors.append((row-1,col-1)) #upleft
    if (row+1) < maxRow:
      neighbors.append((row+1,col-1)) #downleft
  if (col+1) < maxCol:
    if (row-1) >= 0:
      neighbors.append((row-1,col+1)) #upright
    if (row+1) < maxRow:
      neighbors.append((row+1,col+1)) #downright
  return neighbors

def parseWorld(world, rows, cols):
  worldMap = defaultdict(set)
  for i in xrange(0,rows):
    #start of row
    for j in xrange(0, cols):
      #start of col
      for n in adjacentTiles(i,j,rows,cols):
        nX = n[0]
        nY = n[1]
        tileType = world[nX][nY]
        if tileType == TILE_NORMAL:
          worldMap[(i,j)].add( ((nX, nY),COST_ADJACENT) )
        elif tileType == TILE_MOUNTAIN:
          worldMap[(i,j)].add( ((nX, nY),COST_ADJACENT+COST_MOUNTAIN) )
        elif tileType == TILE_WALL:
          # don't need to add this
          pass
      for nX, nY in diagonalTiles(i,j,rows,cols):
        tileType = world[nX][nY]
        if tileType == TILE_NORMAL:
          worldMap[(i,j)].add( ((nX, nY),COST_DIAGONAL) )
        elif tileType == TILE_MOUNTAIN:
          worldMap[(i,j)].add( ((nX, nY),COST_DIAGONAL+COST_MOUNTAIN) )
        elif tileType == TILE_WALL:
          # don't need to add this
          pass
      #end of col
    #end of row
  return worldMap

def main(argv):
  (world1,r1,c1) = readWorld("World1.txt")
  (world2,r2,c2) = readWorld("World2.txt")
  Heuristic.selected = staticmethod(Heuristic.Manhattan)
  try:
    opts, args = getopt.getopt(argv, "h:", ["heuristic="])
  except getopt.GetoptError:
    sys.exit(2)
  for opt, arg in opts:
    if opt in ("-h", "--heuristic"):
      if arg == "manhattan" or arg == "Manhattan":
        Heuristic.selected = staticmethod(Heuristic.Manhattan)
      elif arg == "custom" or arg == "Custom":
        Heuristic.selected = staticmethod(Heuristic.Custom)
      else:
        print("No -h/--heuristic option specified.. Defaulting to Manhattan")
        Heuristic.selected = staticmethod(Heuristic.Manhattan)
  worldMap1 = parseWorld(world1,r1,c1)
  path = aStar(worldMap1, (7,0), (0,9) )
  print NodeToPath(path)
  print "Cost: " + str(path.g)

  worldMap2 = parseWorld(world2,r2,c2)
  path2 = aStar(worldMap2, (7,0), (0,9) )
  print NodeToPath(path2)
  print "Cost: " + str(path2.g)

if __name__ == '__main__':
  main(sys.argv[1:])
