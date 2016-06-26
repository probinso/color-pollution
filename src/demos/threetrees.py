#!/usr/bin/env python3
# - Utf 8 -

"""
Object Oriented Programming
"""

from collections import Iterable
class OTree:
  __slots__ = ('_value', '_left', '_right')
  def __init__(self, value):
    if not isinstance(value, Iterable):
      it = iter((value,))
    else:
      it = iter(value)

    self._value = next(it)
    self._left  = None
    self._right = None

    for elm in it:
      self.insert(elm)

  def insert(self, value):    
    current = self
    while True:
      if value < current._value:
        if current._left is None:
          current._left = OTree(value)
          break
        else:
          current = current._left
      else:
        if current._right is None:
          current._right = OTree(value)
          break
        else:
          current = current._right

  def __contains__(self, key):
    current = self
    while current:
      if key == current._value:
        return True
      current = current._left if key < current._value else current._right
    return False

"""
Functional Programming
"""
from collections import namedtuple
FTree = namedtuple('FTree', ['value', 'left', 'right'])
def insert(tree, value):
  if tree is None:
    return FTree(value, None, None)
  
  if value < tree.value:
    left  = insert(tree.left, value)
    right = tree.right
  else:
    left  = tree.left
    right = insert(tree.right, value)
  return FTree(tree.value, left, right)

def isin(tree, value):
  if tree is None: return False
  elif tree.value == value: return True

  elif value < tree.value: return isin(tree.left, value)
  else: return isin(tree.right, value)


"""
Procedural Programming
"""
class PTree(object):
  def __init__(self):
    self.value = None
    self.left  = None
    self.right = None

def pinsert(tree, value):
  current = tree

  if current.value is None:
    current.value = value
    return

  while current.value:
    if value < current.value:
      if current.left is None:
        current.left = PTree()
        current.left.value = value
        return
      else:
        current = current.left
    else:
      if current.right is None:
        current.right = PTree()
        current.right.value = value
        return
      else:
        current = current.right


def pisin(tree, value, out):
  out.clear()
  current = tree
  found = False
  while current:
    if value < current.value:
      current = current.left
    elif value > current.value:
      current = current.right
    elif value == current.value:
      found = True
      break

  out.append(found)

