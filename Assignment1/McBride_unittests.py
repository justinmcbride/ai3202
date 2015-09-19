import unittest
from McBride_BinaryTree import *
from McBride_Queue import *
from McBride_Stack import *
from McBride_Graph import *

class test_Queue(unittest.TestCase):
  def testPut(self):
    q = Queue()
    self.assertTrue( q.Put(5) )
    self.assertTrue( q.Put(-50000) )
    self.assertFalse( q.Put('fail') )
    self.assertFalse( q.Put([0,1]) )

  def testSize(self):
    q = Queue()
    self.assertEquals( 0, q.Size() )
    for x in xrange(0,5):
      q.Put(x)
    self.assertEquals( 5, q.Size() )
    q.Get()
    q.Get()
    self.assertEquals( 3, q.Size() )

  def testGet(self):
    q = Queue()
    self.assertIsNone( q.Get())
    for x in xrange(0,10):
      q.Put(x)
    for x in xrange(0,10):
      self.assertEquals( q.Get(), x )

class test_Stack(unittest.TestCase):
  def testPush(self):
    s = Stack()
    self.assertTrue( s.push(1) )
    self.assertTrue( s.push(10000) )
    self.assertTrue( s.push(-1000) )
    self.assertFalse( s.push('failure') )
  def testPop(self):
    s = Stack()
    self.assertIsNone(s.pop())
    for x in xrange(0,10):
      s.push(x)
    for x in xrange(10, 0):
      self.assertEquals( s.pop(), x )
  def testSize(self):
    s = Stack()
    self.assertEquals( s.checkSize(), 0 )
    for x in xrange(0,10):
      s.push(x)
    self.assertEquals( s.checkSize(), 10 )
    for x in xrange(0,5):
      s.pop()
    self.assertEquals( s.checkSize(), 5 )

class test_BinaryTree(unittest.TestCase):
  def testAdd(self):
    root = 7
    bt = BinaryTree(root)

    # add two nodes to the root
    self.assertTrue(bt.add(5, root))
    self.assertTrue(bt.add(6, root))
    # trying to add a third should fail
    self.assertFalse(bt.add(8, root))

    # test adding to a child
    self.assertTrue(bt.add(9, 5))

  def testDelete(self):
    bt = BinaryTree(1)
    bt.add(2, 1)
    bt.add(3, 1)
    bt.add(4, 2)
    bt.add(5, 3)
    bt.add(6, 3)
    bt.add(7, 6)

    # try to delete non-empty node
    self.assertFalse( bt.delete(3) )
    # delete them in reverse order
    self.assertTrue( bt.delete(7) )
    self.assertTrue( bt.delete(6) )
    self.assertTrue( bt.delete(5) )
    self.assertTrue( bt.delete(4) )
    self.assertTrue( bt.delete(3) )
    self.assertTrue( bt.delete(2) )

  def testPrint(self):
    bt = BinaryTree(1)
    bt.add(2, 1)
    bt.add(3, 1)
    bt.add(4, 2)
    bt.add(5, 3)
    bt.add(6, 3)
    bt.add(7, 6)
    expectedS = "1243567"
    s = bt.doPrint()
    self.assertEquals( s, expectedS )

class test_Graph(unittest.TestCase):
  def testAddVertex(self):
    g = Graph()
    self.assertTrue( g.addVertex(1) )
    self.assertTrue( g.addVertex(2) )
    self.assertTrue( g.addVertex(5) )
    self.assertFalse( g.addVertex(5) )
    self.assertFalse( g.addVertex(2) )

  def testAddEdge(self):
    g = Graph()
    g.addVertex(1)
    g.addVertex(2)
    g.addVertex(3)
    g.addVertex(4)
    self.assertTrue( g.addEdge(1, 2) )
    self.assertTrue( g.addEdge(3, 4) )
    self.assertTrue( g.addEdge(1, 4) )
    self.assertFalse( g.addEdge(1, 5) )
    self.assertFalse( g.addEdge(7, 3) )

  def testFindVertex(self):
    g = Graph()
    g.addVertex(1)
    g.addVertex(2)
    g.addVertex(3)
    g.addVertex(4)
    g.addVertex(5)
    g.addEdge(1, 2)
    g.addEdge(3, 4)
    g.addEdge(1, 4)

    self.assertEquals( [2,4], g.findVertex(1) )
    self.assertEquals( [4], g.findVertex(3) )
    self.assertEquals( [], g.findVertex(5) )

    self.assertIsNone( g.findVertex(6) )

if __name__ == '__main__':
  unittest.main()