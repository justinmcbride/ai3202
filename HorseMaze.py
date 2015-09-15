from collections import defaultdict
TILE_NORMAL = 0
TILE_MOUNTAIN = 1
TILE_WALL = 2

COST_ADJACENT = 10
COST_DIAGONAL = 14
COST_MOUNTAIN = 10

class Node:
  def __init__(self, parent, loc):
    self.parent = parent
    self.loc = loc
    self.f = None
    self.g = None
    self.h = None
  def __str__(self):
    return "Node(parent={},loc={},f={},g={},h={}".format(self.parent, self.loc, self.f, self.g, self.h)

def NodeToPath(node):
  if node.parent == None:
    return "{}".format(node.loc)
  else:
    return "{} => {}".format(NodeToPath(node.parent), node.loc)

def manhattanDistances(world, (goalX, goalY)):
  distances = {}
  for i, row in enumerate(world):
    for j, col in enumerate(row):
      distances[(i,j)] = abs(goalX-i) + abs(goalY-j)
  return distances

def manhattanDistance( (startX, startY), (goalX, goalY) ):
  return abs(goalX-startX) + abs(goalY-startY)

def minCost(l):
  #todo: handle ties with <=
  # print("--Finding minCostNode")
  minCost = float("inf")
  node = None
  for item in l:
    if item.f < minCost:
      minCost = item.f
      node = item
      # print("--New minCost: ({}) : {}".format(node.loc,minCost))
  # print("--!Found min = {}".format(str(node)))
  return node

def lowerCostExists(l, n):
  # print("--in lowerCostExists..")
  # print("--f = , l= {}".format(f,",".join([str(x.loc) for x in l])))
  for item in l:
    if item.f < n.f and item.loc == n.loc:
      # print("--!found lower cost")
      return True
  # print("--! didn't find lower cost")
  return False

def aStar(world, start, goal):
  lOpen = []
  lClosed = []

  rootNode = Node(None, start)
  rootNode.h = manhattanDistance(start, goal)
  rootNode.g = 0
  rootNode.f = rootNode.h
  lOpen.append(rootNode)
  # print("Starting search..")
  # print("lOpen= " + ",".join([str(x) for x in lOpen]))
  while len(lOpen) != 0:
    # print("In loop.. len(lOpen) = {}".format(len(lOpen)))
    minCostNode = minCost(lOpen)
    lOpen.remove(minCostNode)
    if minCostNode == goal:
      # print("mincostnode is goal.. breaking")
      return minCostNode
    lClosed.append(minCostNode)
    for (nextLocation,cost) in world[minCostNode.loc]:
      # print("-in foor loop.. nextloc = {}, cost = {}".format(nextLocation, cost))
      
      nextNode = Node(minCostNode, nextLocation)
      nextNode.g = minCostNode.g + cost
      nextNode.h = manhattanDistance(nextNode.loc, goal)
      nextNode.f = nextNode.g + nextNode.h
      # print("potentialnextnode = {}".format(nextNode))
      if nextLocation == goal:
        # print ("--!nextlocation is goal.. breaking")
        return nextNode

      if lowerCostExists(lOpen, nextNode) or lowerCostExists(lClosed, nextNode):
        # print("~~some lower cost exists.. not adding node to open")
        pass
      else:
        lOpen.append(nextNode)
    lClosed.append(minCostNode)
  return "couldn't get there"

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
        # print("[" + str(row) + "," + str(col) + "] = " + e)
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
      # if (row-1) >= 0:
      #   neighbors.append((row-1,col-1)) #upleft
      # if (row+1) < maxRow:
      #   neighbors.append((row+1,col-1)) #downleft
    if (col+1) < maxCol:
      neighbors.append((row,col+1)) #right
      # if (row-1) >= 0:
      #   neighbors.append((row-1,col+1)) #upright
      # if (row+1) < maxRow:
      #   neighbors.append((row+1,col+1)) #downright
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
      for n in diagonalTiles(i,j,rows,cols):
        nX = n[0]
        nY = n[1]
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


(world1,r1,c1) = readWorld("World1.txt")
(world2,r2,c2) = readWorld("World2.txt")

worldMap1 = parseWorld(world1,r1,c1)
worldMap2 = parseWorld(world2,r2,c2)
path = aStar(worldMap1, (7,0), (0,9) )
print NodeToPath(path)
path2 = aStar(worldMap2, (7,0), (0,9) )
print NodeToPath(path2)
