class Stack:
  def __init__(self):
    self.items = []

  ''' push(item)
  Add the item to the list, if it's an integer
  '''
  def push(self, item):
    if type(item) is not int:
      return False
    self.items.append(item)
    return True

  ''' pop()
  Retrieve the integer at the end of the list
  '''
  def pop(self):
    if len(self.items) == 0:
      return None
    return self.items.pop()

  ''' checkSize()
  Return the size of the stack
  '''
  def checkSize(self):
    return len(self.items)