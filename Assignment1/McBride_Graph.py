'''
It wasn't specified whether the graph is directed
or not, but I'm assuming that it's UNDIRECTED. Thus,
adding an edge goes both ways. But it's also toggleable
with the 'directed' parameter..
'''
class Graph:
  def __init__(self, directed = False):
    self.values = {}
    self.directed = directed

  ''' addVertex(value)
  Add the vertex to the internal dictionary with
  a blank list of edges
  '''
  def addVertex(self, value):
    if value in self.values:
      print("Vertex already exists")
      return False
    self.values[value] = []
    return True

  ''' addEdge(value1, value2)
  Check to see that both values are in the graph,
  and then add the edge, only adding it from
  VAL1 -> VAL2 if the graph is DIRECTED.
  '''
  def addEdge(self, value1, value2):
    if any([
      value1 not in self.values,
      value2 not in self.values
      ]):
      print("One or more vertices not found.")
      return False
    self.values[value1].append(value2)
    if not self.directed:
      self.values[value2].append(value1)
    return True

  ''' findVertex(value)
  Retrieve the list of edges if the vertex exists
  '''
  def findVertex(self, value):
    if value in self.values:
      print self.values[value]
      return self.values[value]
    else:
      return None