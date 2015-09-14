class Tile:
  def __init__(self, loc):
    self.loc = loc

class Tile_Normal:
  def __init__(self, loc):
    self.loc = loc

class Tile_Mountain:
  def __init__(self, loc):
    self.loc = loc

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
        print("[" + str(row) + "," + str(col) + "] = " + e)
        currentRow.append(e)
        col += 1
      world.append(currentRow)
      nRow += 1
  return (world, nRow, nElems)


world1 = readWorld("World1.txt")
world2 = readWorld("World2.txt")