''' BinaryTreeNode
Structure is specified in assignment
'''
class BinaryTreeNode:
  def __init__(self, val, parent):
    self.key = val
    self.childLeft = None
    self.childRight = None
    self.parent = parent

class BinaryTree:
  def __init__(self, root):
    self.root = BinaryTreeNode(root, None)

  ''' find(value, node)
  Helper function to find a specfic node in the BinaryTree
  Recursively call down each branch because the tree is 
  not sorted. Returns None if the value can't be found
  '''
  def find(self, value, node=None):
    if node is None:
      node = self.root
    if node.key == value:
      return node
    else:
      if node.childLeft is not None:
        r = self.find(value, node.childLeft)
        if r is not None:
          return r
      if node.childRight is not None:
        r = self.find(value, node.childRight)
        if r is not None:
          return r  
    return None # the search will fall through here

  ''' add(value, parentValue)
  Add value to the tree only if parentValue exists,
  and its two children aren't taken.
  Add to left child if not taken, otherwise add to right.

  '''
  def add(self, value, parentValue):
    # First need to find the parentValue node
    # and see if it's a viable candidate to adds
    node = self.find(parentValue)
    if node is None:
      print("Parent not found")
      return False
    if node.childRight is not None and node.childLeft is not None:
        print("Parent has two children, node not added")
        return False

    # Time to do the actual appending
    if node.childRight is None and node.childLeft is None:
      # Condition one of add
      node.childLeft = BinaryTreeNode(value, node)
      return True
    elif node.childLeft is not None and node.childRight is None:
      # Condition two of add
      node.childRight = BinaryTreeNode(value, node)
      return True

  ''' delete(value)
  Searches for the value to delete, and if it exists
  and has no children, then remove it, also removing it
  from its parent
  '''
  def delete(self, value):
    node = self.find(value)
    if node is None:
      print("Node not found.")
      return False
    if node.childLeft is not None or node.childRight is not None:
      print("Node not deleted, has children")
      return False

    # At this point, we /should/ delete the node
    parentNode = node.parent
    if parentNode.childLeft.key == value:
      parentNode.childLeft = None
    elif parentNode.childRight.key == value:
      parentNode.childRight = None
    node = None
    return True


  ''' Print method

  -We can't name the function 'print' as defined
  in the assignment because print is a 
  reserved keyword

  -Implemented this to return the output as a string,
  so that I can unittest it

  -Added optional 'node' parameter, to both make
  it recursive but also has the side effect of
  allowing to print from any single node
  '''
  def doPrint(self, node = None, top = True):
    s = ""
    if node is None:
      node = self.root

    s += str(node.key) + ","

    if node.childLeft is not None:
      s += self.doPrint(node.childLeft, top=False)
    if node.childRight is not None:
      s += self.doPrint(node.childRight, top=False)
    if top:
      print(s)
    return s