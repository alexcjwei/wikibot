from bs4 import BeautifulSoup
import requests

class Node:
  url = 'https://en.wikipedia.org/wiki/'

  def __init__(self, parent, name):
    self.parent = parent # index
    self.name = name # /wiki/name
    self.children = list()

  def get_name(self):
    return self.name

  def add_child(self, child):
      self.children.append(child)

  def get_parent(self):
    return self.parent

  def get_children(self):
    return self.children

  def get_path(self):
    if not self.parent:
      return f'{self.name}'
    return f'{self.name} -> {self.parent.get_path()}'

  def set_parent(self, parent):
    self.parent = parent