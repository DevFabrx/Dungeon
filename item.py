#!/usr/bin/env python3

class Item:
  def __init__(self, **item):
    self.name = ""
    self.type = ""
    self.price = 0
    self.influenced_attribute = ""
    self.value = 0 
    self.__dict__.update(item)
