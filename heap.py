# implementation of min heap
class bcolors:
  HEADER = '\033[95m'
  OKBLUE = '\033[94m'
  OKCYAN = '\033[96m'
  OKGREEN = '\033[92m'
  WARNING = '\033[93m'
  FAIL = '\033[91m'
  ENDC = '\033[0m'
  BOLD = '\033[1m'
  UNDERLINE = '\033[4m'

class Heap():
  def __init__(self):
    self.capacity = 2
    self.arr = [None for i in range(self.capacity)]
    self.empty_index = 0
    self.size = 0

  def _resize(self):
    self.capacity = 2 * self.capacity
    new_arr = [None for i in range(self.capacity)]
    for i in range(len(self.arr)):
      new_arr[i] = self.arr[i]
    self.arr = new_arr
    
  def insert(self, item):
    if self.size >= 0.5 * self.capacity:
      self._resize()

    item_index = self.empty_index
    self.arr[item_index] = item
    self.size += 1
    self._set_empty_index()

    while True:
      parent_index = self._get_parent_index(item_index)
      if parent_index == -1:
        break
      elif self._item_value(item_index) < self._item_value(parent_index):
        self._swap_items(parent_index, item_index)
        item_index = parent_index
      else:
        break

  def insert_array(self, items):
    for item in items:
      self.insert(item)

  def get_size(self):
    return self.size

  def is_empty(self):
    return self.size == 0
    
  def _swap_items(self, index1, index2):
    tmp = self.arr[index1]
    self.arr[index1] = self.arr[index2]
    self.arr[index2] = tmp

  def peek_min(self):
    return self.arr[0]

  def remove_min(self):
    if self.is_empty():
      raise ValueError("Cannot remove from empty heap")
    item = self.arr[0]
    self.arr[0] = None
    index = 0
    while True:
      left_index = self._get_left_child_index(index)
      right_index = self._get_right_child_index(index)
      
      left_exists = left_index < self.capacity and self.arr[left_index] != None
      right_exists = right_index < self.capacity and self.arr[right_index] != None
      
      if left_exists and right_exists:
        if self._item_value(left_index) < self._item_value(right_index):
          self.arr[index] = self.arr[left_index]
          self.arr[left_index] = None
          index = left_index
        else:
          self.arr[index] = self.arr[right_index]
          self.arr[right_index] = None
          index = right_index
      elif left_exists:
        self.arr[index] = self.arr[left_index]
        self.arr[left_index] = None
        index = left_index
      elif right_exists:
        self.arr[index] = self.arr[right_index]
        self.arr[right_index] = None
        index = right_index
      else:
        break
    self.empty_index = min(self.empty_index, index)
    self.size -= 1
    return item

  def _item_value(self, index):
    if self.arr[index] == None:
      raise ValueError("Trying to access non-existent element")
    item = self.arr[index]
    if hasattr(item, "__getitem__"):
      return item[0]
    else:
      return item
    
  def _set_empty_index(self):
    for i in range(self.empty_index + 1, len(self.arr)):
      if self.arr[i] == None:
        self.empty_index = i
        return
    self.empty_index = self.capacity

  def _get_parent_index(self, index):
    return (index - 1)//2
  def _get_left_child_index(self, index):
    return 2 * index + 1
  def _get_right_child_index(self, index):
    return 2 * index + 2

  def verify_min_property(self):
    for i in range(len(self.arr)):
      if self.arr[i] == None:
        continue
      left_index = self._get_left_child_index(i)
      right_index = self._get_right_child_index(i)
      left_index_exists = left_index < self.capacity and self.arr[left_index] != None
      right_index_exists = right_index < self.capacity and self.arr[right_index] != None
      if (left_index_exists and self._item_value(i) > self._item_value(left_index)) or (right_index_exists and self._item_value(i) > self._item_value(right_index)):
        return False
    return True

  def _print(self):
    s = '['
    for i in range(len(self.arr)):
      if i == self.empty_index:
        s += f'{bcolors.OKGREEN}E{bcolors.ENDC}'
      elif self.arr[i] == None:
        continue #s += f'{bcolors.WARNING}N{bcolors.ENDC}'
      else:
        s += f'{bcolors.OKCYAN}{str(self.arr[i])}{bcolors.ENDC}'
      if i != len(self.arr) - 1:
        s += ', '
    s += ']'
    print(s)
    
import random

def random_boolean(k=0.5):
  return random.random() < k
def random_array(n):
  arr = []
  for i in range(n):
    arr.append(random.randint(1, 100))
  return arr

if __name__ == "__main__":

  for k in range(100):
    heap = Heap()
    arr_length = 100
    arr = random_array(arr_length)
    print(arr)
    i = 0
    while i < arr_length:
      heap._print()
      if random_boolean(k = 0.1) and not heap.is_empty():
        print(f'remove : {heap.remove_min()}')
      else:
        heap.insert(arr[i])
        print(f'insert : {arr[i]}')
        i+=1
      if not heap.verify_min_property():
        raise ValueError("min propterty false")
