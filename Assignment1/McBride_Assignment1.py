from McBride_BinaryTree import *
from McBride_Queue import *
from McBride_Stack import *
from McBride_Graph import *

'''
I have implemented all the classes in seperate files
for clarity. Additionally, I was doing unit testing
before I saw problem 5, which asks for tests....
So those are here too...
Unit tests are run with $python McBride_unittests.py

Everything in this file is just for problem 5
'''
def main():
  # Problem 5, part a
  #   Testing the queue
  #   Adding 15 ints, then dequeing them and printing
  print("---------")
  print("-Prob 5a-")
  print("---------")
  q = Queue()
  for i in xrange(0, 15):
    q.Put(i)
  for _ in xrange(0, 15):
    print(q.Get())
  del q

  # Problem 5, part b
  #   Testing the stack
  #   Adding 15 ints, then popping and printing them
  print("---------")
  print("-Prob 5b-")
  print("---------")
  s = Stack()
  for i in xrange(0, 15):
    s.push(i)
  for _ in xrange(0, 15):
    print(s.pop())
  del s

  # Problem 5, part c
  #   Testing the tree
  #   Adding 10 ints as nodes,
  #   printing the tree
  #   deleting two
  #   priting the tree again
  print("---------")
  print("-Prob 5c-")
  print("---------")
  bt = BinaryTree(5)
  bt.add(1, 5)
  bt.add(2, 5)
  bt.add(3, 2)
  bt.add(7, 2)
  bt.add(4, 1)
  bt.add(6, 1)
  bt.add(8, 6)
  bt.add(9, 7)
  bt.add(10, 7)
  bt.add(15, 10)
  print("After adds:")
  bt.doPrint()

  bt.delete(15)
  bt.delete(8)
  print("After deletes:")
  bt.doPrint()

  del bt

  # Problem 5, part d
  #   Testing the graph
  #   Adding 10 ints as vertices,
  #   adding 20 edges
  #   finding 5 vertices
  print("---------")
  print("-Prob 5d-")
  print("---------")
  g = Graph()
  for i in xrange(0,10):
    g.addVertex(i)

  g.addEdge(1, 2)
  g.addEdge(1, 3)
  g.addEdge(1, 4)
  g.addEdge(1, 5)
  g.addEdge(1, 6)
  g.addEdge(1, 7)
  g.addEdge(1, 8)
  g.addEdge(1, 9)
  g.addEdge(2, 5)
  g.addEdge(2, 6) # 10 edges..
  g.addEdge(2, 7)
  g.addEdge(2, 8)
  g.addEdge(3, 9)
  g.addEdge(3, 4)
  g.addEdge(3, 5) # 15 edges...
  g.addEdge(3, 6)
  g.addEdge(3, 7)
  g.addEdge(3, 8)
  g.addEdge(3, 0)
  g.addEdge(5, 8) # 20 edges

  print("Vertex 1: ")
  g.findVertex(1)
  print("Vertex 3: ")
  g.findVertex(3)
  print("Vertex 6: ")
  g.findVertex(6)
  print("Vertex 9: ")
  g.findVertex(9)
  print("Vertex 0: ")
  g.findVertex(0)
  print("Vertex 5: ")
  g.findVertex(5)

if __name__ == '__main__':
  main()