import Queue as OriginalQueue

'''
The instructions for the Problem 1 were quite
  vague, so I just wrapped a Python queue
  into my own class, and simplified it
'''
class Queue:
  def __init__(self):
    self.queue = OriginalQueue.Queue()

  ''' Put(item)
  I limited the items to integers,
  fail when it's full,
  or otherwise just add it.
  '''
  def Put(self, item):
    if type(item) is not int:
      return False
    if self.queue.full():
      return False
    self.queue.put(item)
    return True

  ''' Get()
  Gets the first item from the queue, if 
  it's not empty
  '''
  def Get(self):
    if self.queue.empty():
      return None
    return self.queue.get()

  ''' Size()
  Returns the internal queue's size
  '''
  def Size(self):
    return self.queue.qsize()